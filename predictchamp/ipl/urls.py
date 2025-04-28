from django.urls import path
from . import views

urlpatterns = [
    path('',views.predict,name='predict_view'),
    path('update/<str:win>/<str:loss>/<int:no>/<int:tie>/', views.updatetb, name='updatetb_view'),
    path('reset/',views.reset,name='reset_view'),
    path('matchreset/<int:mno>/',views.matchreset,name='matchreset_view'),
    path('playoff/',views.playoff_v,name='playoff_view'),
    path('updateplaytb/<str:win>/<str:loss>/', views.updateplaytb, name='updateplaytb_view'),
    path('playreset/',views.playreset,name='playreset_view'),
]