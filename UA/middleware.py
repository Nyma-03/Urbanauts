# from .models import Citizen

# class EnsureCitizenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = getattr(request, "user", None)
#         if user and user.is_authenticated:
#             try:
#                 _ = user.citizen  # access will raise if missing
#             except Citizen.DoesNotExist:
#                 Citizen.objects.create(user=user, full_name=user.get_full_name() or user.username)
#         return self.get_response(request)
