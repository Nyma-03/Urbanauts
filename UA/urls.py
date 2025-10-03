from django.urls import path
from . import views
from django.urls import path




urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('climate-challenges/', views.climate_challenges, name='climate_challenges'),
    path('track-ecosystems/', views.track_ecosystems, name='track_ecosystems'),
    path('development-sustainability/', views.development_and_sustainability, name='development_and_sustainability'),
    path('waste-management/', views.waste_management, name='waste_management'),
    path('risk-zones/', views.risk_zones, name='risk_zones'),
   
    path('urban-planner-toolkit/', views.urban_planner_toolkit, name='urban_planner_toolkit'),
    path("sustainability/", views.sustainability, name="sustainability"),
    path("api/solar/", views.api_solar, name="api_solar"),
    path("api/water/", views.api_water, name="api_water"),
    path("api/greening/", views.api_greening, name="api_greening"),
    path("api/risks/", views.api_risks, name="api_risks"),
    path("risks/", views.risks, name="risks"),
     path("waste/submit/", views.waste_submit, name="waste_submit"),
    path("waste/dashboard/", views.waste_dashboard, name="waste_dashboard"),

    path("food/offer/", views.food_offer_submit, name="food_offer_submit"),
    path("food/dashboard/", views.food_dashboard, name="food_dashboard"),

    
    
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    
    
    path("blogs/", views.blog_list, name="blog_list"),
    path("blogs/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("blogs/create/", views.blog_create, name="blog_create"),
    path("blogs/<int:blog_id>/edit/", views.blog_edit, name="blog_edit"),
    path('citizen-task/', views.citizen_task, name='citizen_task'),
    path('about/', views.about, name='about'),
     path('goals/', views.goals, name='goals'),
     path('blog/', views.blog, name='blog'),
     path('development/', views.development, name='development'),
     path('riskzones/', views.riskzones, name='riskzones'),
     path('waste/', views.waste_management, name='waste_management'),
      path('contact/', views.contact, name='contact'),
     path('urban-planner-toolkit/', views.urban_planner_toolkit, name='urban_planner_toolkit'),  
]
