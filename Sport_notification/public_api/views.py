from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from data.models import Team, Subscription

from public_api.serializers import TeamSerializer


class Teams(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    model = Team


class Subscriptions(viewsets.ModelViewSet):
    model = Subscription
    #todo implement create subscription
    

class TeamMatches(viewsets.ModelViewSet):
    pass  #todo list Teams for current user and their last, current and next competition
