from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# login required for func based views
from django.contrib.auth.decorators import login_required
# login required for class based views
from django.utils.decorators import method_decorator


class Productview(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='B')
        mobiles = Product.objects.filter(category='M')
        # to see items count in cart icon
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html', {'topwears': topwears, 'bottomwears': bottomwears, 'mobiles': mobiles, 'totalitem': totalitem})


class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        # to check if that item already exist in cart or not,so if he already have in cart then we can show him go to cart rather then add to cart
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        # to see items count in cart icon
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    user = request.user
    # to catch the id of the product so that we can add the product of that id to cart.
    product_id = request.GET.get('prod_id')
    # print(product_id) #just for debugging to see that we getting the id of product here or not
    # here we matching that id of product that we catch using product_id variable from above line,
    product = Product.objects.get(id=product_id)
    # here we don't really need to catch and then pass the quantity of product also i.e as we catch and pass other values like user and product field of our cart table, because by default quantity will be 1 on first save
    Cart(user=user, product=product).save()
    # return render(request, 'app/addtocart.html') now this way we'll be able to show the cart detail that we catched and save above in Cart table by passing if we pass dict obj of save cart and reference to our templatet..but..its better to show the catched data of cart through a new func like 'show_cart' thats why here we just simply redirect it rather then passing data to our addtocart template here,,,see
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        # below line we getting cart data of the logged in user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0  # 0.0 because we setted our price field in float form.
        shipping_amount = 70.0
        total_amount = 0.0
        # adding our cart amount using list comprehenssion python.
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        # means if there is any product in cart(or if card is not empty),,
        if cart_product:
            for p in cart_product:
                # means if we have 2 products of 200 then it means 200*2=400,,this is the amount for a single product,
                tempamount = (p.quantity * p.product.descounted_price)
                # now we going to add the amount of all products from above tempamount var,because above is for the amount of a single product.total amount without shipping amount
                amount += tempamount
                # with shipping amount
                totalamount = amount + shipping_amount
        # to see items count in cart on navbar
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html')


# for plus
@login_required
def plus_cart(request):
    if request.method == 'GET':
        # we catching this prod_id through our ajax func here(because in our template ajax is injected).
        prod_id = request.GET['prod_id']
        # after getting prod_id,now below we checking for if the product id(we get throgh ajax) of that cart is mathced with logged in user
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # increasing quantities on clicking +
        c.quantity += 1
        # saving increased quantities
        c.save()
        # now because quantities increase we need to increase prices as well,so we just use the almost same calculation code here that we used in above func
        amount = 0.0  # 0.0 because we setted our price field in float form.
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.descounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount
            # put catched data to var 'data' to return that data to our js file through json response from this var 'data' we created here.
            # totalamount = amount
        # we indent back because this is not part of our for loop
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        # return our data to our js file by creating json response
        return JsonResponse(data)


# for minus
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # decreasing quantities on clicking -
        c.quantity -= 1
        # saving decreased quantities
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.descounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount : commentented because it assumed to be better to add this amount while passing our json object to our js file so we can see better results as live..so its a good thing to add in our json so we can see live effects on page..
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


# for remove
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # deleting quantities
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==
                        request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.descounted_price)
            amount += tempamount
            # totalamount = amount + shipping_amount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@login_required
def address(request):
    addr = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addr': addr, 'active': 'btn-primary'})


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})


# filter for mobile
def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'redmi' or data == 'samsung' or data == 'iphone':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(descounted_price__lt=100000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(descounted_price__gt=100000)
    # to see items count in cart on navbar
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


# filter for topwear
def topwear(request, data=None):
    if data == None:
        topwear = Product.objects.filter(category='TW')
    elif data == 'khaadi' or data == 'levis' or data == "levi's":
        topwear = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(
            category='TW').filter(descounted_price__lt=5000)
    elif data == 'above':
        topwear = Product.objects.filter(
            category='TW').filter(descounted_price__gt=5000)
    # to see items count in cart on navbar
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html', {'topwear': topwear, 'totalitem': totalitem})

# filter for bottomwear


def bottomwear(request, data=None):
    if data == None:
        bottomwear = Product.objects.filter(category='B')
    elif data == 'full-count' or data == 'levis' or data == 'iron-heat':
        bottomwear = Product.objects.filter(category='B').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(
            category='B').filter(descounted_price__lt=3000)
    elif data == 'above':
        bottomwear = Product.objects.filter(
            category='B').filter(descounted_price__gt=3000)

    # to see items count in cart on navbar
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwear, 'totalitem': totalitem})


# def login(request):
#     return render(request, 'app/login.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'congratulations!! Register Successfully')
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})

# on checkout page to show customer detail like addres and also show calculated order summary on that page.


@login_required
def checkout(request):
    user = request.user
    # for checkout page,getting addr of user from Customer table(model)
    addr = Customer.objects.filter(user=user)
    # for checkout page,getting cart inf of that user from Cart table(model)
    cart_items = Cart.objects.filter(user=user)
    # for amount
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    # if cart have products then do this
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.descounted_price)
            amount += tempamount
        # total amount should be outside of loop,here we don't need to use ajax because on this page we no longer need to show live results
        totalamount = amount + shipping_amount

    # to see items count in cart on navbar
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'addr': addr, 'totalamount': totalamount, 'cart_items': cart_items})

# for payment done after checkout,


@login_required
def payment_done(request):
    user = request.user
    # catching customer/user id from selected radio box address from our webpage which we define in our input field of checkout page..
    custid = request.GET.get('custid')
    # catch the id of customer from our radio box(in which we define attr name and value as custid) and match it with the id of that customer from our Customer table.
    customer = Customer.objects.get(id=custid)
    # to save the instructions provided by user in "Orderplaced" table from Cart of Customer and then delete the cart of user
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer,
                    product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        # to see items count in cart on navbar
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, 'Congratulations!! Profile Updated Successfully')
        # to see items count in cart on navbar
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
