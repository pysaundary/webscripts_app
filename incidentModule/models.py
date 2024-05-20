from django.db import models
from utilities.models import ControlUtility
import string,random
# Create your models here.

def getCurrentYear():
    from datetime import datetime
    return datetime.now().year

def create_random_otp():
    import random
    max_range=99999
    min_range=00000
    return random.randint(min_range,max_range)

def  createIncidentId()->str:
    key=f"RMG{create_random_otp()}{getCurrentYear()}"
    if not IncidentModel.objects.filter(incidentId = key).exists():
        return key
    else:
        createIncidentId()

class IncidentModel(models.Model):
    ENTERPRISE,GOVERMENT = ("enterprise","goverment") 
    incidentChoices = (
        (ENTERPRISE,"enterprise"),
        (GOVERMENT,"goverment")
    ) 

    HIGH,MEDIUM,LOW = ("high","medium","low")
    priorityChoices = (
        (HIGH,"high"),
        (MEDIUM,"medium"),
        (LOW,"low")
    )

    OPEN,IN_PROCESS,CLOSED = (
        "open",
        "in_process",
        "low"
    )
    incidentStatusChoices = (
        (OPEN,"open"),
        (IN_PROCESS,"in_process"),
        (LOW,"low")
    )
    createBy = models.ForeignKey("authentication.Users", verbose_name= "Incident reporter", on_delete=models.CASCADE ,related_name="reportedBy")
    incidentId = models.CharField("incident id", max_length=50,null=True,blank=True)
    details = models.TextField("incident details")
    incidentType = models.CharField("Incident Type", max_length=50 ,choices= incidentChoices , default= ENTERPRISE)
    priority = models.CharField("Incident Priority", max_length=50 ,choices=priorityChoices , default= LOW)
    status = models.CharField("Incident Status", max_length=50,choices=incidentStatusChoices , default= OPEN)

    # def save(self,*args, **kwargs) -> None:
        # if self.incidentId == None:
            # self.incidentId = createIncidentId()
        # return super().save()

    class Meta:
        verbose_name = "IncidentModel"
        verbose_name_plural = "IncidentModels"

   

   

