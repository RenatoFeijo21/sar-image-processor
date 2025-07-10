import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, gamma
from scipy.special import kv as besselk, gamma as gamma_func
from scipy.optimize import curve_fit
from sklearn.cluster import KMeans

def gerar_histograma(image):
    data = image.flatten()
    plt.hist(data, bins=256, density=True, alpha=0.5, label='Imagem')

    # Ajuste Normal
    mu, std = norm.fit(data)
    x = np.linspace(min(data), max(data), 100)
    p_norm = norm.pdf(x, mu, std)
    plt.plot(x, p_norm, 'r', label='Normal')

    # Ajuste Gama
    ag, locg, scaleg = gamma.fit(data, floc=0)
    p_gamma = gamma.pdf(x, ag, locg, scaleg)
    plt.plot(x, p_gamma, 'g', label='Gamma')

    # Ajuste K-distribution
    try:
        popt = ajustar_k_distribution(data)
        p_k = k_distribution_pdf(x, *popt)
        plt.plot(x, p_k, 'b', label='K-distribution')
        print(f"K-distribution parâmetros: nu={popt[0]:.4f}, b={popt[1]:.4f}")
    except Exception as e:
        print("Erro no ajuste da K-distribution:", e)

    plt.legend()
    plt.title('Histograma e Ajustes')
    plt.show()

    # KMeans (indicativo preliminar)
    km = KMeans(n_clusters=2).fit(data.reshape(-1,1))
    print('Centros KMeans:', km.cluster_centers_)

    # Seleção preliminar do melhor ajuste (via SSE)
    sse_norm = np.sum((histograma_pdf(data, norm.pdf, [mu, std]) - data) ** 2)
    sse_gamma = np.sum((histograma_pdf(data, gamma.pdf, [ag, locg, scaleg]) - data) ** 2)
    sse_k = np.sum((histograma_pdf(data, k_distribution_pdf, popt) - data) ** 2)

    erros = {'Normal': sse_norm, 'Gamma': sse_gamma, 'K': sse_k}
    melhor = min(erros, key=erros.get)
    print("Melhor ajuste preliminar:", melhor)

def histograma_pdf(data, func, params):
    x = np.linspace(min(data), max(data), len(data))
    return func(x, *params)

def calcular_estatisticas(image):
    media = np.mean(image)
    variancia = np.var(image)
    desvio = np.std(image)
    enl = (media ** 2) / variancia
    return media, variancia, desvio, enl

def k_distribution_pdf(x, nu, b):
    return (2 * (b ** ((nu + 1)/2)) * (x ** nu) * besselk(nu - 1, 2 * np.sqrt(b * x))) / gamma_func(nu)

def ajustar_k_distribution(data):
    nu_init = 1.0
    b_init = 1.0
    hist, bins = np.histogram(data, bins=256, density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    popt, _ = curve_fit(k_distribution_pdf, bin_centers, hist, p0=[nu_init, b_init], maxfev=5000)
    return popt
