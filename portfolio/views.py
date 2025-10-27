from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import About, Skill, Project, Experience, Education, SocialLink, Contact, Certification
from .forms import ContactForm

def home(request):
    about = About.objects.first()
    skills = Skill.objects.all()[:8]
    projects = Project.objects.filter(featured=True)[:6]
    experiences = Experience.objects.all()[:3]
    social_links = SocialLink.objects.all()
    
    context = {
        'about': about,
        'skills': skills,
        'projects': projects,
        'experiences': experiences,
        'social_links': social_links,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    about_info = About.objects.first()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    social_links = SocialLink.objects.all()
    
    context = {
        'about': about_info,
        'skills': skills,
        'experiences': experiences,
        'education': education,
        'social_links': social_links,
    }
    return render(request, 'portfolio/about.html', context)

def projects(request):
    all_projects = Project.objects.all()
    social_links = SocialLink.objects.all()
    
    context = {
        'projects': all_projects,
        'social_links': social_links,
    }
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    # Exclude current project by slug
    related_projects = Project.objects.exclude(slug=slug)[:3]
    social_links = SocialLink.objects.all()
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'social_links': social_links,
    }
    return render(request, 'portfolio/project_detail.html', context)

def certifications(request):
    certs = Certification.objects.all()
    social_links = SocialLink.objects.all()
    
    # Filter by type if provided
    cert_type = request.GET.get('type')
    if cert_type:
        certs = certs.filter(certification_type=cert_type)
    
    context = {
        'certifications': certs,
        'selected_type': cert_type,
        'social_links': social_links,
    }
    return render(request, 'portfolio/certifications.html', context)

def contact(request):
    social_links = SocialLink.objects.all()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    about_info = About.objects.first()
    
    context = {
        'form': form,
        'about': about_info,
        'social_links': social_links,
    }
    return render(request, 'portfolio/contact.html', context)


# TEMPORARY - DELETE AFTER USE
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_first_admin(request):
    username = 'admin'
    password = 'Admin@2024'
    email = 'admin@example.com'
    
    # Check if any superuser exists
    if User.objects.filter(is_superuser=True).exists():
        existing = User.objects.filter(is_superuser=True).first()
        return HttpResponse(f'''
            <h2>✅ Admin already exists!</h2>
            <p>Username: <code>{existing.username}</code></p>
            <p>If you forgot the password, delete this user in Railway shell and visit this page again.</p>
            <a href="/admin/">Go to Admin</a>
            <hr>
            <p style="color:red;">⚠️ DELETE this view from code!</p>
        ''')
    
    # Create admin
    User.objects.create_superuser(username, email, password)
    
    return HttpResponse(f'''
        <h2>🎉 Admin Created Successfully!</h2>
        <p><strong>Username:</strong> <code>{username}</code></p>
        <p><strong>Password:</strong> <code>{password}</code></p>
        <br>
        <a href="/admin/" style="background:#4CAF50;color:white;padding:15px 30px;text-decoration:none;border-radius:5px;font-size:18px;">
            Login to Admin Panel
        </a>
        <hr>
        <h3 style="color:red;">⚠️ IMPORTANT SECURITY:</h3>
        <ol>
            <li>Login and change your password immediately</li>
            <li>Delete this <code>create_first_admin</code> function from views.py</li>
            <li>Delete the URL from urls.py</li>
            <li>Push to GitHub</li>
        </ol>
    ''')