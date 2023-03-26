from django.urls import path, include
from .views import DashboardSqlView, DashboardNoSqlView


urlpatterns = [
        path('dashboard/', DashboardNoSqlView.as_view(), name ='dashboard_url'),
        path('dashboard-sql/', DashboardSqlView.as_view(), name ='dashboard_sql_url'),
]