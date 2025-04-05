from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('contactus/', contact, name='contactus'),
    path('testimonial/', testimonial, name='testimonial'),
    path('why/', why, name='why'),
    path('login/', Login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout', Logout, name='logout'),
    path('cart/', viewCart, name='cart'),
    path('addcart/<int:product_id>/', addcart, name='addcart'),
    path('removecart/<int:item_id>/', removecart, name='removecart'),
    path('increment/<int:item_id>/', increment, name='increment'),
    path('decrement/<int:item_id>/', decrement, name='decrement'),
    path('cart/checkout/', checkout, name='checkout'),
    path('cart/checkout/thankyou', thankyou, name='thankyou'),
    path('profile/', profile, name='profile'),

    


]