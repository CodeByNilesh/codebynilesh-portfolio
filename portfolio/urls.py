from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('certifications/', views.certifications, name='certifications'),  # NEW
    path('contact/', views.contact, name='contact'),
    path('fix-login/', views.fix_admin),  # TEMPORARY
]