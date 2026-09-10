from django.urls import path
from . import views

urlpatterns = [
    # 🛰️ Master Terminal Portfolio Web Showcase Route (e.g., /modern5/ismail/)
    path('<slug:slug>/', views.modern5_portfolio_storefront_view, name='modern5_portfolio_storefront'),

    # 📥 Active Client Contract Brief Mailbox Submission Receiver Link
    path('<slug:slug>/submit-brief/', views.modern5_submit_contract_brief, name='modern5_submit_contract_brief'),
]
