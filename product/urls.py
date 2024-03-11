from django.urls import path, include
from product import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'Product', views.ProductViewSet, basename='product')
# router.register(r'Calculate',views.CalculateAPI)

urlpatterns = [
    path('', include(router.urls)),
    path('calculation/', views.MyApiView.as_view())

]
