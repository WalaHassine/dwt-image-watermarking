import numpy as np
import pywt
from utils import psnr

def embed(I, w, alpha=0.05):
    """
    Phase d'insertion.
    I     : image hôte float64 [0,1]
    w     : signature binaire, taille (a/2, b/2)
    alpha : force d'insertion
    Retourne Y (image tatouée) et son PSNR.
    """
    App, (D11, D12, D13) = pywt.dwt2(I, 'haar')

    assert w.shape == D12.shape, (
        f"Taille incompatible : signature {w.shape} vs D12 {D12.shape}"
    )

    # D12'(i,j) = D12(i,j) + alpha * w(i,j)
    D12_new = D12 + alpha * w

    Y = pywt.idwt2((App, (D11, D12_new, D13)), 'haar')
    Y = np.clip(Y, 0.0, 1.0)

    score = psnr(I, Y)
    if score < 35:
        print(f"⚠ PSNR = {score:.2f} dB < 35 dB — réduire alpha")
    else:
        print(f"✓ PSNR = {score:.2f} dB — invisibilité correcte")

    return Y, score