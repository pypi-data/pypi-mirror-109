import functools
import itertools
import math
import operator
import time
from collections import namedtuple
from copy import deepcopy
from typing import (
    Dict,
    Generator,
    List,
    TYPE_CHECKING,
)

import gevent

if TYPE_CHECKING:
    from locust.runners import WorkerNode


def dispatch_users(
    worker_nodes,  # type: List[WorkerNode]
    user_class_occurrences: Dict[str, int],
    spawn_rate: float,
) -> Generator[Dict[str, Dict[str, int]], None, None]:
    """
    Generator function that dispatches the users
    in `user_class_occurrences` to the workers.
    The currently running users is also taken into
    account.

    It waits an appropriate amount of time between each iteration
    in order for the spawn rate to be respected, whether running in
    local or distributed mode.

    The spawn rate is only applicable when additional users are needed.
    Hence, if `user_class_occurrences` contains less users than there are
    currently running, this function won't wait and will only run for
    one iteration. The logic for not stopping users at a rate of `spawn_rate`
    is that stopping them is a blocking operation, especially when
    having a `stop_timeout` and users with tasks running for a few seconds or
    more. If we were to dispatch multiple spawn messages to have a ramp down,
    we'd run into problems where the previous spawning would be killed
    by the new message. See the call to `self.spawning_greenlet.kill()` in
    `:py:meth:`locust.runners.LocalRunner.start` and `:py:meth:`locust.runners.WorkerRunner.worker`.

    :param worker_nodes: List of worker nodes
    :param user_class_occurrences: Desired number of users for each class
    :param spawn_rate: The spawn rate
    """
    # Get repeatable behaviour.
    worker_nodes = sorted(worker_nodes, key=lambda w: w.id)

    # This represents the already running users among the workers
    initial_dispatched_users = {
        worker_node.id: {
            user_class: worker_node.user_class_occurrences.get(user_class, 0)
            for user_class in user_class_occurrences.keys()
        }
        for worker_node in worker_nodes
    }

    # This represents the desired users distribution among the workers
    balanced_users = balance_users_among_workers(
        worker_nodes,
        user_class_occurrences,
    )

    # This represents the desired users distribution minus the already running users among the workers
    effective_balanced_users = {
        worker_node.id: {
            user_class: max(
                0,
                balanced_users[worker_node.id][user_class] - initial_dispatched_users[worker_node.id][user_class],
            )
            for user_class in user_class_occurrences.keys()
        }
        for worker_node in worker_nodes
    }

    number_of_users_per_dispatch = max(1, math.floor(spawn_rate))

    wait_between_dispatch = number_of_users_per_dispatch / spawn_rate

    dispatched_users = deepcopy(initial_dispatched_users)

    # The amount of users in each user class
    # is less than the desired amount
    less_users_than_desired = all(
        sum(x[user_class] for x in dispatched_users.values())
        < sum(x[user_class] for x in effective_balanced_users.values())
        for user_class in user_class_occurrences.keys()
    )

    if less_users_than_desired:
        while sum(sum(x.values()) for x in effective_balanced_users.values()) > 0:
            users_to_dispatch = users_to_dispatch_for_current_iteration(
                user_class_occurrences,
                dispatched_users,
                effective_balanced_users,
                balanced_users,
                number_of_users_per_dispatch,
            )

            ts = time.perf_counter()
            yield users_to_dispatch
            if sum(sum(x.values()) for x in effective_balanced_users.values()) > 0:
                delta = time.perf_counter() - ts
                sleep_duration = max(0.0, wait_between_dispatch - delta)
                assert sleep_duration <= 10, sleep_duration
                gevent.sleep(sleep_duration)

    elif (
        number_of_users_left_to_dispatch(dispatched_users, balanced_users, user_class_occurrences)
        <= number_of_users_per_dispatch
    ):
        yield balanced_users

    else:
        while not all_users_have_been_dispatched(effective_balanced_users):
            users_to_dispatch = users_to_dispatch_for_current_iteration(
                user_class_occurrences,
                dispatched_users,
                effective_balanced_users,
                balanced_users,
                number_of_users_per_dispatch,
            )

            ts = time.perf_counter()
            yield users_to_dispatch
            delta = time.perf_counter() - ts
            sleep_duration = (
                max(0.0, wait_between_dispatch - delta)
                if not all_users_have_been_dispatched(effective_balanced_users)
                else 0
            )
            assert sleep_duration <= 10, sleep_duration
            gevent.sleep(sleep_duration)


