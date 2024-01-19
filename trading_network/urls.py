from django.urls import path
from rest_framework.routers import DefaultRouter

from trading_network import views
from trading_network.apps import TradingNetworkConfig
from trading_network.views import ContactViewSet, ProductViewSet

app_name = TradingNetworkConfig.name

router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('link/<int:pk>/', views.LinkRetrieveAPIView.as_view(), name='link'),
    path('link/', views.LinkListAPIView.as_view(), name='link_list'),
    path('link/create/', views.LinkCreateAPIView.as_view(), name='link_create'),
    path('link/<int:pk>/update/', views.LinkUpdateAPIView.as_view(), name='link_update'),
    path('link/<int:pk>/delete/', views.LinkDestroyAPIView.as_view(), name='link_delete'),
] + router.urls
