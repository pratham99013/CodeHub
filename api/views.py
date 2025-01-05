from rest_framework.decorators import api_view , permission_classes 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from myapp.models import Project, Review

@api_view(['GET'])
def getroutes(request):

    routes = [
        {'GET' : '/api/projects'},
        {'GET' : '/api/projects/id'},
         {'POST' : '/api/projects/id/vote'},
             {'POST' : '/api/users/token'},
             {'POST' : '/api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def getprojects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many = True)
    return Response(serializer.data)


@api_view(['GET'])
def getproject(request, pk):
    project = Project.objects.get(id = pk)
    serializer = ProjectSerializer(project, many = False)
    return Response(serializer.data)

@api_view(['POST'])
def projectVote(request, pk):
    project = Project.objects.get(id = pk)
    user = request.user.profile
    data = request.data

    reveiw , created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )

    reveiw.value = data['value']
    reveiw.save()
    project.getvotecount

    print(data)
    serializer = ProjectSerializer(project, many= False)
    return Response(serializer.data)