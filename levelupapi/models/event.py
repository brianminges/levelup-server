from django.db import models
from levelupapi.models.game import Game
from levelupapi.models.gamer import Gamer



class Event(models.Model):
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE) 
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField() 
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE) 
    attendees = models.ManyToManyField(Gamer, related_name="attending")
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
