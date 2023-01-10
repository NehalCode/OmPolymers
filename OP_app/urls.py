from django.urls import path
from OP_app import views

urlpatterns = [
 path('',views.index,name="index"),
 path('contact/',views.contact,name="contact"),

# register 
 path('signup/',views.signup,name="signup"),
 path('otp_verification/',views.otp_verification,name="otp_verification"),
 path('login/',views.login,name="login"),
 path('logout/',views.logout,name="logout"),

 path('shop/',views.shop,name="shop"),
 path('cat_filter/<int:pk>/',views.cat_filter,name="cat_filter"),
 path('cart/',views.cart,name="cart"),
 path('add_to_cart/<int:pk>/',views.add_to_cart,name="add_to_cart"),
 path('remove_product/<int:pk>/',views.remove_product,name="remove_product"),

 path('single_product/<int:pk>/',views.single_product,name="single_product"),
 path('about/',views.about,name="about"),
 path('wishlist/',views.wishlist,name="wishlist"),
 path('remove_wishlist/<int:pk>/',views.remove_wishlist,name="remove_wishlist"),

 
]
