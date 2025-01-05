from django.shortcuts import render, redirect
from .models import Profile, Skills
from myapp.models import Project
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, Profileform, SkillForm, MessageForm
from django.db.models import Q
 



def loginPage(request):

    page = 'login'
    context = {'page' : page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both fields are required.')
            return render(request, 'login_register.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login done successfully')
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.error(request, 'user logout')
    return redirect('profiles')


def RegisterUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created successfully!')
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            print(form.errors)  # Debugging: Print form errors in the console
            messages.error(request, 'An error occurred during registration.')

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)




def profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
         search_query = request.GET.get('search_query')
    
    skills = Skills.objects.filter(name__iexact = search_query)
        
    g1 = Profile.objects.distinct().filter( Q(name__icontains = search_query)
                                 | Q(short_intro__icontains = search_query)
                                 | Q(skills__in = skills))
    context = {'profile' : g1, 'search_query' : search_query}
    return render(request, 'profiles.html', context)



def userprofile(request, pk):
    g1 = Profile.objects.get(id=pk)
    project = Project.objects.filter(owner = g1)
    context = {'profile' : g1 , 'project' : project}
    return render(request, 'user-profile.html', context)


@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile
    projects = profile.project_set.all()
    context = {'profile' : profile, 'projects' : projects}
    return render(request, 'account.html', context)


@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.profile
    form = Profileform(instance=profile)

    if request.method == "POST":
         form = Profileform(request.POST, request.FILES, instance=profile )
         if form.is_valid:
             form.save()
             messages.success(request, 'User edited successfully!')
             return redirect('account')
      
    context = {'form' : form}
    return render(request, 'profile_form.html', context)


@login_required(login_url = 'login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
       form = SkillForm(request.POST) 
       if form.is_valid:
           skill = form.save(commit=False)
           skill.owner = profile
           skill.save()
           messages.success(request, 'Skill was added')
           return redirect('account') 
    context = {'form' : form}
    return render(request, 'skill_form.html', context)



@login_required(login_url = 'login')
def deleteSkill(request, pk):
 profile = request.user.profile
 skill = profile.skills_set.get(id = pk)



 if request.method == 'POST':
     skill.delete()
     messages.error(request, 'Skill was removed')
     return redirect('account')
         
 context = {'skill' : skill}
 return render(request, 'delete.html', context)


@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unread = messageRequest.filter(is_read = False).count()
    context = { 'messagerequest' : messageRequest, 'unread' : unread}
    return render(request, 'inbox.html', context)


@login_required(login_url = 'login')
def viewmessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id = pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message' : message}
    return render(request, 'message.html', context)




@login_required(login_url = 'login')
def createmessage(request, pk):
    recepient = Profile.objects.get(id=pk)
    form = MessageForm()
    sender = request.user.profile

    if request.method == 'POST':
          form = MessageForm(request.POST)
          if form.is_valid():
              message = form.save(commit=False)
              message.sender = sender
              message.recepient =  recepient
              message.name = sender.name
              message.email = sender.email
              message.save()
              messages.success(request, 'Successfully sent !')
              return redirect('user-profile', pk=recepient.id)

            


    context = {'recepient' :  recepient , 'form' : form}
    return render(request, 'message_form.html', context)