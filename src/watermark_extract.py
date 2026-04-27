import numpy as np
import pywt
from utils import correlation

def extract(Y, I, alpha=0.05, threshold=0.75):
    """
    Phase de détection (non-aveugle).
    Y     : image tatouée float64 [0,1]
    I     : image originale float64 [0,1]
    alpha : même valeur qu'à l'insertion
    Retourne ww (signature extraite) et le score de corrélation.
    """
    _, (_, D12_Y, _) = pywt.dwt2(Y, 'haar')
    _, (_, D12_I, _) = pywt.dwt2(I, 'haar')

    # ww(i,j) = (D12'(i,j) - D12(i,j)) / alpha
    ww = (D12_Y - D12_I) / alpha

    return ww   # passer ww et w à correlation() pour décider