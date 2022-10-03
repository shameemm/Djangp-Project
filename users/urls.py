from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login', views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('',views.index, name='index'),
    path('logout',views.logout, name='logout'),
    path('view_product',views.view_product, name='view_product'),
    path('otplogin',views.otplogin, name='otplogin'),
    path('getotp',views.getotp, name='getotp'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('cart',views.cart,name='cart'),
    path('minus',views.minus,name='minus'),
    path('up',views.up,name='up'),
    path('checkout',views.checkout,name='checkout'),
    path('payment',views.payment,name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)