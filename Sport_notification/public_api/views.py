import secrets

from rest_framework import viewsets

from data.models import Team, Subscription

from public_api.serializers import TeamSerializer
from rest_framework.response import Response

from data.models import Subscriber
from public_api.serializers import SubscriptionSerializer
from rest_framework.views import APIView


class Teams(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    model = Team


class Subscriptions(viewsets.ViewSet):

    def create(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            session_token = secrets.token_urlsafe(16)
            request.session['sport_token'] = session_token
            subscriber = Subscriber.objects.create(
                token=session_token,
                subscription_details=obj,
            )
            return Response(True)
        else:
            return Response(serializer.errors)


class TeamMatches(viewsets.ViewSet):

    def list(self, request):
        token = request.session.get('sport_token')
        if token:
            subscriber = Subscriber.objects.get(token=token)
            # todo
            # subscriptions for subscriber
            # teams for subscriptions
            # matches or fixtures for teams
            return Response(subscriber)
        else:
            return Response(status=404)
