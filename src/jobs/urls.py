from django.urls import include, path
from rest_framework.routers import DefaultRouter
from jobs.views import CategoryViewSet, JobViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]
