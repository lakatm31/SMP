from django.urls import path
from . import views

urlpatterns = [
    path('', views.simulation, name='simulation'),
    #path('simulation-dms/', views.simulation_dms, name='simulation_dms'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]