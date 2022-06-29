from math_exceptions import *


def factorial(n):
    """
    factorial calculates the factorial of a given number.
    represents the following: n!

    :param n: number for which the factorial value should be computed
    :return: factorial value of n
    """
    if n == 1 or n == 0: 
        return 1
    else:
        return n * factorial(n - 1)

def binomial(n, k):
    """
    binomial calculates the binomial coefficient "n choose k".

    :param n: represents an n-element set;
    :param k: k to be chosen elements;
    :return: an integer coefficient for the binomial theorem stated in newton_bin_expansion.
    """
    if not 0 <= k <= n:
        return 0
    else:
        return factorial(n) / (factorial(k) * factorial(n - k))

def newton_bin_expansion(a, b, n):
    """
    newton_bin_expansion describes the algebraic expansion of powers of a binomial.
    represents the followig polynomial: (a + b)^n.

    :param a: first argument;
    :param b: second argument;
    :param n: nonnegative integer power of polynimial;
    :return: expanded polynomial into a sum.
    """
    if n < 0:
        raise InvalidArgument("The power 'n' schould not be negative!")
    result = 0
    for k in range(0, n + 1):
        result += binomial(n, k) * pow(a, n - k) * pow(b, k)
    return result


if __name__ == "__main__":
    print(newton_bin_expansion(2, 2, 2))
