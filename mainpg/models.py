from django.db import models
from django.core.cache import cache

# Create your models here.
class SingletonModel(models.Model):
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)


class ReqFormSettings(SingletonModel):      
    fieldInfo = models.JSONField(null=True, blank=True)
    #JSON Dict structure:
    # M x [Field Group, N x [db name, display name, type, [choices] (for dropdown) ]]
    # type is one of "boolean", "char", "textarea"

    links = models.JSONField(null=True, blank=True)
    databaseDisplay = models.JSONField(null=True, blank=True)

class ServiceAccountInfo(SingletonModel):
    serviceActive = models.BooleanField(default=False)
    messageQueue = models.JSONField(default=list)
    errorMessages = models.JSONField(default=dict)



class PickupSettings(SingletonModel):
    pass