def users_to_dispatch_for_current_iteration(
    user_class_occurrences: Dict[str, int],
    dispatched_users: Dict[str, Dict[str, int]],
    effective_balanced_users: Dict[str, Dict[str, int]],
    balanced_users: Dict[str, Dict[str, int]],
    number_of_users_per_dispatch: int,
) -> Dict[str, Dict[str, int]]:
    if all(
        sum(map(operator.itemgetter(user_class), dispatched_users.values())) >= user_count
        for user_class, user_count in user_class_occurrences.items()
    ):
        dispatched_users.update(balanced_users)
        effective_balanced_users.update(
            {
                worker_node_id: {user_class: 0 for user_class in user_class_occurrences.keys()}
                for worker_node_id, user_class_occurrences in dispatched_users.items()
            }
        )

    else:
        ts_dispatch = time.perf_counter()

        number_of_workers = len(effective_balanced_users)

        number_of_users_in_current_dispatch = 0

        for i, user_class in enumerate(itertools.cycle(user_class_occurrences.keys())):
            # For large number of user classes and large number of workers, this assertion might fail.
            # If this happens, you can remove it or increase the threshold. Right now, the assertion
            # is there as a safeguard for situations that can't be easily tested (i.e. large scale distributed tests).
            assert i < 5000, "Looks like dispatch is stuck in an infinite loop (iteration {})".format(i)

            if sum(map(sum, map(dict.values, effective_balanced_users.values()))) == 0:
                break

            if all(
                sum(map(operator.itemgetter(user_class_), dispatched_users.values())) >= user_count
                for user_class_, user_count in user_class_occurrences.items()
            ):
                break

            if (
                sum(map(operator.itemgetter(user_class), dispatched_users.values()))
                >= user_class_occurrences[user_class]
            ):
                continue

            if go_to_next_user_class(user_class, user_class_occurrences, dispatched_users, effective_balanced_users):
                continue

            for j, worker_node_id in enumerate(itertools.cycle(effective_balanced_users.keys())):
                assert j < int(
                    2 * number_of_workers
                ), "Looks like dispatch is stuck in an infinite loop (iteration {})".format(j)
                if effective_balanced_users[worker_node_id][user_class] == 0:
                    continue
                dispatched_users[worker_node_id][user_class] += 1
                effective_balanced_users[worker_node_id][user_class] -= 1
                number_of_users_in_current_dispatch += 1
                break

            if number_of_users_in_current_dispatch == number_of_users_per_dispatch:
                break

        # Another assertion to safeguard against unforeseen situations. Ideally,
        # we want each dispatch loop to be as short as possible to compute, but with
        # a large amount of workers/user classes, it can take longer to come up with the dispatch solution.
        # If the assertion is raised, then it could be a sign that the code needs to be optimized for the
        # case that caused the assertion to be raised.
        assert time.perf_counter() - ts_dispatch < (
            0.5 if number_of_workers < 100 else 1 if number_of_workers < 250 else 1.5 if number_of_workers < 350 else 3
        ), "Dispatch iteration took too much time: {}s (len(workers) = {}, len(user_classes) = {})".format(
            time.perf_counter() - ts_dispatch, number_of_workers, len(user_class_occurrences)
        )

    return {
        worker_node_id: dict(sorted(user_class_occurrences.items(), key=lambda x: x[0]))
        for worker_node_id, user_class_occurrences in sorted(dispatched_users.items(), key=lambda x: x[0])
    }


def go_to_next_user_class(
    current_user_class: str,
    user_class_occurrences: Dict[str, int],
    dispatched_users: Dict[str, Dict[str, int]],
    effective_balanced_users: Dict[str, Dict[str, int]],
) -> bool:
    """
    Whether to skip to next user class or not. This is done so that
    the distribution of user class stays approximately balanced during
    a ramp up.
    """
    dispatched_user_class_occurrences = {
        user_class: sum(map(operator.itemgetter(user_class), dispatched_users.values()))
        for user_class in user_class_occurrences.keys()
    }
    if all(n > 0 for n in dispatched_user_class_occurrences.values()):
        if not current_user_class_will_keep_distribution_better_than_all_other_user_classes(
            current_user_class, user_class_occurrences, dispatched_user_class_occurrences
        ):
            return True
        else:
            return False
    else:
        # Because each user class doesn't have at least one user, we use a simpler strategy
        # that make sure the each user class appears once.
        for user_class in filter(
            functools.partial(operator.ne, current_user_class), sorted(user_class_occurrences.keys())
        ):
            if sum(map(operator.itemgetter(user_class), effective_balanced_users.values())) == 0:
                # No more users of class `user_class` to dispatch
                continue
            if (
                dispatched_user_class_occurrences[current_user_class] - dispatched_user_class_occurrences[user_class]
                >= 1
            ):
                # There's already enough `current_user_class` for the current dispatch. Hence, we should
                # not consider `current_user_class` and go to the next user class instead.
                return True
        return False


