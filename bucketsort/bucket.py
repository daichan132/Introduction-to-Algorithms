def bucket_sort(A):
    n = len(A)
    B = [[] for _ in range(n)]

    for i in range(n):
        index = int(n * A[i])
        print(index, A[i])
        B[index].append(A[i])

    print("before:", B)
    for i in range(n):
        insertion_sort(B[i])

    print("after:", B)
    result = []
    for i in range(n):
        result += B[i]

    return result


def insertion_sort(A):
    n = len(A)
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = key


A = [0.2, 0.73, 0.53, 0.12, 0.61]
sorted_A = bucket_sort(A)
print(sorted_A)
