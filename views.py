from django.shortcuts import render, reverse, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.views.generic import ListView, View
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

import json

from .models import Profile, Product, BigCategory, Category, Comment, Cart, Purchase, PurchaseNumber
from .forms import SignupForm, ProfileForm


'''
메인페이지, 모든 상품을 리스트로 출력하고 무한 스크롤로 표현한다
'''
def index( request ):
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    item_list = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, item_list.filter(category=x).count()])

    items = Product.objects.all().order_by('pubDate')
    page_obj = Paginator(items, 30)

    if request.is_ajax():
        page = request.GET.get('page')
        msg = True
        try:
            object_list = page_obj.page(page).object_list
        except PageNotAnInteger:
            redirect('shopping:index')
        except EmptyPage:
            msg = False
            object_list = page_obj.page(page_obj.num_pages).object_list

        object_list = list(object_list.values())
        context = {'object_list': object_list, 'msg': msg}

        return JsonResponse(context, encoder=DjangoJSONEncoder, safe=False)
    else:
        object_list = page_obj.page(1)
        return render(request, 'shoppingmall/index.html', {'menu': menu,
                                                          'itemList': itemList,
                                                          'products': object_list})
'''
navbar에 검색창이 존재, 이를 통해 검색어를 입력하면 
상품 이름에서 검색해서 일치하는 상품만 출력해준다
'''
def searchItem(request):
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    item_list = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, item_list.filter(category=x).count()])

    q = request.GET.get('queryWord','')
    if q:
        items = Product.objects.filter(productName__icontains=q).order_by('pubDate')
        if items:
            page_obj = Paginator(items, 30)

            if request.is_ajax():
                page = request.GET.get('page')
                msg = True
                try:
                    object_list = page_obj.page(page).object_list
                except PageNotAnInteger:
                    redirect('shopping:index')
                except EmptyPage:
                    msg = False
                    object_list = page_obj.page(page_obj.num_pages).object_list

                object_list = list(object_list.values())
                context = {'object_list': object_list, 'msg': msg}

                return JsonResponse(context, encoder=DjangoJSONEncoder, safe=False)
            else:
                object_list = page_obj.page(1)
                return render(request, 'shoppingmall/search.html', {'menu': menu,
                                                                   'itemList': itemList,
                                                                   'products': object_list})
        else:
            return render(request, 'shoppingmall/error.html', {'menu': menu,
                                                               'itemList': itemList,
                                                               'msg':'검색 결과가 존재하지 않습니다'})

    return render( request, 'shoppingmall/error.html', {'menu': menu,
                                                        'itemList': itemList,
                                                        'msg':'검색어를 입력하지 않았습니다'})
'''
회원가입
'''
class SignUp(View):
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.name = form.cleaned_data.get('name')
            user.profile.phoneNumber = form.cleaned_data.get('phoneNumber')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate( username=user.username, password=password)
            login(request, user)
            return redirect('shopping:update_profile')
        else:
            return render( request, 'shoppingmall/error.html', {'msg':request.POST})

    def get(self, request):
        form = SignupForm()
        return render( request, 'shoppingmall/signup.html', {'form':form})


'''
로그인 뷰
'''
def my_login( request ):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login( request, user )
                return redirect('shopping:shop_index')
            else:
                return render(request, 'shoppingmall/error.html', {'msg': 'Invalid ID or PW'})
        else:
            return render( request, 'shoppingmall/error.html', {'msg':'Invalid ID or PW'})

    else:

        if not request.user.is_anonymous:
            return redirect('shopping:shop_index')

        form = AuthenticationForm()
        return render( request, 'registration/login.html', {'form':form})

