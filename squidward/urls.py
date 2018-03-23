from django.urls import path, include
from . import views

urlpatterns = [
    path('',
         views.index, name='index'),

    path('reports/',
         views.report_index, name='report_index'),

    path('reports/pptp/',
         views.report_index_pptp, name='report_index_pptp'),

    path('reports/pptp/<int:fromdate>_<int:untildate>/<str:user_ip>',
         views.pptp_manual_user, name='pptp_manual_user'),

    path('reports/top/week/',
         views.report_top_week, name='report_top_week'),

    path('reports/top/month/',
         views.report_top_month, name='report_top_month'),

    path('reports/manual/<int:fromdate>_<int:untildate>/',
         views.report_manual, name='report_manual'),

    path('reports/manual/<int:fromdate>_<int:untildate>/<str:user_ip>/',
         views.report_manual_user, name='report_manual_user'),



]