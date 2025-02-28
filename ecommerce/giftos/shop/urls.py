from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('',home,name='home'),
    path('shop/',shop,name='shop'),
    path('contactus/',contact,name='contactus'),
    path('testimonial/',testimonial,name='testimonial'),
    path('why/',why,name='why'),
    path('login/',Login,name='login'),
    path('signup/',signup,name='signup'),
    path('logout',Logout,name='logout'),

]
