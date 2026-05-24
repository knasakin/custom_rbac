from django.urls import path
from rest_framework.routers import DefaultRouter
from access import views


router = DefaultRouter()
router.register('access-rules', views.AccessRuleViewSet, basename='access-rules')

urlpatterns = [
    path('products/', views.ProductsAPIView.as_view(), name='products'),
    path('orders/', views.OrdersAPIView.as_view(), name='orders'),
]

urlpatterns += router.urls
