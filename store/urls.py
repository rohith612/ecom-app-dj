from django.urls import path
from . import views

urlpatterns = [

    # page navigation urls
    path('', views.home_page, name="home_page"),
    path('product/', views.store_page, name='store_page'),

    path('cart/', views.cart_page, name='cart_page'),
    path('checkout/', views.checkout_page, name='checkout_page'),

    # user authentication urls
    path('login/', views.login_page, name="login_page"),
    path('signup/', views.signup, name="signup_page"),
    path('profile/', views.profile, name="profile_page"),
    path('logout/', views.logout_page, name="logout_page"),

    # ajax requests urls
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.process_order, name="process_order"),

    path('<slug:slug>/', views.product_details, name='product_details'),
]
