from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from . import views


urlpatterns = [
    path('register/tuteur/', views.registerTuteur, name='registerTuteur'),
    path('register/professeur/', views.registerProfesseur, name='registerProfesseur'),
    path('register/eleve/', views.registerEleve, name='registerEleve'),
    path('users/login/', views.MyTokenObtainPairViews.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tuteurs/', views.tuteurs, name='tuteurs'),
    path('tuteurExiste/<str:username>/<str:password>', views.tuteurExiste, name='tuteurExiste'),
    path('tuteurs/<str:pk>', views.tuteurs, name='tuteurs'),
    path('professeurs/', views.professeurs, name='professeurs'),
    path('professeurs/<str:pk>', views.professeurs, name='professeurs'),
    path('eleves/', views.eleves, name='eleves'),
    path('eleves/<str:pk>', views.eleves, name='eleves'),
]
