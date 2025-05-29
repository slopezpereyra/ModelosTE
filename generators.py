SEED = 48151


def gcl(y_prev, a=16807, c=0, m=2**31 - 1):
    """GCL: Implementa  

    Yₙ = aYₙ₋₁ + c    mod(m)        

    donde Uₙ = Yₙ/m. De este modo, genera n variables uniformes continuas. Por
    defecto, fija los parámetros a, c y m a los establecidos en la consigna del
    trabajo especial.
    """
    y_next = (a * y_prev + c) % m
    u_next = y_next / m
    return y_next, u_next


def xorshift(x_prev):
    x = x_prev & 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17) & 0xFFFFFFFF
    x ^= (x << 5) & 0xFFFFFFFF
    u = x / 0xFFFFFFFF
    return x, u


class Generator:

  def __init__(self, u_function):
    self.u_function = u_function 
    self.seed = SEED 
    self.u = None

  def gen_uniform(self):
    y, u = self.u_function(self.seed)
    self.u = u 
    self.seed = y 
    return u






























