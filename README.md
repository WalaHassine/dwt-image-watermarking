# dwt-image-watermarking
Cet algorithme décrit un système de **tatouage numérique (watermarking)** d'images. Voici à quoi il sert :

**Objectif principal :** Insérer une signature (marque invisible) dans une image numérique, afin de prouver la propriété ou l'authenticité de cette image.

---

**Il se compose de deux phases :**

**1. Phase d'insertion**
On prend une image originale et une signature (ex. logo, identifiant), on les transforme, on insère la signature discrètement dans l'image, puis on obtient une **image tatouée** — visuellement identique à l'originale, mais contenant la marque cachée.

**2. Phase de détection**
On prend l'image tatouée, on extrait la signature cachée, et on la compare à la signature originale pour vérifier l'authenticité.

---

**La technique utilisée est la DWT (Discrete Wavelet Transform) — transformation en ondelettes**, qui décompose l'image en plusieurs sous-bandes fréquentielles. La signature est insérée dans une sous-bande de détail (D₁₂) selon la formule :

> D₁₂'(i,j) = D₁₂(i,j) + α·w(i,j)

où `α` contrôle la force d'insertion (équilibre entre invisibilité et robustesse).

---
---

## Algorithme de Tatouage Numérique par DWT (Ondelettes)

---

### Phase d'Insertion

**Entrées :**
- `I` : image originale
- `w` : signature (watermark) à insérer
- `α` : facteur de pondération (force d'insertion)

**Sortie :**
- `Y` : image tatouée

```
DÉBUT
  [a, b] ← size(I)

  // Décomposition par DWT
  [App, D₁₁, D₁₂, D₁₃] ← DWT2(I, 'Haar')

  // Redimensionner w à la taille de la sous-bande choisie
  w ← resize(w, size(D₁₂))

  // Insertion de la signature dans la sous-bande de détail
  POUR i de 1 à a/2 FAIRE
    POUR j de 1 à b/2 FAIRE
      D₁₂'(i,j) ← D₁₂(i,j) + α × w(i,j)
    FIN POUR
  FIN POUR

  // Reconstruction de l'image tatouée par DWT Inverse
  Y ← IDWT2([App, D₁₁, D₁₂', D₁₃], 'Haar')

  // Évaluation de l'invisibilité
  psnr ← PSNR(I, Y)
  SI psnr > 35 dB ALORS
    RETOURNER Y   // Bonne invisibilité
  SINON
    Réduire α et recommencer
  FIN SI
FIN
```

---

### Phase de Détection / Extraction

**Entrées :**
- `Y` : image tatouée (potentiellement attaquée)
- `I` : image originale (pour méthode non-aveugle)
- `w` : signature originale (pour comparaison)
- `α` : facteur de pondération (même valeur qu'à l'insertion)

**Sortie :**
- `corr` : taux de corrélation (similarité entre signatures)

```
DÉBUT
  // Décomposition de l'image tatouée
  [App', D₁₁', D₁₂', D₁₃'] ← DWT2(Y, 'Haar')

  // Décomposition de l'image originale
  [App, D₁₁, D₁₂, D₁₃] ← DWT2(I, 'Haar')

  // Extraction de la signature
  POUR i de 1 à a/2 FAIRE
    POUR j de 1 à b/2 FAIRE
      ww(i,j) ← (D₁₂'(i,j) - D₁₂(i,j)) / α
    FIN POUR
  FIN POUR

  // Comparaison avec la signature originale
  corr ← corrélation(ww, w)

  SI corr ≥ seuil (ex: 0.75) ALORS
    RETOURNER "Signature détectée ✓"
  SINON
    RETOURNER "Signature absente ou corrompue ✗"
  FIN SI
FIN
```

---
```
+--------+--------+
|        |        |
|  App   |  D₁₁  |
| (LL)   | (LH)   |
|        |        |
+--------+--------+
|        |        |
|  D₁₂  |  D₁₃  |
| (HL)   | (HH)   |
|        |        |
+--------+--------+
```
---

Remarque :  
- Harr : type d'ondelette choisi pour la construction et decomposition d'images  
- Pour chaque paire de pixels voisins, elle calcule :  
Moyenne (passe-bas)  (a + b) / 2   → sous-bande App (LL)  
Différence (passe-haut)  (a - b) / 2  → sous-bandes de détail  

Pourquoi le choix de Harr pour le watermarking:   
- Très rapide à calculer  
- Simple à implémenter  
- Bonne localisation spatiale (elle détecte bien les contours)  
- Disponible directement dans Python avec pywt.dwt2(I, 'haar')  


### Remarque sur le choix de la sous-bande

- Insérer dans **D₁₂ (sous-bande de détail horizontale)** : bon compromis invisibilité/robustesse
- Plus on augmente le **niveau de décomposition** → plus la robustesse augmente, mais l'invisibilité diminue
- L'insertion dans **plusieurs sous-bandes** améliore la robustesse contre les attaques


**Les deux critères clés évalués sont :**
- **Invisibilité** : mesurée par le PSNR (doit être > 35 dB)
- **Robustesse** : capacité de la signature à résister aux attaques (compression, filtrage, etc.)

### Résultats 
<img width="296" height="172" alt="image" src="https://github.com/user-attachments/assets/d6e3396c-6ec7-429b-b671-83ef4df5f50a" />
