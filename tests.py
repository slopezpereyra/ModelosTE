from random import uniform
import generators as gen
import matplotlib.pyplot as plt

def ks_statistic(F, sample):

  sample = sorted(sample)
  n = len(sample)
  
  D = 0 
  for j in range(1, n+1):
    y = sample[j-1]
    d1 = j/n - F(y) 
    d2 = F(y) - (j-1)/n
    d = max(d1, d2)
    D = max(D, d)

  return D


def ks(F, sample, sim_sample_size=None, n_sims=1000):
    if sim_sample_size is None:
        sim_sample_size = len(sample)
    D = ks_statistic(F, sample)
    k = 0
    for _ in range(n_sims):
        sim_sample = [ uniform(0,1) for _ in range(sim_sample_size) ]
        sim_D = ks_statistic(lambda x: x, sim_sample)
        if sim_D >= D:
            k += 1

    return D, k / n_sims

# Este test lo sacamos de acá:
# https://www.cs.rice.edu/~johnmc/comp528/lecture-notes/Lecture22.pdf
def plot_overlapping_pairs(generator: gen.Generator, samples):
    # Generate samples
    # Create overlapping pairs (x_n, x_{n+1})
    x = samples[:-1]
    y = samples[1:]

    # Plot
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'b.', markersize=4)
    plt.xlabel('$x_n$')
    plt.ylabel('$x_{n+1}$')
    plt.title(f'Overlapping pairs - {generator.getName()}')
    plt.grid(True)
    plt.show()
  
def run_tests():

  def generate_samples(generator: gen.Generator, n):
    return [generator.gen_uniform() for _ in range(n)]

  
  for g in [gen.GCL(), gen.XORShift(), gen.PCG()]:

    X = generate_samples(g, 1000)
    # lambda x: x es la FPA de una uniforme, asumiendo x in [0, 1]
    D, p = ks(lambda x: x, X, sim_sample_size=1000, n_sims=1000)

    print(f"""
      ---------------------------------------\n
      KS test for generator {g.name}:\n
      D statistic = {D}\n 
      p-value = {p}
    """)

    plot_overlapping_pairs(g, X)

    if p <= 0.05:
      print(f"ERROR: Generador {g.name} no simula una uniforme U(0,1)")
      return 

  print("Todas las pruebas pasaron. :)")

























  
