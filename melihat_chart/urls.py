from django.urls import path
from melihat_chart.views import melihat_chart, chart_detail

app_name = 'melihat-chart'

urlpatterns = [
    path('melihat-chart/', melihat_chart, name='melihat_chart'),
    path('melihat-chart/<uuid:chart_id>', chart_detail, name='chart_detail'),
]
