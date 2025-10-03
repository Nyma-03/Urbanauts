from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def climate_challenges(request):
    return HttpResponse("Climate Challenges Content Goes Here.")

from django.shortcuts import render



def development_and_sustainability(request):
    # Simulated data
    solar_energy_sites = ["Site 1", "Site 2", "Site 3"]
    water_resources = {
        "rivers": ["River 1", "River 2"],
        "lakes": ["Lake 1", "Lake 2"],
        "water_stress": ["Area 1", "Area 2"]
    }
    urban_greening = ["Area 1", "Area 2", "Area 3"]

    context = {
        'solar_energy_sites': solar_energy_sites,
        'water_resources': water_resources,
        'urban_greening': urban_greening,
    }

    return render(request, 'development_and_sustainability.html', context)


def waste_management(request):
    return HttpResponse("Waste Management Content Goes Here.")

def risk_zones(request):
    # Simulated data
    flood_risk = ["Area 1", "Area 2"]
    rainfall_risk = ["Area 3", "Area 4"]
    drought_risk = ["Area 5", "Area 6"]

    context = {
        'flood_risk': flood_risk,
        'rainfall_risk': rainfall_risk,
        'drought_risk': drought_risk,
    }

    return render(request, 'risk_zones.html', context)


def blogs(request):
    return HttpResponse("Blogs Content Goes Here.")

def urban_planner_toolkit(request):
    return HttpResponse("Urban Planner Toolkit Content Goes Here.")
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import render
from .models import AirQuality, Biodiversity, Sustainability



def track_ecosystems(request):
    aqi_data = None
    biodiversity_data = None
    sustainability_data = None

    if request.method == 'POST':
        location = request.POST.get('location')

        try:
            aqi_data = AirQuality.objects.get(city=location)
            biodiversity_data = Biodiversity.objects.get(location=location)
            sustainability_data = Sustainability.objects.get(location=location)
        except (AirQuality.DoesNotExist, Biodiversity.DoesNotExist, Sustainability.DoesNotExist):
            aqi_data = None
            biodiversity_data = None
            sustainability_data = None

        # Build chart-friendly numbers (avoid template conditionals)
        aqi_values = {
            'good': aqi_data.aqi_value if (aqi_data and aqi_data.aqi_value <= 50) else 0,
            'moderate': aqi_data.aqi_value if (aqi_data and 50 < aqi_data.aqi_value <= 100) else 0,
            'hazardous': aqi_data.aqi_value if (aqi_data and aqi_data.aqi_value > 100) else 0,
        }

        # Sustainability: show the raw components (percent metrics + AQI already separate)
        sustainability_values = {
            'green_cover': sustainability_data.green_cover if sustainability_data else 0,   # %
            'water_stress': sustainability_data.water_stress if sustainability_data else 0, # %
            'aqi': sustainability_data.aqi if sustainability_data else 0                    # number
        }

        # Biodiversity: treat ecosystem_strength as 0–100; show “Remaining” as complement
        eco_strength = biodiversity_data.ecosystem_strength if biodiversity_data else 0
        try:
            eco_strength = float(eco_strength)
        except (TypeError, ValueError):
            eco_strength = 0.0
        eco_strength = max(0.0, min(100.0, eco_strength))  # clamp to [0,100]

        biodiversity_values = {
            'ecosystem_strength': eco_strength,
            'remaining': 100.0 - eco_strength
        }

        context = {
            'aqi_data': aqi_data,
            'biodiversity_data': biodiversity_data,
            'sustainability_data': sustainability_data,
            'aqi_values': aqi_values,
            'sustainability_values': sustainability_values,
            'biodiversity_values': biodiversity_values,
        }
        return render(request, 'track_ecosystems.html', context)

    return render(request, 'track_ecosystems.html')



from django.http import JsonResponse
from django.shortcuts import render
from .models import SolarSite, WaterResource, GreeningOpportunity

def sustainability(request):
    return render(request, "sustainability.html")

def api_solar(request):
    data = [{
        "name": s.name, "lat": s.lat, "lon": s.lon, "date": s.date.isoformat(),
        "ghi": s.ghi_kwh_m2_day, "dni": s.dni_kwh_m2_day, "suitability": s.suitability
    } for s in SolarSite.objects.order_by("-date")[:1000]]
    return JsonResponse({"items": data})

def api_water(request):
    rivers, reservoirs = [], []
    for w in WaterResource.objects.all()[:3000]:
        d = {"name": w.name, "kind": w.kind, "geom": w.geom_geojson, "props": w.props}
        (rivers if w.kind == "river" else reservoirs).append(d)
    return JsonResponse({"rivers": rivers, "reservoirs": reservoirs})

def api_greening(request):
    items = [{
        "location": g.location, "lat": g.lat, "lon": g.lon,
        "date": g.date.isoformat(), "ndvi": g.ndvi, "green_cover": g.green_cover,
        "needs": g.needs_greening, "note": g.note
    } for g in GreeningOpportunity.objects.order_by("-date")[:2000]]
    return JsonResponse({"items": items})



#===========

from .models import RiskZone

def risks(request):
    return render(request, "risks.html")

def api_risks(request):
    zones = RiskZone.objects.all()
    data = []
    for z in zones:
        data.append({
            "id": z.id,
            "name": z.name,
            "city": z.city,
            "risk_type": z.risk_type,
            "description": z.description,
            "geom": z.geom_geojson,
        })
    return JsonResponse({"zones": data})
