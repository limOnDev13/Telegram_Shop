from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        db_column='parent_id'
    )

    class Meta:
        db_table = 'category'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent'],
                name='unique_children_names'
            )
        ]

    def __str__(self):
        return self.name

class ChannelToSubscribe(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=50)
    url = models.TextField()

    class Meta:
        db_table = 'channel_to_subscribe'

    def __str__(self):
        return self.title

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    img_path = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        db_column='category_id'
    )

    class Meta:
        db_table = 'product'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_pair_name_and_category_id'
            )
        ]

    def __str__(self):
        return self.name

class ShoppingCart(models.Model):
    id = models.IntegerField(primary_key=True)  # id = user_id

    class Meta:
        db_table = 'shopping_cart'

    def __str__(self):
        return f"Shopping Cart {self.id}"

class ProductShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        db_column='product_id'
    )
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='products',
        db_column='shopping_cart_id'
    )
    count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = 'product_shopping_cart'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'shopping_cart'],
                name='unique_pair_product_and_shopping_cart'
            )
        ]

    def __str__(self):
        return f"{self.product.name} x{self.count} in cart {self.shopping_cart.id}"
