from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))
    )
    # .prefetch_related('client').prefetch_related('client__user')  # This "prefetches" used for solving N+1 problems,
    # but still the many fields in queryset. In class Prefetch we can customize the queryset for uses fields only
    serializer_class = SubscriptionSerializer
