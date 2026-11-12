from dataclasses import dataclass
from typing import Iterable, Any


@dataclass
class SetCoverInstance:
    universe: tuple
    subsets: tuple
    masks: tuple
    full_mask: int
    covering_indices: tuple


def prepare_instance(universe: Iterable[Any],
                     subsets: Iterable[Iterable[Any]]) -> SetCoverInstance:
    """Convert a Set Cover instance into an efficient bitmask representation."""
    universe = tuple(dict.fromkeys(universe))
    subsets = tuple(tuple(dict.fromkeys(s)) for s in subsets)

    element_to_index = {element: i for i, element in enumerate(universe)}

    masks = []
    for subset in subsets:
        mask = 0
        for element in subset:
            if element not in element_to_index:
                raise ValueError(f"Element {element!r} is not in the universe.")
            mask |= 1 << element_to_index[element]
        masks.append(mask)

    full_mask = (1 << len(universe)) - 1

    covering_indices = []
    for element_index in range(len(universe)):
        bit = 1 << element_index
        candidates = tuple(
            i for i, mask in enumerate(masks) if mask & bit
        )
        covering_indices.append(candidates)

    return SetCoverInstance(
        universe=universe,
        subsets=subsets,
        masks=tuple(masks),
        full_mask=full_mask,
        covering_indices=tuple(covering_indices),
    )


def build_result(instance, selected_indices, execution_time,
                 explored_nodes, pruned_nodes=0):
    """Build a common result dictionary used by all algorithms."""
    selected_indices = list(selected_indices)
    return {
        "selected_indices": selected_indices,
        "selected_subsets": [instance.subsets[i] for i in selected_indices],
        "cardinality": len(selected_indices),
        "execution_time": execution_time,
        "explored_nodes": explored_nodes,
        "pruned_nodes": pruned_nodes,
        "feasible": True,
        "optimal": True,
    }


def infeasible_result(execution_time, explored_nodes, pruned_nodes=0):
    """Return a consistent result when no cover exists."""
    return {
        "selected_indices": [],
        "selected_subsets": [],
        "cardinality": None,
        "execution_time": execution_time,
        "explored_nodes": explored_nodes,
        "pruned_nodes": pruned_nodes,
        "feasible": False,
        "optimal": True,
    }
