from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator

# Mahsulot uchu zarur modellar

class BrendModel(models.Model):
    """Brend"""
    brend = models.CharField(max_length=30, validators=[MinLengthValidator(3)])

def deleteBrend():
    """'BrendModel' ga tegishli 'deleted' obyektini qaytaradi"""
    return BrendModel.objects.get_or_create(brend='deleted')[0]

class CountryModel(models.Model):
    country = models.CharField(max_length=20)

def deleteCountry():
    """'CountryModel' ga tegishli 'deleted' obyektini qaytaradi"""
    return CountryModel.objects.get_or_create(country='deleted')[0]

class ProductModel(models.Model):
    """Mahsulot modeli"""
    name = models.CharField(max_length=30, validators=[MinLengthValidator(3)])                              # Mahsulot qisqa nomi
    title = models.CharField(max_length=65, validators=[MinLengthValidator(3)], blank=True)                 # Mahsulot to'liq nomi
    description = models.TextField(max_length=300, validators=[MinLengthValidator(70)], blank=True)         # Tavfsif
    brend = models.ForeignKey(BrendModel, on_delete=models.SET(deleteBrend))                                # Mahsulot brendi
    country = models.ForeignKey(CountryModel, blank=True, on_delete=models.SET(deleteCountry))              # Mahsulot tayyorlangan mamlakat
    package_weight = models.FloatField(blank=True,validators=[MinValueValidator(0)])                        # Mahsulot paketining og'irligi
    discount = models.PositiveSmallIntegerField(default=0, validators=[MaxLengthValidator(100)])            # Mahsulot uchun berilgan chegirma
    common_price = models.FloatField(validators=[MinValueValidator(0)])                                     # Mahsulotning umumiy narxi
    price_via_special_card = models.FloatField(validators=[MinValueValidator(0)], blank=True) # !           # Mahsulotni brendning maxsus kartasi orqali narxi
    quantity = models.PositiveSmallIntegerField(blank=True, null=True)

def deleteProduct():
    return ProductModel.objects.get_or_create(name='deleted', brend=deleteBrend, common_price=0)[0]

class ProductImageModel(models.Model):
    """Mahsulot surati. Asos - {Mahsulot modeli}"""
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE) # Mahsulot
    images = models.ImageField(upload_to=f'products/images/{id}/')      # Mahsulot surati

def deletedUser():
    return User.objects.get_or_create(name='deleted')[0]

class CommentModel(models.Model):
    """Reytinglarni olib boradi"""
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET(deletedUser))
    comment = models.TextField(max_length=150, blank=True)
    rating = models.PositiveIntegerField(validators=[MaxLengthValidator(5)])

class ShareModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET(deletedUser))
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class FavoriteModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.SET(deleteProduct))

class BonusModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField(validators=[MaxLengthValidator(100)], blank=True)
    bonus = models.PositiveSmallIntegerField(blank=True)

