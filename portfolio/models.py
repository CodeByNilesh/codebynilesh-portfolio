from django.db import models
from django.utils.text import slugify

class About(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='profile/')
    resume = models.FileField(upload_to='resume/', blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "About"

class Skill(models.Model):
    SKILL_LEVEL = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=20, choices=SKILL_LEVEL)
    percentage = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    technologies = models.CharField(max_length=200, help_text="Comma-separated technologies")
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-start_date']

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.degree} - {self.institution}"
    
    class Meta:
        ordering = ['-start_date']

class SocialLink(models.Model):
    PLATFORM_CHOICES = (
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.platform

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class Certification(models.Model):
    CERTIFICATION_TYPE = (
        ('course', 'Online Course'),
        ('certification', 'Professional Certification'),
        ('award', 'Award'),
        ('achievement', 'Achievement'),
    )
    
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    certification_type = models.CharField(max_length=20, choices=CERTIFICATION_TYPE, default='certification')
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    certificate_image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"