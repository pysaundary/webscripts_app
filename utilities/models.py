from django.db import models

# Create your models here.

class ControlUtility(models.Model):
    isActive = models.BooleanField(default = True)
    isDeleted = models.BooleanField(default=True)    

    class Meta:
        verbose_name = "ControlUtility"
        verbose_name_plural = "ControlUtilities"



