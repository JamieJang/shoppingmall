from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Product, BigCategory, Category, Comment, Cart, Purchase, PurchaseNumber

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self,request,obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin,self).get_inline_instances(request,obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('category','productName','price','dcprice','totalAmount','pubDate','pk')
    list_per_page = 20
    list_filter = ['category','pubDate','price']

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('theme','category','pk')
    list_per_page = 20
    list_filter = ['category', 'theme']

admin.site.register(BigCategory)
admin.site.register(Comment)

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('user','purchaseNumber','product','quantity','created_at')
    list_per_page = 30
    list_filter = ['user','created_at']

@admin.register(Purchase)
class AdminPurchase(admin.ModelAdmin):
    list_display = ('user','purchaseNumber','product','quantity','purchased_date','pk')
    list_per_page = 30
    list_filter = ['user','purchased_date']

@admin.register(PurchaseNumber)
class AdminPurchaseNumber(admin.ModelAdmin):
    list_display=['user','number','complete']
    list_per_page=30
    list_filter=['user','number','complete']