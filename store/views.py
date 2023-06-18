from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Project,Review
from django.contrib.auth.models import User
from .forms import ProfileForm,ProjectForm,ReviewForm
from django.http import HttpResponseRedirect
from django.http  import HttpResponse,Http404,HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer

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

@login_required(login_url='/accounts/login/')  
def single_post(request, id):
    current_user = request.user
    project = Project.objects.get(pk=id)
    reviews = Review.objects.filter(project_id=id).all()
    print(len(reviews))
    current_user = request.user
    project = Project.get_project_by_id(id)
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_id = current_user
            review.project_id = project
            review.save()
    else:
        form=ReviewForm()
    return render(request,'singlepost.html',{"reviews":reviews,"form":form,"project":project})

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'title' in request.GET and request.GET["title"]:
        search_term = request.GET.get("title")
        searched_projects =Project.search_by_title(search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"projects": searched_projects})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message}) 
    

@login_required(login_url='/accounts/login/')  
def edit_project(request, id):
    current_user = request.user
    project = Project.objects.get(id=id)
    form=ProjectForm(instance=project)
    if request.method=='POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect(home)
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'edit_project.html',context)

@login_required(login_url='/accounts/login/')  
def delete_project(request, id):
    current_user = request.user
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        project.delete()
        return redirect(home)

    context = {
        'project': project,
    }
    return render(request, 'delete_project.html', context)


class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)        















     

    
   




