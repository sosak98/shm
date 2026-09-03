"""
Charge le catalogue complet de démonstration SHM Shop (35 pagnes réels avec photos)
et initialise le compte administrateur si absent.

    python manage.py load_demo
"""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shop.models import Category, Product

CATEGORIES = [
    {
        'slug': 'abc-wax',
        'name': 'Véritable ABC Wax (Block Prints)',
        'description': 'Collection Grand Quality Baba Fashion (100% coton, 6 yards). Motifs intenses et couleurs éclatantes.',
        'icon': '✨',
        'order': 1,
    },
    {
        'slug': 'orientar-kingtex',
        'name': 'Orientar Kingtex',
        'description': 'Collection Orientar Kingtex (100% coton, 6 yards). Motifs fins, géométries et designs nobles.',
        'icon': '👑',
        'order': 2,
    },
    {
        'slug': 'super-chiganvy',
        'name': 'Super Chiganvy Wax',
        'description': 'Pagne Wax Super Chiganvy de qualité supérieure (100% coton, 6 yards). Doux, résistant et élégant.',
        'icon': '💎',
        'order': 3,
    },
]

PAGNES = [
    # --- 1. VÉRITABLE ABC WAX (BLOCK PRINTS) - 6 500 FCFA ---
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-01', 'name': "Soleil d'Or & Tournesols",
        'price': 6500, 'old_price': None,
        'motif': 'Jaune moutarde et noir / calices floraux',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Motifs floraux solaires éclatants sur fond filigrane gris.',
        'image': 'products/IMG-20260903-WA0018.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-02', 'name': 'Canopée Émeraude',
        'price': 6500, 'old_price': None,
        'motif': 'Vert vif et noir / bosquets et feuillage',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Un vert végétal sublime et élégant.',
        'image': 'products/IMG-20260903-WA0019.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-03', 'name': 'Éventails Solaires',
        'price': 6500, 'old_price': 8000,
        'motif': 'Vert anis, jaune et noir / éventails géométriques',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Graphisme dynamique et couleurs rayonnantes.',
        'image': 'products/IMG-20260903-WA0020.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-04', 'name': 'Rosaces Royales Vertes',
        'price': 6500, 'old_price': None,
        'motif': 'Vert prairie et blanc cassé / arabesques florales',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Des rosaces raffinées parfaites pour tailleurs ou robes.',
        'image': 'products/IMG-20260903-WA0021.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-05', 'name': 'Tourbillon Saphir',
        'price': 6500, 'old_price': None,
        'motif': 'Bleu roi intense et beige / spirales et rosaces',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Un bleu roi profond et majestueux.',
        'image': 'products/IMG-20260903-WA0022.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-06', 'name': 'Fleurs de Jade',
        'price': 6500, 'old_price': None,
        'motif': 'Vert émeraude et blanc / grandes corolles 5 pétales',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). De ravissantes fleurs vert jade et blanches.',
        'image': 'products/IMG-20260903-WA0023.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-07', 'name': "Éventails d'Argent & Or",
        'price': 6500, 'old_price': 7500,
        'motif': 'Blanc lilas, doré et noir / faisceaux géométriques',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Alliance délicate de doré et lilas clair.',
        'image': 'products/IMG-20260903-WA0024.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-08', 'name': 'Feuillage Kaki Prestige',
        'price': 6500, 'old_price': None,
        'motif': 'Vert olive kaki et noir / petits nuages et frondaisons',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Ton kaki tendance et raffiné.',
        'image': 'products/IMG-20260903-WA0025.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-09', 'name': 'Lianes Somptueuses Kaki',
        'price': 6500, 'old_price': None,
        'motif': 'Vert kaki et noir profond / fleurs stylisées et clochettes',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Motif végétal moderne aux finitions soignées.',
        'image': 'products/IMG-20260903-WA0026.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-10', 'name': 'Palmes Aqua Tropicales',
        'price': 6500, 'old_price': None,
        'motif': 'Bleu ciel, vert menthe et noir / palmiers et bambous',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Nuances fraîches de bleu ciel et vert menthe.',
        'image': 'products/IMG-20260903-WA0027.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-11', 'name': 'Volutes Vert Bouteille',
        'price': 6500, 'old_price': None,
        'motif': 'Vert forêt et noir / dentelle graphique',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Tissu dense aux motifs arabesques.',
        'image': 'products/IMG-20260903-WA0028.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-12', 'name': 'Jardin Tropical Vert & Jaune',
        'price': 6500, 'old_price': 8000,
        'motif': 'Vert anis, jaune soleil et touches blanches',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Couleurs chaleureuses et estivales.',
        'image': 'products/IMG-20260903-WA0030.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-13', 'name': "Fleurs d'Automne Kaki",
        'price': 6500, 'old_price': None,
        'motif': 'Kaki sauge et noir / bouquets floraux',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Élégance sobre et distinguée.',
        'image': 'products/IMG-20260903-WA0031.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-14', 'name': 'Délice Floral Émeraude',
        'price': 6500, 'old_price': None,
        'motif': 'Vert émeraude / pétales épanouis',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Fleurons épanouis d’un vert intense.',
        'image': 'products/IMG-20260903-WA0033.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-15', 'name': 'Arbre de Vie Olive',
        'price': 6500, 'old_price': None,
        'motif': 'Vert olive et noir / silhouettes arborescentes',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Symbole universel de vie et de prospérité.',
        'image': 'products/IMG-20260903-WA0037.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'abc-wax',
        'reference': 'SHM-ABC-16', 'name': 'Oiseau du Paradis Kaki',
        'price': 6500, 'old_price': 8000,
        'motif': 'Kaki et noir / oiseaux en vol au clair de lune',
        'description': 'Véritable ABC Wax Block Prints 100% coton (6 yards). Oiseau en plein envol dans médaillon strié.',
        'image': 'products/IMG-20260903-WA0039.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },

    # --- 2. ORIENTAR KINGTEX - 6 500 FCFA ---
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-01', 'name': 'Alphabet Impérial Vert & Rouge',
        'price': 6500, 'old_price': None,
        'motif': 'Vert forêt, damier bordeaux et lettres stylisées',
        'description': 'Orientar Kingtex 100% coton (6 yards). Motifs lettres et damiers nobles.',
        'image': 'products/IMG-20260903-WA0029.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-02', 'name': 'Spirales Perlées Vert & Crème',
        'price': 6500, 'old_price': None,
        'motif': 'Vert olive et crème / spirales coquillages et perles',
        'description': 'Orientar Kingtex 100% coton (6 yards). Effet relief avec chapelets de perles graphiques.',
        'image': 'products/IMG-20260903-WA0032.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-03', 'name': "Feuilles d'Érable Kaki Rayé",
        'price': 6500, 'old_price': None,
        'motif': "Kaki rayé et noir / feuilles d'érable flottantes",
        'description': 'Orientar Kingtex 100% coton (6 yards). Texture rayée fine et feuilles d’érable majestueuses.',
        'image': 'products/IMG-20260903-WA0034.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-04', 'name': 'Éventails Royaux Kaki',
        'price': 6500, 'old_price': None,
        'motif': 'Vert olive strié et noir / grands éventails plissés',
        'description': 'Orientar Kingtex 100% coton (6 yards). Grand classique chic des cérémonies.',
        'image': 'products/IMG-20260903-WA0035.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-05', 'name': "Épis de Blé d'Or & Kaki",
        'price': 6500, 'old_price': 7500,
        'motif': "Fond kaki rayé / gerbes d'épis de blé",
        'description': 'Orientar Kingtex 100% coton (6 yards). Motifs épis de blé symbole d’abondance.',
        'image': 'products/IMG-20260903-WA0036.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-06', 'name': 'Trèfles Arabesques Cacao',
        'price': 6500, 'old_price': None,
        'motif': 'Marron chocolat, crème et noir / trèfles entrelacés',
        'description': 'Orientar Kingtex 100% coton (6 yards). Teintes terre chaudes et trèfles hypnotiques.',
        'image': 'products/IMG-20260903-WA0038.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-07', 'name': 'Cibles Stellaires Mauve & Noir',
        'price': 6500, 'old_price': None,
        'motif': 'Mauve poudré, blanc et noir / cercles concentriques',
        'description': 'Orientar Kingtex 100% coton (6 yards). Fond mauve doux aux cercles optiques modernes.',
        'image': 'products/IMG-20260903-WA0040.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-08', 'name': 'Soleils & Éclairs Safari',
        'price': 6500, 'old_price': 8000,
        'motif': 'Ocre jaune, orange et noir / roues solaires',
        'description': 'Orientar Kingtex 100% coton (6 yards). Énergie vive d’orange et ocre chaud.',
        'image': 'products/IMG-20260903-WA0041.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'orientar-kingtex',
        'reference': 'SHM-ORI-09', 'name': 'Lianes et Oiseaux Nocturnes',
        'price': 6500, 'old_price': None,
        'motif': 'Kaki clair et noir / feuillages et médaillons',
        'description': 'Orientar Kingtex 100% coton (6 yards). Motifs délicats inspirés de la faune et flore.',
        'image': 'products/IMG-20260903-WA0042.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },

    # --- 3. SUPER CHIGANVY WAX - 9 000 à 10 000 FCFA ---
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-01', 'name': 'Sillage Royal',
        'price': 9500, 'old_price': 12000,
        'motif': 'Turquoise et or / volutes florales',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un motif aqua lumineux rehaussé de doré, parfait pour les grandes occasions.',
        'image': 'products/IMG-20260822-WA0015.jpg',
        'is_new': True, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-02', 'name': 'Élégance Nocturne',
        'price': 10000, 'old_price': None,
        'motif': 'Noir, blanc et gris / spirales graphiques',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un classique noir et blanc, chic en toute circonstance.',
        'image': 'products/IMG-20260822-WA0016.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-03', 'name': "Roses d'Abomey",
        'price': 9000, 'old_price': 11000,
        'motif': 'Bleu nuit / grandes roses bleues',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). De somptueuses roses sur fond bleu nuit, très apprécié des clientes.',
        'image': 'products/IMG-20260822-WA0012.jpg',
        'is_new': True, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-04', 'name': 'Flamme du Sahel',
        'price': 9500, 'old_price': 12000,
        'motif': 'Orange vif / feuilles noir et jaune',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un orange solaire et éclatant qui ne passe pas inaperçu.',
        'image': 'products/IMG-20260822-WA0017.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-05', 'name': 'Pétales d’Harmonie',
        'price': 10000, 'old_price': None,
        'motif': 'Rose poudré et noir / feuilles tropicales',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un rose délicat souligné de noir, doux et élégant.',
        'image': 'products/IMG-20260822-WA0014.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-06', 'name': 'Racines',
        'price': 9000, 'old_price': None,
        'motif': 'Marron et crème / spirales ethniques',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Des tons terre chaleureux, idéal pour un style authentique.',
        'image': 'products/IMG-20260822-WA0010.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-07', 'name': 'Nuit d’Ébène',
        'price': 10000, 'old_price': None,
        'motif': 'Indigo profond / touches crème et orange',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un bleu profond sophistiqué aux motifs floraux stylisés.',
        'image': 'products/IMG-20260822-WA0007.jpg',
        'is_new': False, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-08', 'name': 'Cercles Sacrés',
        'price': 9500, 'old_price': None,
        'motif': 'Bleu royal / cercles imbriqués',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un bleu royal intense aux motifs traditionnels revisités.',
        'image': 'products/IMG-20260822-WA0003.jpg',
        'is_new': False, 'is_promo': False, 'is_available': False,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-09', 'name': 'Jardin Précieux',
        'price': 10000, 'old_price': None,
        'motif': 'Rose pâle et or / fleurs royales',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un mélange précieux de rose et d’or, réservé aux looks royaux.',
        'image': 'products/IMG-20260822-WA0013.jpg',
        'is_new': True, 'is_promo': False, 'is_available': True,
    },
    {
        'category_slug': 'super-chiganvy',
        'reference': 'SHM-CHIG-10', 'name': 'Feuilles du Soir',
        'price': 9000, 'old_price': 11500,
        'motif': 'Blanc cassé / feuilles bordeaux',
        'description': 'Pagne Wax Super Chiganvy 100% coton (6 yards). Un contraste raffiné de bordeaux sur fond clair.',
        'image': 'products/IMG-20260822-WA0006.jpg',
        'is_new': False, 'is_promo': True, 'is_available': True,
    },
]


