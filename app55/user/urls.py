from django.urls import path
from.import views

urlpatterns = [
    path('',views.userhome),
    path('funds/',views.funds),
    path('payment/',views.payment),
    path('success/',views.success),
    path('cancel/',views.cancel),
    path('viewfunds/',views.viewfunds),
    path('cpuser/',views.cpuser),
    path('epuser/',views.epuser),
    path('add_to_cart/<int:prodid>/', views.add_to_cart),
    path('remove_from_cart/<int:prodid>/', views.remove_from_cart),
    path('cart/', views.view_cart),
    path('checkout/', views.create_checkout_session)
]
