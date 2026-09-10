# 🎯 REWRITE YOUR LINK IN modern6/urls.py TO LOOK EXACTLY LIKE THIS:
from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard Hero Cockpit Landing Home Page
    path('<slug:slug>/', views.modern6_agency_storefront_view, name='modern6_agency_storefront'),

    path('<slug:slug>/property/<int:pk>/', views.modern6_property_detail_view, name='modern6_property_detail'),


    # Inbound Slidedown Form Brief Box Intake
    path('<slug:slug>/book-tour/', views.modern6_book_property_tour, name='modern6_book_property_tour'),
]
