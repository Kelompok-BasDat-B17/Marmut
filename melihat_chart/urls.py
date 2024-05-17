from django.urls import path
from melihat_chart.views import melihat_chart, daily_top,weekly_top, monthly_top, yearly_top

app_name = 'melihat-chart'

urlpatterns = [
    path('melihat-chart/', melihat_chart, name='melihat_chart'),
    path('melihat-chart/daily-top/', daily_top, name='daily_top'),
    path('melihat-chart/weekly-top/', weekly_top, name='weekly_top'),
    path('melihat-chart/monthly-top/', monthly_top, name='monthly_top'),
    path('melihat-chart/yearly-top/', yearly_top, name='yearly_top'),
]
