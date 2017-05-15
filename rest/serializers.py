from django.contrib.auth.models import User, Group
from django.db.models import Prefetch
from .models import Coin, Symbol
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class SymbolSerializer(serializers.HyperlinkedModelSerializer):

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('coins')
        return queryset

    coins = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='coins-detail'
    )

    class Meta:
        model = Symbol
        fields = ('name', 'symbol', 'coins')

class SymbolSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Symbol
        fields = ('name', 'symbol')

class CoinSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.SerializerMethodField('get_symbol_name')
    symb = serializers.SerializerMethodField('get_symbol_symbol')

    @staticmethod
    def setup_eager_loading(queryset, get_all=False):
        if get_all:
            data_set = [symbol.coins.all()[0].id for symbol in Symbol.objects.all().prefetch_related('coins')]
            queryset = Coin.objects.filter(id__in=data_set).order_by('-market_cap').select_related('symbol')
        else:
            queryset = queryset.select_related('symbol')

        return queryset

    def get_symbol_name(self, model):
        return model.symbol.name

    def get_symbol_symbol(self, model):
        return model.symbol.symbol

    class Meta:
        model = Coin
        fields = ('id','name', 'symb', 'market_cap', 'price', 'supply', 'volume', 'hour_prc', 'day_prc', 'week_prc', 'update_date')

class GeneralSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.SerializerMethodField('get_symbol_name')
    symb = serializers.SerializerMethodField('get_symbol_symbol')

    def get_symbol_name(self, model):
        return model.symbol.name

    def get_symbol_symbol(self, model):
        return model.symbol.symbol

    class Meta:
        model = Coin
        fields = ('id', 'name', 'symb', 'market_cap', 'price', 'supply', 'volume', 'hour_prc', 'day_prc', 'week_prc',
                  'update_date')