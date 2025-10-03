from django.db import models

# Model to store the AQI data
class AirQuality(models.Model):
    city = models.CharField(max_length=100)
    aqi_value = models.IntegerField()  # Air Quality Index value

    def get_status(self):
        if self.aqi_value <= 50:
            return "Good"
        elif self.aqi_value <= 100:
            return "Moderate"
        elif self.aqi_value <= 150:
            return "Unhealthy for Sensitive Groups"
        elif self.aqi_value <= 200:
            return "Unhealthy"
        elif self.aqi_value <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    @property
    def status(self):
        return self.get_status()

    def __str__(self):
        return f'{self.city} - {self.status}'

# Model to store biodiversity data
class Biodiversity(models.Model):
    location = models.CharField(max_length=100)
    ecosystem_strength = models.CharField(max_length=50)  # Strong, Moderate, Weak
    description = models.TextField(blank=True)  # Leave it blank for automatic generation

    def get_description(self):
        if self.ecosystem_strength == "Strong":
            return "This ecosystem is strong with a high level of biodiversity, supporting various species."
        elif self.ecosystem_strength == "Moderate":
            return "This ecosystem has a moderate level of biodiversity, with some environmental stressors."
        else:
            return "This ecosystem is weak with limited biodiversity and is highly impacted by environmental degradation."

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.get_description()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.location} - {self.ecosystem_strength}'

# Model to store sustainability data
class Sustainability(models.Model):
    location = models.CharField(max_length=100)
    green_cover = models.FloatField()  # % of green cover
    water_stress = models.FloatField()  # % of water-stressed areas
    aqi = models.IntegerField()  # Average AQI for the location
    description = models.TextField(blank=True)  # Manual or auto-generated description

    def get_description(self):
        # Green Cover Description
        if self.green_cover >= 50:
            green_cover_desc = "The area has a high level of green cover, contributing positively to the environment."
        elif self.green_cover >= 20:
            green_cover_desc = "The area has moderate green cover, but it can be improved."
        else:
            green_cover_desc = "The area has low green cover, which is a concern for sustainability."

        # Water Stress Description
        if self.water_stress <= 30:
            water_stress_desc = "The area has low water stress, indicating good water availability."
        elif self.water_stress <= 60:
            water_stress_desc = "The area has moderate water stress, with potential challenges in the future."
        else:
            water_stress_desc = "The area is facing high water stress, and conservation efforts are crucial."

        # Combining the descriptions
        return f"{green_cover_desc} {water_stress_desc}"

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.get_description()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.location} Sustainability'
#=================================================

from django.db import models

class SolarSite(models.Model):
    """
    Manually store daily solar resource indicators for candidate sites.
    """
    name = models.CharField(max_length=120)
    lat = models.FloatField()
    lon = models.FloatField()
    date = models.DateField()
    ghi_kwh_m2_day = models.FloatField(help_text="Global Horizontal Irradiance (kWh/m²/day)")
    dni_kwh_m2_day = models.FloatField(null=True, blank=True, help_text="Direct Normal Irradiance (kWh/m²/day)")
    suitability = models.CharField(max_length=20, blank=True)  # auto: High/Medium/Low

    def save(self, *args, **kwargs):
        if not self.suitability:
            if self.ghi_kwh_m2_day >= 5.0:
                self.suitability = "High"
            elif self.ghi_kwh_m2_day >= 3.5:
                self.suitability = "Medium"
            else:
                self.suitability = "Low"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.date}) — {self.ghi_kwh_m2_day} kWh/m²/day"


class WaterResource(models.Model):
    """
    Store river/reservoir geometries as GeoJSON (keeps deps light).
    GeoJSON coordinates are [lon, lat].
    """
    WATER_KIND = [("river", "River/Stream"), ("reservoir", "Reservoir/Dam")]
    kind = models.CharField(max_length=12, choices=WATER_KIND)
    name = models.CharField(max_length=200, blank=True)
    geom_geojson = models.JSONField()
    props = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.kind}: {self.name or 'unnamed'}"


class GreeningOpportunity(models.Model):
    """
    Points where urban greening would reduce risk (low NDVI or low green cover).
    """
    location = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    date = models.DateField()
    ndvi = models.FloatField(null=True, blank=True)
    green_cover = models.FloatField(null=True, blank=True)
    needs_greening = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        flag = False
        if self.ndvi is not None:
            flag = self.ndvi < 0.2   # low vegetation
        elif self.green_cover is not None:
            flag = self.green_cover < 20.0
        self.needs_greening = flag
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} — {'Needs greening' if self.needs_greening else 'OK'}"


