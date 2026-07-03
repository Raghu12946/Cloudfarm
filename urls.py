from django.urls import path
from . import views
from .views import prediction 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('predict/', views.prediction, name="prediction"),
    path('fertilizers/', views.fertilizer_list, name='fertilizer_list'),
    path('fertilizers/<int:pk>/', views.fertilizer_detail, name='fertilizer_detail'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('home/', views.home, name='home'),  # Home page
    path('fertilizer_list/', views.fertilizer_list, name='fertilizer_list'),  # Fertilizer list page
    path('aboutus/', views.about_us, name='Aboutus'), 
    path('logout/', views.logout_view, name='logout'),
    path('buy-products/', views.buy_products, name='buy_products'),
    path('bill/', views.bill, name='bill'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<str:product_name>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('payment/', views.payment, name='payment'),
    # path('process_payment/', views.process_payment, name='process_payment'),
    path('help/', views.help, name='help'),
    # path('process_payment/', process_payment, name='process_payment'),
    path('croptable/', views.croptable, name='croptable'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

