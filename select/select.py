def partition_around(arr, p, r, x):
    index = arr.index(x)
    arr[index], arr[r] = arr[r], arr[index]
    i = p - 1
    for j in range(p, r):
        if arr[j] <= x:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    return i + 1


def select_visualized(arr, p, r, i, depth=0):
    indent = "__" * depth
    print(
        f"{'|' if depth else ''}{indent}Current array: {arr[p:r + 1]}, looking for {i}-th element"
    )

    while (r - p + 1) % 5 != 0:
        for j in range(p + 1, r + 1):
            if arr[p] > arr[j]:
                arr[p], arr[j] = arr[j], arr[p]
        if i == 1:
            print(f"{'|' if depth else ''}{indent}The {i}-th element is {arr[p]}")
            return arr[p]
        p += 1
        i -= 1

    q = (r - p + 1) // 5

    for j in range(p, p + q):
        arr[j : j + 5] = sorted(arr[j : j + 5])

    x = select_visualized(arr, p + 2 * q, p + 3 * q - 1, (q + 1) // 2, depth + 1)
    print(f"{'|' if depth else ''}{indent}Median of medians: {x}")
    k = partition_around(arr, p, r, x) - p + 1

    if i == k:
        print(f"{'|' if depth else ''}{indent}The {i}-th element is {arr[p + k - 1]}")
        return arr[p + k - 1]
    elif i < k:
        return select_visualized(arr, p, p + k - 2, i, depth + 1)
    else:
        return select_visualized(arr, p + k, r, i - k, depth + 1)


arr = [34, 12, 67, 43, 9, 25, 56, 18, 90, 71, 65, 49, 32, 39, 81, 80, 38, 21, 5, 3]
i = 10
result = select_visualized(arr, 0, len(arr) - 1, i)
print(f"第{i}番目の要素は {result} です。")
