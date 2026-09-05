from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Catégorie de pagnes (ex: Véritable Vlisco Wax, Pagne simple, Véritable ABC Wax)."""
    name = models.CharField('Nom de la catégorie', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=100, unique=True, blank=True)
    description = models.TextField('Description', blank=True)
    icon = models.CharField('Icône ou Emoji', max_length=20, default='✨', help_text='Ex. ✨, 👑, 🌿, 💎')
    order = models.PositiveIntegerField('Ordre d\'affichage', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.icon} {self.name}'

    @property
    def price_display(self):
        """Calcule dynamiquement le prix ou la plage de prix de la catégorie."""
        prods = self.products.filter(is_available=True)
        if not prods.exists():
            prods = self.products.all()
        if not prods.exists():
            return ""
        prices = sorted(list(set(prods.values_list('price', flat=True))))
        if not prices:
            return ""
        min_p = prices[0]
        max_p = prices[-1]
        if min_p == max_p:
            return f"{min_p:,}".replace(',', ' ') + " FCFA"
        return f"{min_p:,}".replace(',', ' ') + " à " + f"{max_p:,}".replace(',', ' ') + " FCFA"


class Product(models.Model):
    """Un pagne du catalogue SHM Shop."""
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Catégorie'
    )
    name = models.CharField('Nom du pagne', max_length=120)
    reference = models.CharField('Référence', max_length=30, unique=True,
                                 help_text='Ex. ABC-001, ORI-001, CHIG-001')
    price = models.PositiveIntegerField('Prix (FCFA)')
    old_price = models.PositiveIntegerField('Ancien prix (FCFA)', null=True, blank=True,
                                            help_text='Renseigner uniquement en cas de promotion.')
    description = models.TextField('Description', blank=True)
    motif = models.CharField('Motif et couleurs', max_length=140, blank=True)
    image = models.ImageField('Photo principale', upload_to='products/')
    is_available = models.BooleanField('En stock (disponible)', default=True)
    is_new = models.BooleanField('Nouveauté', default=False)
    is_promo = models.BooleanField('En promotion', default=False)
    created_at = models.DateTimeField('Ajouté le', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Pagne'
        verbose_name_plural = 'Pagnes'

    def __str__(self):
        return f'{self.reference} : {self.name}'

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.pk])

    @property
    def price_display(self):
        return f"{self.price:,}".replace(',', ' ') + " FCFA"

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round(100 - (self.price * 100 / self.old_price))
        return None


class ProductImage(models.Model):
    """Photos supplémentaires d'un pagne (galerie de la page produit)."""
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Photo', upload_to='products/')
    alt = models.CharField('Description de la photo', max_length=120, blank=True)

    class Meta:
        verbose_name = 'Photo supplémentaire'
        verbose_name_plural = 'Photos supplémentaires'

    def __str__(self):
        return f'Photo de {self.product.reference}'
