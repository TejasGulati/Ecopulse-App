from django.urls import path
from django.http import JsonResponse
from .views import (
    SustainabilityReportView,
    EnvironmentalImpactView,
    BusinessModelView,
    PredictionView,
    TextGenerationView,
    ImageGenerationView,
    SampleDataView,
)

def api_root(request):
    return JsonResponse({"message": "Welcome to the EcoPulse API"})

urlpatterns = [
    path('', api_root, name='api_root'),
    path('sustainability-report/', SustainabilityReportView.as_view(), name='sustainability_report'),
    path('environmental-impact/', EnvironmentalImpactView.as_view(), name='environmental_impact'),
    path('business-model/', BusinessModelView.as_view(), name='business_model'),
    path('predict/', PredictionView.as_view(), name='predict'),
    path('generate-text/', TextGenerationView.as_view(), name='generate_text'),
    path('generate-image/', ImageGenerationView.as_view(), name='generate_image'),
    path('sample-data/', SampleDataView.as_view(), name='sample-data'),
]