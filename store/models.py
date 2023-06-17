from django.db import models

from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    '''
    profile class to define profile objects
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to = 'images/')
    profile_pic = CloudinaryField('image')
    bio=models.CharField(max_length = 100)
    contacts=models.CharField(max_length = 100,default='SOME STRING')

    def __str__(self):
        return self.user

    def save_profile(self):
        self.save()

    def delete_profile(self):
        '''
        method that deletes post from database
        '''
        self.delete()    

    @classmethod
    def search_by_name(cls,search_term):
        '''
        method that rerieves a user by use of username
        '''
        name = cls.objects.filter(user__username__icontains = search_term)
        return name
    

class Project(models.Model):
    '''
    project class to define project objects
    '''
    image=models.ImageField(upload_to = 'images/')
    image = CloudinaryField('image')
    title=models.CharField(max_length = 100)
    description=models.CharField(max_length = 100)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    

    

    def save_project(self):
        '''
        method to save object to database
        '''
        self.save()

    def delete_project(self):
        '''
        method to delete object from database
        '''
        self.delete()   

    @classmethod
    def get_project_by_id(cls,project_id):
        projects=cls.objects.get(id=project_id)
        return projects     


    @classmethod
    def search_by_title(cls,search_term):
        '''
        method that retrieves a project by use of its title
        '''  
        projects = cls.objects.filter(title__icontains=search_term)
        return projects 
    
class Review(models.Model):
    '''
    review class to define review objects
    '''
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    project_id=models.ForeignKey(Project,on_delete=models.CASCADE,null=True)
    comment=models.TextField(blank=True)
    availability=models.PositiveIntegerField()
    ratings=models.PositiveIntegerField(null=True)   