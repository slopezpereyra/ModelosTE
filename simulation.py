import math
import pandas as pd
from generators import SEED

def lambda_t(t):
    """Intensidad del proceso en función del tiempo (en horas): 

    λ(t) = 20 + 10 cos(π ⋅ t/12)

    """
    return 20 + 10 * math.cos(math.pi * t / 12)

def poisson_no_homogeneo(T, generator, lambda_function=lambda_t,  lambda_max=30):
    """
    Dada una función λ(t), simula un proceso de Poisson no homogéneo con dicha
    función, donde λₘₐₓ debe especificarse. Seteamos λₘₐₓ en 30 por defecto
    porque es el valor máximo de λ(t) = 20 + 10 (cos π ⋅ t/12).

    Utiliza una función generadora de uniformes `generator`.
    Simula tiempos de llegada usando el método de rechazo (thinning).
    
    T: tiempo total a simular (en horas)
    generator: función generadora de números uniformes U(0,1)
    lambda_max: cota superior de lambda(t)
    """
    t = 0
    arrivals = []
    while t < T:
        u = generator.gen_uniform()
        delta = -math.log(u) / lambda_max  
        t += delta
        if t >= T:
            break
        u = generator.gen_uniform()
        if u < lambda_function(t) / lambda_max:
            arrivals.append(t)
    return arrivals

def sim_exponencial(lamda, generator):
  U = 1 - generator.gen_uniform()
  return -math.log(U)/lamda

def simular_cola(arrivals, mu, generator):
    """
    Simula una cola de un solo servidor (FIFO).
    
    arrivals: lista de tiempos de llegada (en horas)
    mu: tasa de servicio (clientes/hora)
    
    Retorna:
        tiempos_espera, tiempos_en_sistema, cantidad_atendidos
    """
    # Corte: Momento en el tiempo en que se puede pasar a
    # atender al próximo elemento de la cola. Arranca en 0, se actualiza 
    # cada vez que un elemento termina de ser atendido (es expulsado de la
    # cola).
    corte = 0
    tiempos_espera = []
    tiempos_en_sistema = []

    # Por cada arrival, debemos simular su tiempo de atención.
    for arr in arrivals:
        duracion = sim_exponencial(1/mu, generator)
        # (s, e): Tiempo en que empieza y termina la atención, respectivamente.
        s = max(arr, corte) 
        e = s + duracion
        corte = e

        espera = s - arr
        en_sistema = e - arr
        tiempos_espera.append(espera)
        tiempos_en_sistema.append(en_sistema)

    return tiempos_espera, tiempos_en_sistema



def main(generator):
    """
    Dada una función que genera uniformes, corre toda la simulación, formatea
    los valores en un data frame y lo devuelve. Las features del data frame son: 

    - TLlegada: Tiempo de llegada 
    - TEspera: Tiempo de espera hasta ser atendido 
    - TEnSistema: Tiempo total en el sistema.
    - Duracion: Tiempo que duró la atención 
    - TInicio: Tiempo en que se lo atendió 
    -TFin: Tiempo en que se retiró de la cola

    """
    arrivals = poisson_no_homogeneo(48, generator)
    tiempos_espera, tiempos_en_sistema = simular_cola(arrivals, 35, generator)
    
    df = pd.DataFrame({
          "TLlegada": arrivals,
          "TEspera": tiempos_espera,
          "TEnSistema": tiempos_en_sistema
      })


    # Calculamos duración (TEnSistema = TEspera + duración)
    df["Duracion"] = df["TEnSistema"] - df["TEspera"]
    df["TInicio"] = df["TLlegada"] + df["TEspera"]
    df["TFin"] = df["TInicio"] + df["Duracion"]

    return df


