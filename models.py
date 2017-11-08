from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# 유저 데이터베이스, 회원가입시 아이디/패스워드/주소/폰번호/이름
# 나머지 부가적인 것들은 구매시 사용됨
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^010\d{4}\d{4}$',
                                 message="'-'를 제외하고 010xxxxxxxx 형식으로 입력해주세요")
    phoneNumber= models.CharField(max_length=13, validators=[phone_regex],blank=True)
    zipCode = models.CharField(max_length=200,null=True,blank=True)
    streetName = models.CharField(max_length=200,null=True,blank=True)
    subAddress = models.CharField(max_length=200,null=True,blank=True)
    detailAddress = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=20,blank=True)
    email = models.EmailField(blank=True)
    createDate = models.DateField(auto_now_add=True,blank=True)

    cumulativeAmount = models.PositiveIntegerField(default=0,null=True,blank=True)
    level = models.PositiveIntegerField(default=1,null=True,blank=True)
    point = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.name

    @receiver(post_save, sender=User)
    def update_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    class Meta:
        ordering = ['level','-createDate']

# 주문번호 모델( 유저정보를 외래키로 가지고, 상품들이 이 모델을 외래키로 가진다 )
class DeliveryInfo(models.Model):
    pass

class BigCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    category = models.ForeignKey(BigCategory, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20)

    def __str__(self):
        return self.theme

    class Meta:
        ordering = ['category']

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productName = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='shoppingmall/%Y/%m/%d', blank=True)
    price = models.PositiveIntegerField()
    dcprice = models.PositiveIntegerField(null=True,blank=True)
    totalAmount = models.PositiveIntegerField()
    detail = models.TextField(blank=True)
    origin = models.CharField(max_length=50,null=True,blank=True)

    pubDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.category, self.productName)

    class Meta:
        ordering = ['category', '-pubDate']


class Comment(models.Model):
    author = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField()
    createAt = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.author, self.product)

    class Meta:
        ordering = ['-createAt']

class PurchaseNumber( models.Model ):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['number']

class Cart(models.Model):
    purchaseNumber = models.ForeignKey( PurchaseNumber, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.user, self.product)

    def plus_quantity(self):
        self.quantity += 1

    def minus_quantity(self):
        self.quantity -= 1

    class Meta:
        ordering = ['user']



class Purchase(models.Model):
    purchaseNumber = models.ForeignKey(PurchaseNumber, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()

    purchased_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.user, self.product)

    def plus_quantity(self):
        self.quantity += 1

    def minus_quantity(self):
        self.quantity -= 1

    def mod_state(self):
        self.state = True

    class Meta:
        ordering = ['purchased_date']


