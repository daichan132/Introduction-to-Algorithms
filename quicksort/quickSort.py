import random


def QUICKSORT(A, p, r):
    if p < r:
        q = partition(A, p, r)
        print(A)

        QUICKSORT(A, p, q - 1)
        QUICKSORT(A, q + 1, r)


def partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if A[j] <= x:
            i = i + 1
            A[i], A[j] = A[j], A[i]

    A[i + 1], A[r] = A[r], A[i + 1]

    return i + 1


if __name__ == "__main__":
    DATA = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    QUICKSORT(DATA, 0, len(DATA) - 1)
    print(DATA)
