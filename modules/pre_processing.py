import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, gamma
from sklearn.cluster import KMeans

def gerar_histograma(image):
    data = image.flatten()
    plt.hist(data, bins=256, density=True, alpha=0.5, label='Imagem')

    mu, std = norm.fit(data)
    x = np.linspace(min(data), max(data), 100)
    plt.plot(x, norm.pdf(x, mu, std), 'r', label='Normal')

    ag, locg, scaleg = gamma.fit(data, floc=0)
    plt.plot(x, gamma.pdf(x, ag, locg, scaleg), 'g', label='Gamma')

    plt.legend()
    plt.title('Histograma e Ajustes')
    plt.show()

    km = KMeans(n_clusters=2).fit(data.reshape(-1,1))
    print('Centros KMeans:', km.cluster_centers_)

def calcular_estatisticas(image):
    media = np.mean(image)
    variancia = np.var(image)
    desvio = np.std(image)
    enl = (media ** 2) / variancia
    return media, variancia, desvio, enl
