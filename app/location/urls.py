from django.urls import path
from location.views import SuggestionsView

urlpatterns = [
    path("suggestions", SuggestionsView.as_view(), name="suggestions"),
]
