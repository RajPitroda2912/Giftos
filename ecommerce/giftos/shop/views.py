from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings    
from .forms import *
from .models import *
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

# ------------- Home Func ---------------
def home(request):
    product =Product.objects.all()[:10:3]
    slider = Slider.objects.all()
    notification = AdminNotification.objects.all().order_by('-created_at')
    data = {
        'slider':slider,
        'product':product,
        'notification' : notification
    }
    return render(request,'home/index.html',data)

# ------------- Contact Func ---------------
def contact(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        contact_data = Contact(name=name,email=email,phone=phone,message=message)
        contact_data.save()
        send_mail(
            "Thank YOU",
            f"Dear {name},\n\nThank you for reaching out to us! We appreciate you taking the time to contact us and we are happy to help.\n\n Regards,\nGiftos",
            "raj.pitroda.lnxct@gmail.com",
            [email]
        )
        return redirect('shop:contactus')
    return render(request,'home/contact.html')

# ------------- Shoping Func ---------------
def shop(request):
    category = Category.objects.all()
    products = Product.objects.all()
   
    # Search
    if 'search' in request.GET:
        search = request.GET['search']
        products = Product.objects.filter(name__icontains=search) | Product.objects.filter(category__name__icontains=search)
    else:
        products = Product.objects.all()

    # Filter by category and price
    selected_categories = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if selected_categories:
        products = products.filter(category__id__in=selected_categories)
    
    if max_price == '20000':
        products = Product.objects.filter(price__gte=min_price)  # Only filter by min price if max price is 20000+
    else:   
        if min_price and max_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)
        elif min_price:
            products = products.filter(price__gte=min_price)
        elif max_price:
            products = products.filter(price__lte=max_price)

    context = {
        'category': category,
        'product': products,
    }
    return render(request,'home/shop.html',context)

# ------------- Testimonial Func ---------------
def testimonial(request):
    return render(request,'home/testimonial.html')


# ------------- Whyus Func ---------------
def why(request):
    return render(request,'home/why.html')

# ------------- Login Func ---------------
def Login(request):
    if request.method=='POST':
        form  = ReCaptcha(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            User = authenticate(email=email,password=password)
            if User is not None:
                login(request,User)
                messages.success(request,"User Login Successfully!")
                return redirect('/')
            else:
                # messages.error(request,"Email and Password is incorrect!")
                pass

    else:
        form = ReCaptcha()    
    return render(request,'login.html',{'form':form})

# ------------- Registration Func ---------------   
def signup(request):
    if request.method == 'POST':
        Register_form = RegisterUser(request.POST)
        if Register_form.is_valid():
            Register_form.save()
            return redirect('shop:login')
    else:
        Register_form = RegisterUser()
    return render(request,'signup.html', {'Register_form': Register_form})

# ------------- Logout Func ---------------
def Logout(request):
    logout(request)
    messages.success(request,"User Logout Successfully!")
    return redirect('/')

# ------------- Showing Cart  ---------------
def viewCart(request):
    if request.user.is_authenticated:
        # User is logged in, retrieve the cart from the database
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Merge session cart into user cart
        session_cart = request.session.get('cart', [])
        for item in session_cart:
            product = get_object_or_404(Product, id=item['product_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()
        request.session['cart'] = []  # Clear session cart after merging
    else:
        # User is not logged in, retrieve cart items from the session
        cart_items = request.session.get('cart', [])
        # Convert session cart items to objects for display
        cart_items = [
            {
                'product': get_object_or_404(Product, id=item['product_id']),
                'quantity': item['quantity']
            }
            for item in cart_items
        ]
    
    # Calculate total price
    if request.user.is_authenticated:
        total_price = sum(item.product.price * item.quantity for item in cart_items)
    else:
        total_price = sum(item['product'].price * item['quantity'] for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'home/cart.html', context)

# ------------- Adding cart ---------------
def addcart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        # User is logged in, use the database cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # User is not logged in, use the session cart
        cart = request.session.get('cart', [])
        if not isinstance(cart, list):
            cart = []

        for i, item in enumerate(cart):
            if item.get('product_id') == product_id:
                cart[i]['quantity'] += 1
                break
        else:
            cart.append({'product_id': product_id, 'quantity': 1})
        
        request.session['cart'] = cart
    return redirect('shop:cart')


# ------------- Removeing cart ---------------

def removecart(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
    else:
        cart = request.session.get('cart', [])
        cart = [item for item in cart if item['product_id'] != item_id]
        request.session['cart'] = cart
    return redirect('shop:cart')

def increment(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart = request.session.get('cart', [])
        for item in cart:
            if item['product_id'] == item_id:
                item['quantity'] += 1
                break
        request.session['cart'] = cart
    return redirect('shop:cart')

def decrement(request, item_id):
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        cart = request.session.get('cart', [])
        for item in cart:                                                     
            if item['product_id'] == item_id:                             
                if item['quantity'] > 1:
                    item['quantity'] -= 1
                else:
                    cart.remove(item)
                break
        request.session['cart'] = cart
    return redirect('shop:cart')

@login_required(login_url='shop:login')
def checkout(request):

    # Merge session cart into user cart after login
    session_cart = request.session.get('cart', [])
    if session_cart:
        cart, created = Cart.objects.get_or_create(user=request.user)
        for item in session_cart:
            product = get_object_or_404(Product, id=item['product_id'])
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()
        request.session['cart'] = []  # Clear session cart after merging

    user = request.user
    user_details = {
        'name': user.name,
        'phone': user.phone,
        'address': user.address,
        'email': user.email
    }

    # Retrieve cart items
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    amount = total_price * 100
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })
    order_id = payment['id']

    orders = None  

    if request.method == "POST":
        name = request.POST.get('name')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        address = request.POST.get('address')
        if address and city and pin and name:  
            orders = Order(
                user=user,
                name=name,
                email=email,
                phone=phone,
                locality=locality,
                city=city,
                pincode=pin,
                address=address,
                amount=total_price,
                payment_id=order_id
            )
            orders.save()
            user.address = address
            user.phone = phone
            user.save()

        for i in cart_items:
            item = OrderDetails(
                order = orders,
                product = i.product.name,
                image = i.product.image,
                quantity = i.quantity,
                price = i.product.price,
                total = i.quantity * i.product.price,
                status = 'Accepted'
            )
            item.save()    

    context = {
        'user_details': user_details,
        'cart_items': cart_items,
        'total_price': total_price,
        'order_id': order_id,
        'payment': payment,
        'amount' : amount,
        'order' : orders
    }
    return render(request, 'home/checkout.html', context)


@csrf_exempt
def thankyou(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        user = Order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.delete()
            
    return render(request, 'home/thank-you.html', {'order_id': order_id})

def profile(request):
    if request.method == 'POST':
        user = request.user
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.save()
        return redirect('shop:home')  
    
def order(request):
    orders = Order.objects.filter(user=request.user)
    order_details = OrderDetails.objects.filter(order__in=orders) 
    context = {
        'order_details': order_details,
        'order': orders
    }
    return render(request,'home/order.html',context)