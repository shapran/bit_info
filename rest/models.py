from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Symbol(models.Model):

    class Meta:
        db_table = 'Symbol'

    symbol = models.CharField(db_index=True, max_length=16)
    name = models.CharField(db_index=True, primary_key=True, max_length=50, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s>' % self.name

class Coin(models.Model):

    class Meta:
        db_table = 'Coin'
        ordering = ['-update_date']

    symbol = models.ForeignKey(Symbol, related_name='coins', on_delete=models.CASCADE, null=True)
    market_cap = models.DecimalField(max_digits=14, decimal_places=2)
    price = models.DecimalField(max_digits=18, decimal_places=6)
    supply = models.DecimalField(max_digits=18, decimal_places=3)
    volume = models.DecimalField(max_digits=18, decimal_places=3)
    hour_prc = models.FloatField(default=0, validators=[MaxValueValidator(999.999), MinValueValidator(0.0)])
    day_prc =  models.FloatField(default=0, validators=[MaxValueValidator(999.999), MinValueValidator(0.0)])
    week_prc = models.FloatField(default=0, validators=[MaxValueValidator(999.999), MinValueValidator(0.0)])
    update_date = models.DateTimeField(db_index=True, default=timezone.now)

    def __str__(self):
        return '{0} at {1}'.format(self.symbol.name, self.update_date)

    def __repr__(self):
        return '<%s-%s>' % (self.symbol.name, self.update_date.strftime('%m:%h_%d_%m_%Y'))