from django.contrib.auth.models import User, Group

from django.views.decorators import cache
from django.utils.decorators import method_decorator

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Coin, Symbol
from rest_framework import viewsets, views
from rest_framework import generics
from .serializers import UserSerializer, GroupSerializer, CoinSerializer, SymbolSerializer, SymbolSimpleSerializer, GeneralSerializer
from .pagination import SymbolsPagination, TotalPagination

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# class CoinViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     queryset = Coin.objects.all()
#     serializer_class = CoinSerializer


class CoinViewSet(viewsets.ModelViewSet):
    # viewsets.ViewSetMixin, generics.ListAPIView

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    pagination_class = TotalPagination  # specify pagination class in the viewset
    serializer_class = CoinSerializer

    def get_queryset(self):
        queryset = Coin.objects.all()

        username = self.request.query_params.get('all', None)
        if username is not None:
            queryset = self.get_serializer_class().setup_eager_loading(queryset, True)
        else:
            queryset = self.get_serializer_class().setup_eager_loading(queryset, False)
        return queryset

    # @method_decorator(cache.cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




class SymbolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # Field for details lookup (default is primary key field)
    lookup_field = 'symbol'

    serializer_class = SymbolSerializer

    def get_queryset(self):
        queryset = Symbol.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

class SymbolsSimpleViewSet(viewsets.ModelViewSet):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    pagination_class = SymbolsPagination  # specify pagination class in the viewset

    queryset = Symbol.objects.all()
    serializer_class = SymbolSimpleSerializer

class GeneralViewSet(views.APIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    data_set = [symbol.coins.all()[0].id for symbol in Symbol.objects.all().prefetch_related('coins')]
    queryset = Coin.objects.filter(id__in=data_set)
    serializer_class = GeneralSerializer