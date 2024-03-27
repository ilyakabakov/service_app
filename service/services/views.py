from django.db.models import Prefetch, F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name',
                                                                                     'user__email'))
    )#.annotate(price=F('service__full_price') -
     #                F('service__full_price') * F('plan__discount_percent') / 100.00)
    # .prefetch_related('client').prefetch_related('client__user')  # This "prefetches" used for solving N+1 queries problems,
    # but still the many fields in queryset. In class Prefetch we can customize the queryset for uses fields only
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        # Never to do the next code if this is not agreed upon by the team
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response
