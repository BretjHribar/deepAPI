from django.conf.urls import url, include
from rest_framework import routers
from DeepAPIproj.DeepAPIapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'imageclassify', views.ImageClassifyView, base_name="ImageClassifyView")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^imageclassify/', views.ImageClassifyView.as_view() )
]
