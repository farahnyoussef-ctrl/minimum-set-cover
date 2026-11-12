def read_instance(filename):
    with open(filename, "r") as file:
        tokens = iter(map(int, file.read().split()))

    m = next(tokens)  # Number of elements
    n = next(tokens)  # Number of candidate subsets

    costs = [next(tokens) for _ in range(n)]

    if any(cost != 1 for cost in costs):
        raise ValueError("This instance is weighted.")

    universe = set(range(1, m + 1))
    subsets = {j: set() for j in range(1, n + 1)}

    for element in range(1, m + 1):
        count = next(tokens)

        for _ in range(count):
            subset_id = next(tokens)
            subsets[subset_id].add(element)

    return universe, subsets


filename = "OR-Library/test.txt"

universe, subsets = read_instance(filename)
print("Instance:", filename)
print("Elements:", len(universe))
print("Candidate subsets:", len(subsets))
print("universe:", sorted(universe))
print("subsets:", {k: sorted(v) for k, v in subsets.items()})
