from django.urls import path
from . import views

urlpatterns=[
    path('',views.all_user,name='all_user'),
    path('dashboard/',views.chart_view,name='Home'),
    path('region/', views.region, name="region")
]
