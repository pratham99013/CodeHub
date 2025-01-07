from django.shortcuts import render, redirect
from .forms import ProjectForm, ReveiwForm
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def projects(request):
    search_query = ''

    if request.GET.get('search_query'):
         search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains = search_query)

    hello = Project.objects.distinct().filter( Q(title__icontains = search_query) | Q(description__icontains = search_query) | Q(owner__name__icontains = search_query)
                                   | Q(tags__in = tags))
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(hello, results)

    try:
        hello = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        hello = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages 
        hello = paginator.page(page)

    context = {'projects' : hello, 'paginator' : paginator}
    return render(request, 'projects.html', context) 

def viewproject(request, pk):
    hello = Project.objects.get(id=pk)
    form = ReveiwForm()

    if request.method == 'POST':
        form = ReveiwForm(request.POST)
        reveiw = form.save(commit=False)
        reveiw.project = hello
        reveiw.owner = request.user.profile
        reveiw.save()
        hello.getvotecount()
        return redirect('viewproject' , pk = hello.id)
    context = {'project' : hello, 'form' : form}
    return render(request, 'single-project.html', context) 

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tag, Project
from .forms import ProjectForm

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    tags = Tag.objects.all()  # Fetch all existing tags to show in the template

    if request.method == 'POST':
        # Get custom tags
        newtags = request.POST.get('newtags', '').replace(',', ' ').split()

        # Get selected existing tags
        selected_tags = request.POST.getlist('existing_tags')  # Get list of selected tag IDs

        # Handle form submission
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            # Add existing tags to the project
            for tag_id in selected_tags:
                tag = Tag.objects.get(id=tag_id)
                project.tags.add(tag)

            # Add custom tags to the project
            for tag_name in newtags:
                tag_name = tag_name.strip()
                if tag_name:  # Ensure tag is not empty
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            messages.success(request, 'Project added successfully')
            return redirect('projects')

    context = {
        'form': form,
        'tags': tags,  # Pass existing tags to the template
    }
    return render(request, 'project_form.html', context)

@login_required(login_url= "login")
def updateProject(request, pk):
    project = Project.objects.get(id = pk)
    form = ProjectForm(instance= project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

    if request.method == 'POST': 
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated succesfully')
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('projects')
        

    context = {'form' : form, }
    return render(request,  'project_form.html', context)


@login_required(login_url= "login")
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.error(request, 'Project deleted succesfully')
        return redirect('projects')
    context = {'object' : project}
    return render(request, 'delete_template.html' , context)