import random
import math
import sys


def rabin_miller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for trials in range(50):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True


def is_prime(num):
    # 排除0,1和负数
    if num < 2:
        return False

    # 创建小素数的列表,可以大幅加快速度
    # 如果是小素数,那么直接返回true
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                    103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                    211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                    449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                    587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                    853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                    991, 997]
    if num in small_primes:
        return True

    # 如果大数是这些小素数的倍数,那么就是合数,返回false
    for prime in small_primes:
        if num % prime == 0:
            return False

    # 如果这样没有分辨出来,就一定是大整数,那么就调用rabin算法
    return rabin_miller(num)


# 得到大整数,默认位数为150
def get_prime(key_size=150):
    while True:
        num = random.randrange(10 ** (key_size - 1), 10 ** key_size)
        if is_prime(num):
            return num


def gcd(a, b):  # 最大公因数递归判断
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(a % b, b)


def find_reverse(a, m):  # 扩展欧几里得算法求模逆 其中a * b ≡ 1(mod m)
    if gcd(a, m) == 0:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    b = u1 % m
    return b


def main():
    while True:
        q = get_prime()
        p = (2 * q) + 1
        if rabin_miller(p):
            break

    a = random.randint(1, p - 1)
    while True:
        g = random.randint(2, p - 1)
        x1 = pow(g, 2, p)
        x2 = pow(g, q, p)
        if x1 != 1 and x2 != 1:
            break

    y = pow(g, a, p)
    print("y=" + str(y))
    fileName = 'secret2.txt'
    file_temp = open(fileName, 'r+')  # 预读文件
    m = int(file_temp.read())
    k = random.randint(1, p - 2)
    print("k=" + str(k))
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p) )% p
    print("c(y1,y2)=" + "(" + str(c1) + "," + str(c2) + ")")
    V = pow(c1, a, p)
    m_test = c2 * find_reverse(V, p) % p
    if m_test == m:
        print("Success!")
    else:
        print("Fail.")


if __name__ == '__main__':
    main()
