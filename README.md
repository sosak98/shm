# ✨ SHM Shop — Boutique en Ligne de Pagnes & Wax Africains

Plateforme e-commerce moderne, rapide et optimisée pour smartphone, conçue pour les boutiques de vente de pagnes à Cotonou et en Afrique de l'Ouest.

Le modèle d'achat est basé sur le **panier sans paiement en ligne obligatoire** : le client choisit ses modèles, ajuste les quantités et valide sa commande en **un clic sur WhatsApp** avec un récapitulatif clair et structuré envoyé directement à la boutique.

---

## 👗 Les 6 Collections en Stock (95 modèles réels)

1. 👑 **Véritable Vlisco Wax** : Wax Hollandais authentique 100% coton haut de gamme (**50 000 FCFA**) — *12 modèles*
2. 💎 **Faux Super Wax** : Imitation Super Wax soignée et éclatante (**15 000 FCFA**) — *9 modèles*
3. ✨ **Faux Vlisco Wax** : Imitation style hollandais aux motifs classiques (**15 000 FCFA**) — *22 modèles*
4. 🧵 **Super Chiganvy Wax** : Wax résistant et élégant en 6 yards (**9 000 à 10 000 FCFA**) — *10 modèles*
5. 🌸 **Véritable ABC Wax** : Coton doux et motifs traditionnels colorés (**6 500 FCFA**) — *25 modèles*
6. 🌿 **Pagne Simple** : Modèles accessibles pour le quotidien (séries Glory Wax & Chigan DAHO) (**2 500 FCFA**) — *17 modèles*

---

## 🚀 Fonctionnalités Clés

- 📱 **Mobile-First & PWA** : Application installable sur Android et iOS, fonctionnant hors-ligne grâce au Service Worker.
- 🧺 **Panier Intelligent** : Gestion fluide en local (`localStorage`), calcul en direct des totaux en FCFA.
- 💬 **Génération de Commande WhatsApp** : Message préformaté prêt à l'envoi avec les références, noms, prix et total.
- ⚡ **Filtres Avancés** : Recherche instantanée, onglets par collection, filtres par budget (2 500 F, 6 500 F, 9 000-10 000 F, 15 000 F, 50 000 F) et promotions.
- 🛡️ **Keep-Alive Uptime** : Point de terminaison `/health/` pour monitoring continu sans mise en veille.
- 🎨 **Administration Moderne** : Interface de gestion Django avec aperçu visuel des tissus et gestion de stock.

---

## 💻 Installation & Démarrage Local

### 1. Prérequis
- Python 3.10+
- `pip` et `venv`

### 2. Démarrage rapide

```bash
# 1. Cloner ou extraire le projet
cd shmshop

# 2. Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations et charger le catalogue complet (95 pagnes)
python manage.py migrate
python manage.py load_demo

# 5. Lancer le serveur de développement
python manage.py runserver
```

L'application est alors disponible sur `http://127.0.0.1:8000/`.

---

## 🔐 Administration Sécurisée

Pour créer un compte administrateur personnalisé :

```bash
python manage.py createsuperuser
```

L'accès à l'interface d'administration se fait sur `/admin/`.

---

## ⚙️ Variables d'Environnement (Production)

| Variable | Description | Exemple |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | Clé secrète Django | `votre-cle-secrete-aleatoire` |
| `DJANGO_DEBUG` | Mode débogage (`1` en dev, `0` en prod) | `0` |
| `DJANGO_ALLOWED_HOSTS` | Domaines autorisés | `.onrender.com,monsite.com` |
| `DATABASE_URL` | Chaîne de connexion PostgreSQL | `postgres://user:pass@host/db` |
| `SHOP_WHATSAPP` | Numéro WhatsApp recevant les commandes | `22996437708` |

---

## 🌐 Déploiement en Production (Render / Cloud)

1. Créez un dépôt sur votre compte GitHub / GitLab.
2. Poussez votre code :
   ```bash
   git init
   git add .
   git commit -m "Déploiement initial SHM Shop"
   git branch -M main
   git remote add origin <URL_DE_VOTRE_DEPOT_GIT>
   git push -u origin main
   ```
3. Connectez votre dépôt sur [Render.com](https://render.com) en utilisant le fichier `render.yaml` fourni (Blueprint) ou comme Web Service Python.
4. Renseignez vos variables d'environnement dans le tableau de bord Render.
