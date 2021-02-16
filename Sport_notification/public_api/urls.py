from rest_framework.routers import DefaultRouter

from Sport_notification.public_api.views import Teams, Subscriptions, TeamCompetitions

router = DefaultRouter()
router.register('teams', Teams, basename='teams')
router.register('subscription', Subscriptions, basename='subscription')
router.register('team_competitions', TeamCompetitions, basename='team_competitions')
