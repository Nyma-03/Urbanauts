from django import forms
from django.utils import timezone
from .models import WasteEntry, FoodOffer

class WasteEntryForm(forms.ModelForm):
    class Meta:
        model = WasteEntry
        fields = ["profile", "date", "waste_type", "weight_kg", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type":"date"}),
            "notes": forms.Textarea(attrs={"rows":3}),
        }

class FoodOfferForm(forms.ModelForm):
    class Meta:
        model = FoodOffer
        fields = ["store", "item_name", "quantity_kg", "ready_at", "expires_at", "notes"]
        widgets = {
            "ready_at": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "expires_at": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "notes": forms.Textarea(attrs={"rows":3}),
        }

    def clean(self):
        cleaned = super().clean()
        ready = cleaned.get("ready_at")
        exp = cleaned.get("expires_at")
        if ready and exp and exp <= ready:
            raise forms.ValidationError("Expiry must be after ready time.")
        if exp and exp <= timezone.now():
            raise forms.ValidationError("Expiry must be in the future.")
        return cleaned


# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserExtra

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "city")

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserExtra.objects.create(user=user, city=self.cleaned_data.get("city"))
        return user





from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "tags"]
