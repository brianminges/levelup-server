"""View module for handling requests about game types"""
from datetime import date
from time import time
from rest_framework.decorators import action
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game, Gamer, GameType, game


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event
        
        Returns:
            Response -- JSON serialized event
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        game = request.query_params.get('game', None)
        gamer = Gamer.objects.get(user=request.auth.user)
        if game is not None:
            events = events.filter(game_id=game)
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    # def create(self, request):
    #     """Handle POST operations
        
    #     Returns
    #         Response -- JSON serialized game instance
    #     """
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     game=Game.objects.get(pk=request.data["game"])
               
    #     event = Event.objects.create(
    #         description=request.data["description"],
    #         date=request.data["date"],
    #         time=request.data["time"],
    #         game=game,
    #         organizer=gamer

    #     )
    #     serializer = EventSerializer(event)
    #     return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # def update(self, request, pk):
    #     """Handle PUT operations
        
    #     Returns
    #         Response -- JSON serialized game instance
    #     """
    #     event = Event.objects.get(pk=pk)
    #     game = Game.objects.get(pk=request.data["game"])
    #     event.game = game
    #     event.description = request.data["description"]
    #     event.date = request.data["date"]
    #     event.time = request.data["time"]
    #     # organizer = Gamer.objects.get(pk=request.data["gamer"])
    #     # event.organizer = organizer
    #     event.save()
        
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        """ Handle PUT operations
        
        Returns
            Response -- JSON serialized game instance
        """
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)    
    
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Delete request or a user to leave an event"""
        
        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
    
 
        
        

# class EventSerializer(serializers.ModelSerializer):
#     """JSON serializer for events
#     """
#     class Meta:
#         model = Event
#         fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
#         depth = 2
        
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'attendees', 'organizer', 'joined')
        depth = 2
        
class CreateEventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time']