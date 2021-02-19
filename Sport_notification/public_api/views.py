from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from Sport_notification.data.models import Team, Subscription


class Teams(viewsets.ModelViewSet):
    model = Team


class Subscriptions(viewsets.ModelViewSet):
    model = Subscription
    #todo implement create subscription
    

class TeamMatches(viewsets.ModelViewSet):
    pass  #todo list Teams for current user and their last, current and next competition