def current_user_class_will_keep_distribution_better_than_all_other_user_classes(
    current_user_class: str,
    user_class_occurrences: Dict[str, int],
    dispatched_user_class_occurrences: Dict[str, int],
) -> bool:
    distances = get_distances_from_ideal_distribution(
        current_user_class, user_class_occurrences, dispatched_user_class_occurrences
    )
    if distances.actual_distance_with_current_user_class > distances.actual_distance and all(
        not current_user_class_will_keep_distribution(
            user_class, user_class_occurrences, dispatched_user_class_occurrences
        )
        for user_class in user_class_occurrences.keys()
        if user_class != current_user_class
    ):
        # If we are here, it means that if one user of `current_user_class` is added
        # then the distribution will be the best we can get. In other words, adding
        # one user of any other user class won't yield a better distribution.
        return True
    if distances.actual_distance_with_current_user_class <= distances.actual_distance:
        return True
    return False


def current_user_class_will_keep_distribution(
    current_user_class: str,
    user_class_occurrences: Dict[str, int],
    dispatched_user_class_occurrences: Dict[str, int],
) -> bool:
    distances = get_distances_from_ideal_distribution(
        current_user_class, user_class_occurrences, dispatched_user_class_occurrences
    )
    if distances.actual_distance_with_current_user_class <= distances.actual_distance:
        return True
    return False


# `actual_distance` corresponds to the distance from the ideal distribution for the current
# dispatched users. `actual_distance_with_current_user_class` represents the distance
# from the ideal distribution if we were to add one user of the given `current_user_class`.
# Thus, we strive to find the right user class to add a user in that will give us
# a `actual_distance_with_current_user_class` less than `actual_distance`.
DistancesFromIdealDistribution = namedtuple(
    "DistancesFromIdealDistribution", "actual_distance actual_distance_with_current_user_class"
)


def get_distances_from_ideal_distribution(
    current_user_class: str,
    user_class_occurrences: Dict[str, int],
    dispatched_user_class_occurrences: Dict[str, int],
) -> DistancesFromIdealDistribution:
    user_classes = sorted(user_class_occurrences.keys())
    desired_weights = [
        user_class_occurrences[user_class] / sum(user_class_occurrences.values()) for user_class in user_classes
    ]
    actual_weights = [
        dispatched_user_class_occurrences[user_class] / sum(dispatched_user_class_occurrences.values())
        for user_class in user_classes
    ]
    actual_weights_with_current_user_class = [
        (
            dispatched_user_class_occurrences[user_class] + 1
            if user_class == current_user_class
            else dispatched_user_class_occurrences[user_class]
        )
        / (sum(dispatched_user_class_occurrences.values()) + 1)
        for user_class in user_classes
    ]
    actual_distance = math.sqrt(sum(map(lambda x: (x[1] - x[0]) ** 2, zip(actual_weights, desired_weights))))
    actual_distance_with_current_user_class = math.sqrt(
        sum(map(lambda x: (x[1] - x[0]) ** 2, zip(actual_weights_with_current_user_class, desired_weights)))
    )
    return DistancesFromIdealDistribution(actual_distance, actual_distance_with_current_user_class)


def number_of_users_left_to_dispatch(
    dispatched_users: Dict[str, Dict[str, int]],
    balanced_users: Dict[str, Dict[str, int]],
    user_class_occurrences: Dict[str, int],
) -> int:
    return sum(
        max(
            0,
            sum(x[user_class] for x in balanced_users.values()) - sum(x[user_class] for x in dispatched_users.values()),
        )
        for user_class in user_class_occurrences.keys()
    )


def all_users_have_been_dispatched(effective_balanced_users: Dict[str, Dict[str, int]]) -> bool:
    return all(
        user_count == 0
        for user_class_occurrences in effective_balanced_users.values()
        for user_count in user_class_occurrences.values()
    )


def balance_users_among_workers(
    worker_nodes,  # type: List[WorkerNode]
    user_class_occurrences: Dict[str, int],
) -> Dict[str, Dict[str, int]]:
    """
    Balance the users among the workers so that
    each worker gets around the same number of users of each user class
    """
    balanced_users = {
        worker_node.id: {user_class: 0 for user_class in sorted(user_class_occurrences.keys())}
        for worker_node in worker_nodes
    }

    user_class_occurrences = user_class_occurrences.copy()

    total_users = sum(user_class_occurrences.values())
    users_per_worker, remainder = divmod(total_users, len(worker_nodes))

    for user_class in sorted(user_class_occurrences.keys()):
        if sum(user_class_occurrences.values()) == 0:
            break
        for worker_node in itertools.cycle(worker_nodes):
            if user_class_occurrences[user_class] == 0:
                break
            if (
                sum(balanced_users[worker_node.id].values()) == users_per_worker
                and total_users - sum(map(sum, map(operator.methodcaller("values"), balanced_users.values())))
                > remainder
            ):
                continue
            elif (
                sum(balanced_users[worker_node.id].values()) == users_per_worker + 1
                and total_users - sum(map(sum, map(operator.methodcaller("values"), balanced_users.values())))
                < remainder
            ):
                continue
            balanced_users[worker_node.id][user_class] += 1
            user_class_occurrences[user_class] -= 1

    return balanced_users
