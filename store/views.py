from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Project
from django.contrib.auth.models import User
from .forms import ProfileForm,ProjectForm

# Create your views here.
def home(request):
    title="Kennedy's Empire"
    
    posts=Project.objects.all()
    return render(request,'index.html',{"posts":posts})


@login_required(login_url='/accounts/login/')  
def create_profile(request):
    current_user = request.user
    if request.method=="POST":
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile =form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect(home)
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html',{"form":form})

@login_required(login_url='/accounts/login/')  
def profile(request,id): 
    try: 
        current_user = request.user
        profile = Profile.objects.filter(user_id=id).all()
        projects = Project.objects.filter(profile_id=current_user.profile.id).all()
        return render(request, 'profile.html', {"profile":profile, "projects":projects}) 
    except User.profile.RelatedObjectDoesNotExist:
        return redirect(create_profile)
    
def edit_profile(request):
    '''
    Edits profile picture and bio
    '''
    current_user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_pic = form.cleaned_data['profile_pic']
            bio  = form.cleaned_data['bio']

            updated_profile = Profile.objects.get(user= current_user)
            updated_profile.profile_pic = profile_pic
            updated_profile.bio = bio
            updated_profile.save()
        return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'edit_profile.html', {"form": form})

@login_required(login_url='/accounts/login/')  
def new_post(request):
    current_user = request.user
    if request.method=='POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = current_user.profile
            project.save()
            return redirect(home)
    else:
        form = ProjectForm()
    return render(request, 'newpost.html',{"form":form})





