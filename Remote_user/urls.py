from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('Register1/', views.Register1, name='Register1'),
    path('ViewYourProfile/', views.ViewYourProfile, name='ViewYourProfile'),
    path('Predict_Attack_Type_Prediction/', views.Predict_Attack_Type_Prediction, name='Predict_Attack_Type_Prediction'),
]