from django.conf.urls import url
from django.contrib.auth import views as auth_view


from . import views

app_name='shopping'

urlpatterns = [
    url(r'^$', views.index, name='shop_index'),

    url(r'^signup/$', views.SignUp.as_view(), name='signup'),
    url(r'^login/$', views.my_login, name='login'),
    url(r'^logout/$',auth_view.logout, {'next_page':'shopping:shop_index'}, name='logout'),

    url(r'^setting/$', views.setting, name='setting'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^profile/update/$', views.updateProfile, name='update_profile'),

    url(r'^product/(?P<category>\w+)/$', views.productList, name='products_list'),
    url(r'^product/detail/(?P<pk>\d+)/$', views.itemDetail, name='item_detail'),

    url(r'^cart/$', views.appendCart, name='appendCart'),
    url(r'^cartList/$',views.cartList, name='cartlist'),
    url(r'^cartitem/delete/$', views.deleteItem, name="delete_item"),

    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^purchaseConfirm/(?P<pk>\d+)/$',views.purchaseConfirm, name='purchase_confirm'),

    url(r'search/$', views.searchItem, name='searchItem'),

    url(r'cancel/(?P<info_pk>\d+)/(?P<item_pk>\d+)/$', views.cancelPurchase, name="cancelPurchase"),

    url(r'purchase_one/$', views.purchaseOne, name="purchase_one"),
    url(r'^purchase_cart/$',views.purchaseCart, name="purchase_cart"),

    url(r'^purchase_list/$', views.purchaseList, name='purchase_list'),

]


