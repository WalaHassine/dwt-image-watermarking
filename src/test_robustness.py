import math

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import io, pywt

from watermark_embed   import embed
from watermark_extract import extract
from utils             import correlation, psnr

# --- charger image de test ---
I = np.array(Image.open("dwt-image-watermarking/assets/grayscale-image.png")
              .convert("L"), dtype=np.float64) / 255.0
a, b = I.shape
w = np.random.randint(0, 2, (
    math.ceil(I.shape[0] / 2),
    math.ceil(I.shape[1] / 2)
))

#w = np.random.randint(0, 2, (a//2, b//2)).astype(np.float64)

# --- insérer le tatouage ---
Y, psnr_val = embed(I, w, alpha=0.05)

# --- définir les attaques ---
def attaque_bruit(img, sigma):
    return np.clip(img + np.random.normal(0, sigma, img.shape), 0, 1)

def attaque_flou(img, sigma):
    return gaussian_filter(img, sigma=sigma)

def attaque_jpeg(img, quality):
    buf = io.BytesIO()
    Image.fromarray((img*255).astype(np.uint8)).save(buf, "JPEG", quality=quality)
    buf.seek(0)
    return np.array(Image.open(buf)).astype(np.float64) / 255.0

# --- lancer les attaques et mesurer ---
attaques = {
    "Bruit σ=0.01"    : attaque_bruit(Y, 0.01),
    "Bruit σ=0.05"    : attaque_bruit(Y, 0.05),
    "Flou σ=1"        : attaque_flou(Y, 1),
    "Flou σ=2"        : attaque_flou(Y, 2),
    "JPEG 75%"        : attaque_jpeg(Y, 75),
    "JPEG 50%"        : attaque_jpeg(Y, 50),
    "JPEG 25%"        : attaque_jpeg(Y, 25),
}

print(f"{'Attaque':<16} {'PSNR':>8} {'Corrélation':>12} {'Résultat':>10}")
print("-" * 50)
for nom, img_att in attaques.items():
    ww = extract(img_att, I, alpha=0.05)
    corr = correlation(ww, w)
    p    = psnr(Y, img_att)
    ok   = "✓ détecté" if corr >= 0.75 else "✗ perdu"
    print(f"{nom:<16} {p:>7.1f}  {corr:>11.4f}  {ok:>10}")