'''
회원정보 변경 중 패스워드 변경 뷰
'''
@login_required(login_url='shopping:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '성공적으로 패스워드를 변경 했습니다')
            return redirect('shopping:shop_index')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html',{'form':form})

'''
회원정보 변경 중 프로필 정보 수정 뷰
'''
@login_required(login_url='shopping:login')
def updateProfile( request ):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 성공적으로 저장했습니다.')
            return redirect('shopping:setting')
        else:
            messages.error(request, '실패했습니다')
    else:
        prof = Profile.objects.filter(user=request.user)
        form = ProfileForm( instance=request.user.profile)
    return render( request, 'registration/update_profile.html', {'form':form,
                                                                 'prof':prof[0]})
'''
회원정보를 보여주는 뷰
'''
@login_required(login_url='shopping:login')
def setting( request ):
    menu = BigCategory.objects.all()
    prof = Profile.objects.filter(user=request.user)
    items = Category.objects.all()
    products = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, products.filter(category=x).count()])

    return render( request, 'shoppingmall/setting.html', {'menu':menu,
                                                          'prof':prof[0],
                                                          'itemList':itemList,
                                                          'products':products})
'''
선택된 카테고리에 포함된 상품을 출력하는 뷰
'''
def productList( request, category ):
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    item_list = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, item_list.filter(category=x).count()])

    products = Product.objects.filter(category__theme=category)

    page_obj = Paginator(products, 12)

    if request.is_ajax():
        page = request.GET.get('page')
        msg = True
        try:
            object_list = page_obj.page(page).object_list
        except PageNotAnInteger:
            redirect('shopping:index')
        except EmptyPage:
            msg = False
            object_list = page_obj.page(page_obj.num_pages).object_list

        object_list = list(object_list.values())
        context = {'object_list': object_list, 'msg': msg}

        return JsonResponse(context, encoder=DjangoJSONEncoder, safe=False)
    else:
        object_list = page_obj.page(1)
        return render(request, 'shoppingmall/index.html', {'menu': menu,
                                                           'itemList': itemList,
                                                           'products': object_list})
'''
선택한 상품의 디테일 정보를 보여주는 뷰
'''
def itemDetail( request, pk ):
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    products = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, products.filter(category=x).count()])

    product = Product.objects.filter(pk=pk)

    return render( request, 'shoppingmall/item_detail.html', {'menu':menu,
                                                              'itemList':itemList,
                                                              'product':product[0]})

'''
상품을 카트에 추가
'''
@require_POST
def appendCart(request):
    if request.user.is_anonymous:
        msg = False
        context = {'msg':msg}
        return HttpResponse(json.dumps(context), content_type="application/json")
    user_pk = request.POST.get('user_pk')
    product_pk = request.POST.get('product_pk')
    quantity = request.POST.get('quantity')

    user = Profile.objects.filter(user__pk=user_pk)
    item = Product.objects.filter(pk=product_pk)

    if item[0].dcprice:
        total = item[0].dcprice * int(quantity)
    else:
        total = item[0].price * int(quantity)

    cart = Cart(user=user[0].user, product=item[0],quantity=quantity, total_price=total)
    cart.save()

    if cart:
        msg = True
    else:
        msg = False

    context = {'msg':msg}

    return HttpResponse(json.dumps(context), content_type="application/json")

'''
유저 별 카트 리스트를 보여주는 뷰
'''
@login_required(login_url='shopping:login')
def cartList(request):
    lists = Cart.objects.filter(user=request.user).filter(purchaseNumber=None)
    customer = Profile.objects.filter(user=request.user)
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    products = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, products.filter(category=x).count()])

    if lists:
        size = len(lists)
        return render(request,'shoppingmall/cart_list.html',{'lists':lists,
                                                             'customer':customer[0],
                                                             'size':size,
                                                             'menu':menu,
                                                             'itemList':itemList})
    else:
        msg = "카트에 아무것도 없습니다"
        return render( request, 'shoppingmall/error.html',{'msg':msg,
                                                           'customer': customer,
                                                           'menu':menu,
                                                           'itemList':itemList})
'''
카트 리스트에서 상품을 제거할 때
'''
@login_required(login_url='shopping:login')
def deleteItem(request):
    pk = request.POST.get('pk')
    upk = request.POST.get('upk')
    item = Cart.objects.filter(pk=pk)
    item.delete();

    item = Cart.objects.filter(pk=pk)
    lists = Cart.objects.filter(user__pk=upk)
    size = len(lists)

    if not item:
        msg = True
    else:
        msg = False

    context={'msg':msg, 'size':size}
    return HttpResponse(json.dumps(context), content_type='application/json')

