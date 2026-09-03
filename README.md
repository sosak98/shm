# ✨ SHM Shop : Boutique catalogue de pagnes

Catalogue en ligne de pagnes africains **sans paiement en ligne** :
le client parcourt, ajoute au **panier**, puis envoie sa commande en
**un seul message WhatsApp pré-rempli** (récapitulatif + total) directement
à la vendeuse.

```
Client -> Catalogue -> Pagne -> 🧺 Panier -> [ Commander ] -> 📱 WhatsApp -> Vendeuse
```

## ✨ Collections disponibles (35 pagnes réels avec photos)

1. ✨ **Véritable ABC Wax** : 25 pagnes à **6 500 FCFA**
2. 💎 **Super Chiganvy Wax** : 10 pagnes à **9 000 FCFA / 10 000 FCFA**

## 📞 Coordonnées de contact
- 💬 **WhatsApp Commandes :** `+229 96 43 77 08` (commandes 24h/24 et 7j/7)
- 📞 **Ligne Directe Appels :** `+229 01 44 76 75 24`
- 📍 **Localisation :** Cotonou, Bénin
- 🕒 **Disponibilité :** 24h/24 et 7j/7 en ligne

---

## 💻 Tester le site en local (terminal Linux)

```bash
# 1. Aller dans votre dossier de téléchargement et décompresser
cd ~/Téléchargements || cd ~/Downloads
unzip SHM-Shop-Blueprint.zip
cd shmshop

# 2. Créer un environnement virtuel et installer les dépendances
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Initialiser la base de données et charger la démo (35 pagnes + catégories + admin)
python3 manage.py migrate
python3 manage.py load_demo

# 4. Lancer le site
python3 manage.py runserver
```

➡️ Ouvrir **http://127.0.0.1:8000** pour voir la boutique  
➡️ Ouvrir **http://127.0.0.1:8000/admin/** pour l'espace d'administration

## ⬆️ Pousser sur GitHub

```bash
cd shmshop
git init
git add .
git commit -m "SHM Shop : catalogue 35 pagnes, panier WhatsApp, PWA et Blueprint Render"
git branch -M main
git remote add origin https://github.com/sosak98/shm.git
git push -u origin main
```

## 🌍 Déploiement Automatique 1-Clic avec Render Blueprint

Grâce au fichier `render.yaml` inclus à la racine du projet, le déploiement sur Render est automatique :

1. Sur [Render.com](https://dashboard.render.com/), clique sur **New +** ➡️ **Blueprint**.
2. Sélectionne ton dépôt GitHub **`sosak98/shm`**.
3. Render configure tout tout seul ! Il te demande seulement de coller ton **`DATABASE_URL`** (ton URL PostgreSQL Neon).
4. Clique sur **Apply** et ton site est déployé en direct ! 🎉

## 🔑 Compte administrateur par défaut

- **Utilisateur :** `shmadmin`
- **Mot de passe :** `shmshop2026`
- Pour changer le mot de passe : `python3 manage.py changepassword shmadmin`

## ⚙️ Personnalisation (`shmshop/settings.py`)

`SHOP_NAME`, `SHOP_WHATSAPP`, `SHOP_PHONE_DISPLAY`, `SHOP_ADDRESS`, `SHOP_HOURS`.

## 🗂️ Structure

```
shmshop/
├── render.yaml              # Déploiement automatique 1-clic Render
├── manage.py
├── requirements.txt
├── shmshop/                 # configuration Django (settings, urls)
├── shop/
│   ├── models.py            # Category + Product (pagne) + ProductImage (galerie)
│   ├── views.py             # pages + filtres catégories/prix + manifest PWA + service worker
│   ├── admin.py             # espace vendeuse moderne + dashboard KPI + gestion catégories
│   ├── templatetags/        # filtre FCFA + lien WhatsApp pré-rempli
│   └── management/commands/load_demo.py   # catalogue 35 pagnes + catégories + superuser
├── templates/
│   ├── base.html            # structure globale & navigation
│   ├── shop/                # accueil, catalogue, produit, panier, contact
│   └── admin/               # tableau de bord moderne & base admin
├── static/                  # css (style.css, admin-modern.css), js, icônes
└── media/products/          # photos réelles des 35 pagnes
```
