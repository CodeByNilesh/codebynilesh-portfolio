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


# EMERGENCY DEBUG - DELETE AFTER USE
from django.http import HttpResponse
from django.contrib.auth.models import User

def reset_admin_now(request):
    """Debug and fix admin - DELETE THIS AFTER USE!"""
    
    # Get ALL users with details
    all_users = User.objects.all()
    user_details = []
    
    for u in all_users:
        user_details.append(f"""
            <div style='background: #f0f0f0; padding: 10px; margin: 10px 0; border-left: 4px solid {"#4CAF50" if u.is_superuser else "#ff5722"}; border-radius: 5px;'>
                <strong>Username:</strong> {u.username}<br>
                <strong>Email:</strong> {u.email}<br>
                <strong>Is Superuser:</strong> {"✅ YES" if u.is_superuser else "❌ NO"}<br>
                <strong>Is Staff:</strong> {"✅ YES" if u.is_staff else "❌ NO"}<br>
                <strong>Is Active:</strong> {"✅ YES" if u.is_active else "❌ NO"}
            </div>
        """)
    
    user_list_html = ''.join(user_details) if user_details else '<p>❌ NO USERS FOUND!</p>'
    
    # Create GUARANTEED working admin
    new_user = 'workingadmin'
    new_pass = 'Working@123'
    
    # Delete if exists
    User.objects.filter(username=new_user).delete()
    
    # Create fresh superuser
    User.objects.create_superuser(new_user, 'working@example.com', new_pass)
    
    return HttpResponse(f'''
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }}
                h2 {{ color: #4CAF50; }}
                .box {{ padding: 20px; margin: 20px 0; border-radius: 5px; }}
                .success {{ background: #d4edda; border-left: 4px solid #28a745; }}
                .info {{ background: #d1ecf1; border-left: 4px solid #17a2b8; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
                .credentials {{ background: #e7f3ff; padding: 20px; border-left: 4px solid #2196F3; font-size: 20px; font-weight: bold; }}
                .btn {{ display: inline-block; background: #4CAF50; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-size: 20px; font-weight: bold; }}
                code {{ background: #f4f4f4; padding: 3px 8px; border-radius: 3px; color: #e83e8c; font-size: 18px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🔍 DATABASE DEBUG INFO</h2>
                
                <div class="box info">
                    <h3>👥 All Users in Database:</h3>
                    {user_list_html}
                    <p><strong>Total Users:</strong> {all_users.count()}</p>
                </div>
                
                <div class="box success">
                    <h3>✅ NEW WORKING ADMIN CREATED!</h3>
                </div>
                
                <div class="credentials">
                    <p>👤 Username: <code>{new_user}</code></p>
                    <p>🔑 Password: <code>{new_pass}</code></p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="/admin/" class="btn">🚀 LOGIN NOW</a>
                </div>
                
                <div class="box warning">
                    <h3>📝 COPY THESE CREDENTIALS:</h3>
                    <p>Username: {new_user}</p>
                    <p>Password: {new_pass}</p>
                    <p><strong>⚠️ Type them EXACTLY as shown above!</strong></p>
                </div>
                
                <div class="box info">
                    <h3>🔐 After Logging In:</h3>
                    <ol>
                        <li>Click "WELCOME, WORKINGADMIN" (top right)</li>
                        <li>Click "Change password"</li>
                        <li>Set NEW password</li>
                        <li><strong>DO NOT go to Users → Don't edit username!</strong></li>
                        <li>Delete this code from views.py and urls.py</li>
                        <li>Push to GitHub</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
    ''')