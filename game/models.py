from django.db import models

class Block(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    owner_color = models.CharField(max_length=7, null=True, blank=True)  
    claimed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('x', 'y')

    def __str__(self):
        return f"Block({self.x},{self.y}) -> {self.owner_color or 'unclaimed'}"