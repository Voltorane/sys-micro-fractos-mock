def newton_bin_expansion(a, b, n):
    result = 0
    for k in range(0, n + 1):
        result += binomial(n, k) * pow(a, n - k) * pow(b, k)
    return result


def binomial(n, k):
    if not 0 <= k <= n:
        return 0
    else:
        return factorial(n) / (factorial(k) * factorial(n - k))


def factorial(n):
    if n == 1 or n == 0: 
        return 1
    else:
        return n * factorial(n - 1)


if __name__ == "__main__":
    print(newton_bin_expansion(2, 2, 2))
