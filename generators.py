import numpy as np
from abc import ABC, abstractmethod

SEED = 48151


class Generator(ABC):

    def __init__(self):
        self.seed = SEED 
        self.u = None
        self.name = ""

    def gen_uniform(self):
        y, u = self.algorithm(self.seed)
        self.u = u 
        self.seed = y 
        return u
    
    @abstractmethod
    def algorithm(self, x_prev):
        pass

    def getName(self) -> str:
        return self.name


class GCL(Generator):
    """GCL: Implementa  

    Yₙ = aYₙ₋₁ + c    mod(m)        

    donde Uₙ = Yₙ/m. De este modo, genera n variables uniformes continuas. Por
    defecto, fija los parámetros a, c y m a los establecidos en la consigna del
    trabajo especial.
    """

    def __init__(self):
        super().__init__()
        self.name = "GCL"
        self.a = 16807
        self.c = 0
        self.m = 2**31 - 1

    def algorithm(self, y_prev):
        y_next = (self.a * y_prev + self.c) % self.m
        u_next = y_next / self.m
        return y_next, u_next
        

class XORShift(Generator):

    def __init__(self):
        super().__init__()
        self.name = "XORShift"

    def algorithm(self, x_prev):
        x = x_prev      & 0xFFFFFFFF
        x ^= (x << 13)  & 0xFFFFFFFF
        x ^= (x >> 17)  & 0xFFFFFFFF
        x ^= (x << 5)   & 0xFFFFFFFF
        u = x           / 0xFFFFFFFF
        return x, u


class PCG(Generator):
    # Se usó el algoritmo de Wikipedia adaptado a python

    def __init__(self):
        super().__init__()
        self.name = "PCG"

        # inicializar state y las constantes con numeros aleatorios
        self.increment = np.uint64(1442695040888963407)
        self.state = np.uint64(SEED + self.increment)
        self.multiplier = np.uint64(6364136223846793005)

    def rotr32(self, x, r):
        #with np.errstate(over='ignore'):               # ignorar warning de overflow, buscamos que esto ocurra
        return x >> r | x << (~r & 31)

    def algorithm(self, _):
        x = np.uint64(self.state)
        count = np.uint32(x >> 59)                      # 59 = 64 - 5
        #with np.errstate(over='ignore'):               # ignorar warning de overflow, buscamos que esto ocurra
        self.state = np.uint64(x * self.multiplier + self.increment)
        x ^= x >> 18
        random_int = int(self.rotr32(np.uint32(x >> 27), count))    # 27 = 32 - 5
        random_u = random_int / (np.uint32(0)-1)
        return 0, random_u




