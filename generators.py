import random

def gcl(seed, a=16807, c=0, m=2**31 - 1, n=10):
    """GCL: Implementa  

    Yₙ = aYₙ₋₁ + c    mod(m)        

    donde Uₙ = Yₙ/m. De este modo, genera n variables uniformes continuas. Por
    defecto, fija los parámetros a, c y m a los establecidos en la consigna del
    trabajo especial.
    """
    values = []
    y = seed
    for _ in range(n):
        y = (a * y + c) % m
        u = y / m
        values.append(u)
    return values

def xorshift(seed, n=10):
    """Generador XORShift 32-bit."""
    values = []
    x = seed & 0xFFFFFFFF  # limitar a 32 bits
    for _ in range(n):
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        values.append(x / 0xFFFFFFFF)  # normalizar
    return values


def mersenne_twister(seed, n=10):
    random.seed(seed)  # Usa MT19937 internamente
    return [random.random() for _ in range(n)]
