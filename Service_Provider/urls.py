from django.urls import path
from . import views

urlpatterns = [
    path('serviceproviderlogin/', views.serviceproviderlogin, name='serviceproviderlogin'),
    path('View_Remote_Users/', views.View_Remote_Users, name='View_Remote_Users'),
    path('View_Prediction_Of_Attacker_Type/', views.View_Prediction_Of_Attacker_Type, name='View_Prediction_Of_Attacker_Type'),
    path('View_Prediction_Of_Attacker_Type_Ratio/', views.View_Prediction_Of_Attacker_Type_Ratio, name='View_Prediction_Of_Attacker_Type_Ratio'),
    path('Download_Predicted_DataSets/', views.Download_Predicted_DataSets, name='Download_Predicted_DataSets'),
]