'''
상품 디테일 뷰에서 구매를 클릭하면 구매 정보 페이지를 보여주는 뷰
'''
@require_POST
def purchase(request):
    if request.user.is_anonymous:
        context = {'msg':False}
        return HttpResponse(json.dumps(context), content_type="application/json")
    user_pk = request.POST.get('user_pk')
    product_pk = request.POST.get('product_pk')
    amount = request.POST.get('amount')

    user = Profile.objects.filter(user__pk=user_pk)
    item = Product.objects.filter(pk=product_pk)
    if item[0].dcprice:
        total = item[0].dcprice * int(amount)
    else:
        total = item[0].price * int(amount)

    buy = Purchase(user=user[0].user, product=item[0], quantity=amount,
                   total_price=total)
    buy.save()

    if buy:
        msg = True
    else:
        msg = False

    context = {'msg':msg, 'item_pk':buy.id}
    return HttpResponse(json.dumps(context),content_type="application/json")

'''
구매정보 뷰에서 구매를 확정하기 위한 뷰
'''
def purchaseConfirm(request, pk):
    item = Purchase.objects.filter(pk=pk)
    customer_info = Profile.objects.filter(user=request.user)
    print("item2:",item,"pk:",pk)
    menu = BigCategory.objects.all()
    items = Category.objects.all()
    products = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, products.filter(category=x).count()])

    return render( request, 'shoppingmall/purchase.html', {'item':item[0],
                                                           'customer':customer_info[0],
                                                           'menu': menu,
                                                           'itemList': itemList})
'''
구매 취소 뷰, 취소하면 이전 페이지(아이템디테일)로 돌아감
'''
def cancelPurchase( request, info_pk, item_pk ):
    info = Purchase.objects.filter(pk=info_pk)
    info.delete()
    return redirect('shopping:item_detail',item_pk)

from datetime import datetime

'''
구매 확정 뷰, 한가지 상품만 구매할 경우, purchase 모델에 주문번호 모델을 추가해준다
'''
@require_POST
def purchaseOne(request):
    pk = request.POST.get('pk')

    item = Purchase.objects.filter(pk=pk)
    customer = Profile.objects.filter(user=request.user)

    today = datetime.today()
    number = str(today.year)+str(today.month)+str(today.day)+str(today.hour)+str(today.minute)+\
        str(today.second)+str('-')+str(customer[0].pk)

    purNum = PurchaseNumber(user=customer[0].user, number=number)
    purNum.save()

    item.update(purchaseNumber=purNum)

    if item:
        msg = True
    else:
        msg = False

    context = {'msg':msg}

    return HttpResponse(json.dumps(context), content_type="apllication/json")

@require_POST
def purchaseCart(request):
    item = Cart.objects.filter(user=request.user).filter(purchaseNumber=None)
    customer = Profile.objects.filter(user=request.user)
    amount = len(item)

    today = datetime.today()
    number = str(today.year) + str(today.month) + str(today.day) + str(today.hour) + str(today.minute) + \
             str(today.second) + str('-') + str(customer[0].pk)

    purNum = PurchaseNumber(user=customer[0].user, number=number)
    purNum.save()


    item.update(purchaseNumber=purNum)
    msg = True

    context = {'msg':msg}

    return HttpResponse(json.dumps(context), content_type="apllication/json")



'''
구매한 상품 리스트를 보여주는 뷰
'''
@login_required(login_url='shopping:login')
def purchaseList(request):
    purNumList = PurchaseNumber.objects.filter(user=request.user)
    purList = []
    numDistinct = []

    for x in purNumList:
        tmp = Purchase.objects.filter(purchaseNumber=x).filter(user=request.user)
        if not tmp:
            tmp = Cart.objects.filter(purchaseNumber=x).filter(user=request.user)

        total_price = 0
        for each in tmp:
            total_price += each.total_price
        purList += tmp
        print(purList)
        numDistinct.append( [x.number,total_price] )


    menu = BigCategory.objects.all()
    items = Category.objects.all()
    products = Product.objects.all()
    itemList = []
    for x in items:
        itemList.append([x, products.filter(category=x).count()])

    return render(request, 'shoppingmall/purchase_list.html', {'purList':purList,
                                                               'numDistinct':numDistinct,
                                                               'total_price':total_price,
                                                               'menu': menu,
                                                               'itemList': itemList})




