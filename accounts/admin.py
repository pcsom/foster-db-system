from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.
admin.site.register(userBasic)
admin.site.register(careType)
admin.site.register(adoptiveFamily)
admin.site.register(fosterFamily)
admin.site.register(kinshipFamily)
admin.site.register(safetyFamily)
admin.site.register(child)