from rest_framework.decorators import api_view
from rest_framework.response import Response
from foot.models import Room
from .serializers import RoomSerializer

# create an pi folder within foot app
# then within foot app create a views.py , __init__.py , serializers.py AND urls.py

@api_view(['GET']) #allowing the users to only get the DATA
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)



