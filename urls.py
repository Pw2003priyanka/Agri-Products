"""
URL configuration for Agriproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Agriapp.views import productview,agriagencyview,productdetail,product,deleteproduct,detailproduct
from Agriapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',agriagencyview.as_view(),name="index"),
    path('productview/',productview.as_view(), name="productview"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('agrilogin/',views.agrilogin,name="agrilogin"),
    path('agriregister/',views.agriregister,name="agriregister"),
    path('productdetail/<int:pk>',productdetail.as_view(),name="productdetail"),
    path('search/',views.search,name="search"),
    path('addtocart/',views.addtocart,name="addtocart"),
    path('viewcart/',views.viewcart,name="viewcart"),
    # path('removepacakge/', views.removepacakge, name='removepacakge'),
    path('summarypage',views.summary,name='summary'),
    path('placeorder/',views.placeorder, name="placeorder"),
    path('success',views.success,name='success'),
    path('payment/',views.payment,name="payment"),
    path('logout/',views.logout,name="logout"),
    path('agriagencynavbar/',views.agriagencynavbar,name='agriagencynavbar'),
    path('profile/',views.agriagencyprofile,name='profile'),
    path('agrieditprofile/',views.agrieditprofile,name='agrieditprofile'), 
    path('addproduct',views.addproduct,name='addproduct'),
    path('viewproduct/',views.viewproduct,name='viewproduct'),
     path('deleteproduct/<int:pk>',deleteproduct.as_view(),name='deleteproduct'),
    path('editproduct/<int:pk>',views.editproduct,name='editproduct'),
    path('agriagencylogout',views.agriagencylogout,name='agriagencylogout'),
    path('my_order/', views.my_order, name='my_order'),
    path('changequantity',views.cq,name='changequantity'),
    path('about/',views.About,name='about/'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