#==========

class RiskZone(models.Model):
    RISK_TYPES = [
        ("flood", "Flood Risk"),
        ("rainfall", "Rainfall Risk"),
        ("drought", "Drought Zone"),
    ]
    risk_type = models.CharField(max_length=20, choices=RISK_TYPES)
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100, blank=True)
    geom_geojson = models.JSONField(help_text="GeoJSON geometry: Polygon or MultiPolygon")
    description = models.TextField(blank=True)

    def default_description(self):
        if self.risk_type == "flood":
            return "Avoid housing here; ideal for wetlands/parks/fish farming."
        elif self.risk_type == "rainfall":
            return "High rainfall; avoid farming that needs sunlight or new construction."
        elif self.risk_type == "drought":
            return "Drought-prone; unsuitable for farming, better for solar plants."
        return ""

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = self.default_description()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_risk_type_display()} — {self.name}"
#================

from django.db import models
from django.utils import timezone
from math import radians, sin, cos, sqrt, atan2

# ---------- Core actors ----------

class Profile(models.Model):
    """Households or Stores that will report waste or food surplus."""
    KIND_CHOICES = [
        ("household", "Household"),
        ("store", "Store / Bakery / Restaurant"),
    ]
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, default="Chattogram")
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_kind_display()}: {self.name}"

# ---------- Waste Tracking ----------

class WasteEntry(models.Model):
    """User-submitted waste log (daily/weekly). Lower weight => better."""
    WASTE_TYPES = [
        ("organic", "Organic"),
        ("recyclable", "Recyclable"),
        ("landfill", "Landfill"),
        ("food", "Food Waste"),
        ("hazard", "Hazardous (special handling)"),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="waste_entries")
    date = models.DateField(default=timezone.now)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    weight_kg = models.FloatField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.profile.name} — {self.waste_type} {self.weight_kg} kg on {self.date}"

# ---------- Food Waste & Redistribution ----------

class RecipientSite(models.Model):
    """NGO / Shelter / Food bank receiving surplus food."""
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, default="Chattogram")
    lat = models.FloatField()
    lon = models.FloatField()
    daily_capacity_kg = models.FloatField(default=50)

    def __str__(self):
        return f"{self.name} ({self.city})"

class FoodOffer(models.Model):
    """Surplus food from stores/bakeries/restaurants."""
    STATUS = [
        ("open", "Open"),
        ("matched", "Matched"),
        ("collected", "Collected"),
        ("expired", "Expired"),
    ]
    store = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="food_offers",
                              limit_choices_to={"kind": "store"})
    item_name = models.CharField(max_length=150)
    quantity_kg = models.FloatField()
    ready_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS, default="open")
    notes = models.TextField(blank=True)

    def is_active(self):
        return self.status in ("open", "matched") and self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.store.name} → {self.item_name} ({self.quantity_kg} kg)"

class FoodMatch(models.Model):
    """Suggested/confirmed pairing of FoodOffer to RecipientSite."""
    STATUS = [
        ("suggested", "Suggested"),
        ("confirmed", "Confirmed"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    offer = models.ForeignKey(FoodOffer, on_delete=models.CASCADE, related_name="matches")
    recipient = models.ForeignKey(RecipientSite, on_delete=models.CASCADE, related_name="matches")
    allocated_kg = models.FloatField()
    distance_km = models.FloatField()
    status = models.CharField(max_length=12, choices=STATUS, default="suggested")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.offer.item_name} → {self.recipient.name} ({self.allocated_kg} kg)"

# ---------- Utility ----------

def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km."""
    R = 6371.0
    p1, p2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dl = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(p1)*cos(p2)*sin(dl/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


#============
# from django.db import models
# from django.contrib.auth.models import User

# class UserExtra(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True, null=True)
#     neon_color = models.CharField(max_length=20, default="#39ff14")  # cyberpunk glow

#     def __str__(self):
#         return self.user.username
from django.db import models
from django.contrib.auth.models import User

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    neon_color = models.CharField(max_length=20, default="#39ff14")

    def __str__(self):
        return self.user.username







from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=200, blank=True, null=True)  # simple tag string

    def __str__(self):
        return self.title




from django.db import models
from django.contrib.auth.models import User

class CityStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    air_quality = models.IntegerField(default=50)       # 0-100%
    co2 = models.IntegerField(default=50)              # 0-100%
    energy_sustainability = models.IntegerField(default=50)
    
    def __str__(self):
        return f"{self.user.username}'s City Stats"



from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