#============


from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Profile, WasteEntry, RecipientSite, FoodOffer, FoodMatch, haversine_km
)
from .forms import WasteEntryForm, FoodOfferForm

# ----------- Waste Tracking -----------

def waste_submit(request):
    if request.method == "POST":
        form = WasteEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("waste_dashboard")
    else:
        form = WasteEntryForm()
    return render(request, "waste_form.html", {"form": form})

def waste_dashboard(request):
    # period (last 30 days)
    start = timezone.now().date() - timezone.timedelta(days=30)
    entries = WasteEntry.objects.filter(date__gte=start).select_related("profile")

    # totals per profile
    totals = (
        entries.values("profile__id", "profile__name", "profile__kind")
        .annotate(total_kg=Sum("weight_kg"))
        .order_by("total_kg")  # less is better (sustained)
    )

    # totals by waste type
    by_type = (
        entries.values("waste_type")
        .annotate(total_kg=Sum("weight_kg"))
        .order_by("-total_kg")
    )

    return render(request, "waste_dashboard.html", {
        "totals": totals,
        "by_type": by_type,
        "start": start,
    })

# ----------- Food Waste & Redistribution -----------

def food_offer_submit(request):
    if request.method == "POST":
        form = FoodOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("food_dashboard")
    else:
        form = FoodOfferForm()
    return render(request, "food_offer_form.html", {"form": form})

def food_dashboard(request):
    # active offers
    offers = FoodOffer.objects.select_related("store").order_by("-ready_at")

    # naive on-the-fly suggestions (not persisted unless you create FoodMatch)
    suggestions = []
    active_offers = [o for o in offers if o.is_active() and o.store.lat and o.store.lon]
    recipients = list(RecipientSite.objects.all())

    for offer in active_offers:
        ranked = []
        for rec in recipients:
            dist = haversine_km(offer.store.lat, offer.store.lon, rec.lat, rec.lon)
            # accept within 12 km (tune) and capacity > 0
            if dist <= 12 and rec.daily_capacity_kg > 0:
                alloc = min(offer.quantity_kg, rec.daily_capacity_kg)
                ranked.append((dist, rec, alloc))
        ranked.sort(key=lambda x: x[0])
        if ranked:
            top3 = ranked[:3]
            suggestions.append({
                "offer": offer,
                "candidates": [{"recipient": r, "distance": round(d,2), "allocated": a} for (d,r,a) in top3]
            })

    return render(request, "food_dashboard.html", {
        "offers": offers,
        "suggestions": suggestions,
    })



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import UserExtra

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    userextra = UserExtra.objects.get(user=request.user)

    if request.method == "POST":
        userextra.bio = request.POST.get("bio", userextra.bio)
        userextra.city = request.POST.get("city", userextra.city)
        userextra.latitude = request.POST.get("latitude", userextra.latitude)
        userextra.longitude = request.POST.get("longitude", userextra.longitude)
        userextra.save()
        return redirect("profile")

    return render(request, "profile.html", {"userextra": userextra})






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm


from django.db.models import Q
from django.shortcuts import render

def blog_list(request):
    query = request.GET.get("q")
    if query and query.strip():
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query)
        ).order_by("-created_at")
    else:
        blogs = Blog.objects.all().order_by("-created_at")
    return render(request, "blog_list.html", {"blogs": blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, "blog_detail.html", {"blog": blog})

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("blog_list")
    else:
        form = BlogForm()
    return render(request, "blog_form.html", {"form": form})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, author=request.user)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, "blog_form.html", {"form": form})




from django.shortcuts import render

# views.py

# views.py
from django.shortcuts import render


from django.shortcuts import render
from django.http import JsonResponse

def urban_planner_toolkit(request):
    # Default stats
    default_stats = {
        "air_quality": 50,
        "co2": 50,
        "co2_bar": 50,
        "energy_sustainability": 50
    }

    # Load stats from session or initialize
    stats = request.session.get('stats', default_stats.copy())

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.POST.get("action")
        message = ""

        if action == "add_park":
            stats['air_quality'] = min(stats['air_quality'] + 10, 100)
            message = "🌳 Park Added! Air Quality +10%"
        elif action == "reduce_traffic":
            stats['co2'] = max(stats['co2'] - 15, 0)
            stats['co2_bar'] = 100 - stats['co2']
            message = "🚗 Traffic Reduced! CO₂ -15%"
        elif action == "build_solar_farm":
            stats['energy_sustainability'] = min(stats['energy_sustainability'] + 20, 100)
            message = "☀️ Solar Farm Built! Energy +20%"

        request.session['stats'] = stats
        return JsonResponse({"stats": stats, "message": message})

    return render(request, 'urban_planner_toolkit.html', {"stats": stats})




from django.shortcuts import render

def citizen_task(request):
    return render(request, 'climate_challenges.html')

def about(request):
    return render(request, 'index(about).html')

from django.shortcuts import render

def goals(request):
    return render(request, 'index(goals).html')
def blog(request):
    return render(request, 'blog.html')
# views.py
def development(request):
    return render(request, 'development.html')
# views.py
def riskzones(request):
    return render(request, 'riskzones.html')
from django.shortcuts import render

def waste_management(request):
    return render(request, 'waste.html')
from django.shortcuts import render
from .models import ContactMessage

def contact(request):
    success = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        success = "Your message has been sent successfully!"

    return render(request, 'contact.html', {'success': success})
