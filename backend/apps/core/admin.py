from django.contrib import admin
from .models import CustodyEvent, FoundItem, Location, Organization, StorageBin

admin.site.register([Organization, Location, StorageBin, FoundItem, CustodyEvent])
