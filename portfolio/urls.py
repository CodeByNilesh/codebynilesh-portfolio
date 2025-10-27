from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('certifications/', views.certifications, name='certifications'),
    path('contact/', views.contact, name='contact'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # TEMPORARY - DELETE AFTER USE
    path('setup-admin-now/', views.setup_admin, name='setup_admin'),
]