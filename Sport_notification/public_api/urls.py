from rest_framework.routers import DefaultRouter

from Sport_notification.public_api.views import Teams, Subscriptions, TeamMatches

router = DefaultRouter()
router.register('teams', Teams, basename='teams')
router.register('subscription', Subscriptions, basename='subscription')
router.register('team_matches', TeamMatches, basename='team_matches')
