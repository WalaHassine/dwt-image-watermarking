import numpy as np

def psnr(original, watermarked):
    """Calcule le PSNR entre l'image originale et l'image tatouée."""
    
    # Ajustement des dimensions si nécessaire
    h = min(original.shape[0], watermarked.shape[0])
    w = min(original.shape[1], watermarked.shape[1])

    original = original[:h, :w]
    watermarked = watermarked[:h, :w]

    mse = np.mean((original - watermarked) ** 2)

    if mse == 0:
        return float('inf')

    return 10 * np.log10(1.0 / mse)


def correlation(ww, w):
    """Corrélation de Pearson entre la signature extraite et l'originale."""
    num = np.sum(ww.flatten() * w.flatten())
    den = np.sqrt(np.sum(ww**2) * np.sum(w**2))
    return num / den if den != 0 else 0.0