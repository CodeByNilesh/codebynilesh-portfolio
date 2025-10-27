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


# EMERGENCY FIX - DELETE AFTER USE
from django.http import HttpResponse
from django.contrib.auth.models import User

def reset_admin_now(request):
    """Creates fresh admin - DELETE THIS AFTER USE!"""
    
    # Show all existing users for debugging
    all_users = User.objects.all()
    user_list = '<br>'.join([f"- {u.username} (superuser: {u.is_superuser})" for u in all_users])
    
    # Create new admin
    new_username = 'finaladmin'
    new_password = 'FinalPass@123'
    new_email = 'final@example.com'
    
    # Delete if exists
    User.objects.filter(username=new_username).delete()
    
    # Create fresh
    User.objects.create_superuser(new_username, new_email, new_password)
    
    return HttpResponse(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h2 {{ color: #4CAF50; }}
                .success {{ background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .info {{ background: #d1ecf1; border: 1px solid #bee5eb; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .credentials {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0; font-size: 18px; }}
                .btn {{ display: inline-block; background: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-size: 18px; margin: 10px 5px; }}
                .btn:hover {{ background: #45a049; }}
                code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>✅ Fresh Admin User Created!</h2>
                
                <div class="success">
                    <p><strong>A brand new admin account has been created successfully!</strong></p>
                </div>
                
                <div class="credentials">
                    <p><strong>👤 Username:</strong> <code>{new_username}</code></p>
                    <p><strong>🔑 Password:</strong> <code>{new_password}</code></p>
                </div>
                
                <a href="/admin/" class="btn">🚀 Go to Admin Panel</a>
                
                <div class="info">
                    <p><strong>Existing users in database:</strong></p>
                    <p>{user_list if user_list else "No users found"}</p>
                </div>
                
                <div class="warning">
                    <p><strong>⚠️ AFTER SUCCESSFUL LOGIN:</strong></p>
                    <ol>
                        <li>Change your password (top right corner)</li>
                        <li><strong>DO NOT change username!</strong></li>
                        <li>Delete this <code>reset_admin_now</code> function from views.py</li>
                        <li>Delete the URL from urls.py</li>
                        <li>Push to GitHub</li>
                    </ol>
                </div>
                
                <div class="info">
                    <p><strong>📝 Instructions:</strong></p>
                    <ol>
                        <li>Click "Go to Admin Panel" button above</li>
                        <li>Enter username: <code>{new_username}</code></li>
                        <li>Enter password: <code>{new_password}</code></li>
                        <li>Click "Log in"</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
    ''')