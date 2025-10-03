from django.contrib import admin
from .models import AirQuality, Biodiversity, Sustainability

class AirQualityAdmin(admin.ModelAdmin):
    list_display = ('city', 'aqi_value', 'status')  

class BiodiversityAdmin(admin.ModelAdmin):
    list_display = ('location', 'ecosystem_strength', 'description')  

class SustainabilityAdmin(admin.ModelAdmin):
    list_display = ('location', 'green_cover', 'water_stress', 'aqi', 'description')  
# Register the models in the admin panel
admin.site.register(AirQuality, AirQualityAdmin)
admin.site.register(Biodiversity, BiodiversityAdmin)
admin.site.register(Sustainability, SustainabilityAdmin)
from django.contrib import admin
from .models import SolarSite, WaterResource, GreeningOpportunity

@admin.register(SolarSite)
class SolarSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "lat", "lon", "ghi_kwh_m2_day", "dni_kwh_m2_day", "suitability")
    list_filter = ("date", "suitability")
    search_fields = ("name",)

@admin.register(WaterResource)
class WaterResourceAdmin(admin.ModelAdmin):
    list_display = ("kind", "name")
    search_fields = ("name", "kind")

@admin.register(GreeningOpportunity)
class GreeningOpportunityAdmin(admin.ModelAdmin):
    list_display = ("location", "date", "lat", "lon", "ndvi", "green_cover", "needs_greening")
    list_filter = ("needs_greening", "date")
    search_fields = ("location",)


from .models import RiskZone

@admin.register(RiskZone)
class RiskZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "risk_type")
    list_filter = ("risk_type", "city")
    search_fields = ("name", "city")

from django.contrib import admin
from .models import Profile, WasteEntry, RecipientSite, FoodOffer, FoodMatch

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "city", "lat", "lon")
    list_filter = ("kind", "city")
    search_fields = ("name", "address", "city")

@admin.register(WasteEntry)
class WasteEntryAdmin(admin.ModelAdmin):
    list_display = ("profile", "date", "waste_type", "weight_kg")
    list_filter = ("waste_type", "date")
    search_fields = ("profile__name",)

@admin.register(RecipientSite)
class RecipientSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "daily_capacity_kg", "lat", "lon")
    list_filter = ("city",)
    search_fields = ("name", "city")

@admin.register(FoodOffer)
class FoodOfferAdmin(admin.ModelAdmin):
    list_display = ("store", "item_name", "quantity_kg", "ready_at", "expires_at", "status")
    list_filter = ("status", "ready_at", "expires_at")
    search_fields = ("store__name", "item_name")

@admin.register(FoodMatch)
class FoodMatchAdmin(admin.ModelAdmin):
    list_display = ("offer", "recipient", "allocated_kg", "distance_km", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("offer__item_name", "recipient__name")
from django.contrib import admin
from .models import Blog

admin.site.register(Blog)




from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('submitted_at',)
