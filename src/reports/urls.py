from django.urls import path
from .views import (
    report_view, SelectView, main_report_summary, HomeView, delete_view, ReportUpdateView, generate_problems_in_pdf)
app_name = "reports"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('reports/', SelectView.as_view(), name="rv"),
    path('reports/summary/', main_report_summary, name="summary"),
    path('reports/<str:production_line>/', report_view, name="rvp"),
    path('reports/delete/<pk>/', delete_view, name="delete"),
    path('reports/<str:production_line>/<pk>/update',
         ReportUpdateView.as_view(), name="update"),
    path('reports/generate/pdf/', generate_problems_in_pdf, name='pdf'),
]
