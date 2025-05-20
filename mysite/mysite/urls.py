from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from polls.api_views import QuestionViewset, ChoiceViewset, AdminQuestionViewset, AdminChoiceViewset

router = routers.SimpleRouter()
router.register('question', QuestionViewset, basename='question')
router.register('choice', ChoiceViewset, basename='choice')
router.register('admin/question', AdminQuestionViewset, basename='admin-question')
router.register('admin/choice', AdminChoiceViewset, basename='admin-choice')

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
] + debug_toolbar_urls()
