from django.urls import path
from . import views

app_name = "netvis"

urlpatterns = [
    path('graph/<app_name>/<model_name>/<pk>', views.graph_data, name='graph'),
    path('graph/<app_name>/<model_name>', views.qs_graph_data, name='qs_as_graph'),
    path('cached/<app_name>/<model_name>', views.cashed_graph_data, name='cached_graph'),
]
