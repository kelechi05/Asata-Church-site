from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('our-history/', views.our_history, name='our_history'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('clergies/', views.clergies, name='clergies'),
    path('church-families/', views.church_families, name='church_families'),
    path('contact/', views.contact, name='contact'),
    path('preachers-desk/', views.preachers_desk, name='preachers_desk'),
    path('preachers-desk/<int:pk>/<slug:slug>/', views.preachers_desk, name='preachers_desk_detail'),
    path('departments/<slug:slug>/', views.department_detail, name='department_detail'),
]
