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

## 🦾 CI-CD

Les informations concernant le CI-CD se trouvent dans le fichier correspondant [CI-CD.md](CI-CD.md)

---

## 👮🏻‍♂️Sécurité

Les Consignes de sécurité sont rassemblées dans le fichier [SECURITY.md](SECURITY.md)