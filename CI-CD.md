
## 🔃 CI/CD – Intégration & Déploiement Continu

### ⚙️ Intégration Continue (CI) – *GitHub Actions*

### Définition dans [workflows/tests.yml](.github/workflows/tests.yml)

Déclenchée à chaque `push` ou `pull request` sur toutes les branches :
1. **Install** : `pip install .` (gestion des dépendances via [pyproject.tml](pyproject.toml))
2. **Lint** : `flake8`, `pylint`
3. **Test** : démarrage de `flask run` avec vérification santé

---

### 🚀 Déploiement Continu (CD) - *Github Actions*

### Définition dans [workflows/deploy.yml](.github/workflows/deploy.yml)

#### Déploiement sur Replit

(Notre license Replit a expirée, donc le déploiement ne fonctionne pas, désolé)

#### Déploiement sur Github Pages

Pour montrer que le projet fonctionne, nous déployons aussi le projet sur Github Pages en mode static grace à Frozen-Flask, que nous utilisons pour build le projet avec [freeze_flask.py](freeze_flask.py)

#### 🧪 Environnement :

Pour customiser le déploiement de notre application, nous permettons à l'utilisateur de fournir des variables d'environnement pour activer le mode DEBUG, changer l'hôte et le port de l'application et même changer le niveau de débug de la console.
```bash
FLASK_DEBUG=FALSE
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
LOG_LEVEL=INFO
```

Nous utilisons aussi des Secrets Github afin de déployer notre application sur Replit.
```bash
REPLIT_TOKEN=1234567890
REPLIT_REPL_ID=0123
```
