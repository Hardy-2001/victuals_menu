from django.urls import path
from . import views

urlpatterns = [
    # 🏫 INSTITUTION store storefront homepage cockpits track
    path('<slug:slug>/', views.modern7_homepage_view, name='modern7_homepage'),

    # ℹ️ CAMPUS overview history sheets tracks
    path('<slug:slug>/about/', views.modern7_aboutpage_view, name='modern7_aboutpage'),

    # ❓ CAMPUS FAQ help center accordion grids track
    path('<slug:slug>/faq/', views.modern7_faqpage_view, name='modern7_faqpage'),

    # 📞 ADMISSIONS direct channel coordinates contact fields tracks
    path('<slug:slug>/contact/', views.modern7_contactpage_view, name='modern7_contactpage'),

    # 🗂️ DYNAMIC course catalog gallery grids selection filters portfolio track
    path('<slug:slug>/courses/', views.modern7_coursepage_view, name='modern7_coursepage'),

    # 📑 LECTURE deep details specification review tab panels track
    path('<slug:slug>/course/<int:pk>/', views.modern7_course_detail_view, name='modern7_course_detail'),

    # 👨‍🏫 FACULTY board register roster view tracks
    path('<slug:slug>/instructors/', views.modern7_instructorpage_view, name='modern7_instructorpage'),

    # ==============================================================================
    # 📥 TRANSACTIONS processing intake post data engines
    # ==============================================================================
    path('<slug:slug>/contact/submit/', views.modern7_submit_contact_view, name='modern7_submit_contact'),
    path('<slug:slug>/review/submit/', views.modern7_submit_review_view, name='modern7_submit_review'),
]
