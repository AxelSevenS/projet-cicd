# 🌍 EcoAlerte – Environmental Awareness Platform

## 🔥 Présentation

EcoAlerte est une plateforme web de sensibilisation à l’environnement développée pour le hackathon **"IA For Good"** à **Ynov Aix-en-Provence**.
Son but : éduquer les utilisateurs via des quiz, du contenu interactif et des conseils concrets, le tout généré dynamiquement grâce à l’IA.

> 🌱 *Chaque clic compte pour la planète.*

🔗 **Démo en ligne :** [EcoAlerte](https://eco-web-helper-carcazown.replit.app/)

---

## 🏗️ Architecture Technique

### 🎨 Frontend
- **HTML + Jinja2**
- **Bootstrap 5.3.0** + CSS personnalisé
- **JavaScript natif** (quiz, animations, compteurs)
- **Font Awesome 6.4.0**
- **Google Fonts** (Poppins)

### 🔧 Backend
- **Flask 3.1.1**
- Structure par routes
- Logging avec module Python `logging`

### 📄 Pages Clés
- `/` : Page d’accueil avec message fort + CTA
- `/info` : Données écologiques, chiffres clés
- `/quiz` : Quiz interactif avec score
- `/actions` : Conseils pratiques classés (maison, transport, etc.)
- `/share` : Partage réseaux sociaux

### 🔌 API
- `POST /api/quiz/submit` : Traitement et score du quiz

---

## 📂 Fichiers Statics

- `script.js` : fonctionnalités globales, animations
- `quiz.js` : logique quiz (timer, progression)
- `style.css` : thème écologique vert/bleu
- Icônes Font Awesome + typographie Poppins

---

## 🔃 CI/CD – Intégration & Déploiement Continu

### ⚙️ Intégration Continue (CI) – *GitHub Actions*

Déclenchée à chaque `push` ou `pull request` sur `main` et `dev` :
1. **Install** : `pip install -r requirements.txt`
2. **Lint** : `flake8`, `pylint`
3. **Test** : démarrage de `flask run` avec vérification santé

---

### 🚀 Déploiement Continu (CD)

#### 🟢 Replit (Production Live)
- Déploiement auto sur `main`
- Gunicorn configuré : `0.0.0.0:5000`
- Environnement Nix + autoscale activé

#### 🖥️ VM Personnelle (Backup)
- Pull automatique via `cron`
- Redémarrage via `systemd`
- Gunicorn multithread

#### 🧪 Environnement :
```bash
FLASK_DEBUG=0
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
LOG_LEVEL=INFO
```