class Command(BaseCommand):
    help = 'Charge les catégories et le catalogue complet SHM Shop (35 pagnes).'

    def handle(self, *args, **options):
        # 1. Catégories
        cats = {}
        for cdata in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=cdata['slug'],
                defaults=cdata,
            )
            cats[cdata['slug']] = cat
        self.stdout.write(self.style.SUCCESS(f'{len(cats)} catégorie(s) configurée(s).'))

        # 2. Produits
        created = 0
        for pdata in PAGNES:
            data = dict(pdata)
            cat_slug = data.pop('category_slug')
            data['category'] = cats.get(cat_slug)

            prod, was_created = Product.objects.update_or_create(
                reference=data['reference'],
                defaults=data,
            )
            created += int(was_created)

        # Nettoyage des anciennes références SHM-001 si présentes
        Product.objects.filter(reference__startswith='SHM-00').delete()

        total = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'{created} pagne(s) créé(s) / {total} pagne(s) au total dans le catalogue.'
        ))

        # 3. Compte administrateur démo si absent
        admin_user = 'shmadmin'
        admin_pass = 'shmshop2026'
        admin_email = 'contact@shmshop.bj'
        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(
                username=admin_user,
                email=admin_email,
                password=admin_pass
            )
            self.stdout.write(self.style.SUCCESS(
                f'Compte administrateur créé : {admin_user} / {admin_pass}'
            ))
        else:
            self.stdout.write(self.style.NOTICE(
                f'Compte administrateur démo ({admin_user}) déjà présent.'
            ))
