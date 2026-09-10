from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import (
    Modern7SchoolTenant,
    Modern7PlatformConfigDeck,
    Modern7CourseCategory,
    Modern7FacultyInstructor,
    Modern7CourseListing,
    Modern7StudentEnquiryLead,
    Modern7CourseReview
)


# ==============================================================================
# 🛰️ CORE VIEWS SECTOR 1: MULTI-TENANT GENERAL CONTROLLER PACK
# ==============================================================================

def get_tenant_context_or_404(slug):
    """
    🔒 SECURITY PROTOCOL SHARED ENGINE
    Queries the multi-tenant registry safely by slug path string text parameters.
    Returns (school_tenant, visual_config, system_categories) cleanly.
    """
    school_tenant = get_object_or_404(Modern7SchoolTenant, slug_path__iexact=slug, is_active_node=True)
    visual_config = get_object_or_404(Modern7PlatformConfigDeck, tenant_link=school_tenant)
    system_categories = Modern7CourseCategory.objects.filter(school_tenant=school_tenant)
    return school_tenant, visual_config, system_categories


def modern7_homepage_view(request, slug):
    """
    🏠 SCHOOL HOMEPAGE COCKPIT VIEW
    Streams look deck text rows, active courses, faculty, and scorable reviews.
    """
    # Initialize isolated context tracking markers cleanly
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    # Extract courses and faculty sharded purely to this institution row entry
    platform_courses = Modern7CourseListing.objects.filter(school_tenant=school_tenant, is_visible_on_catalog=True)[:6]
    platform_instructors = Modern7FacultyInstructor.objects.filter(school_tenant=school_tenant)[:4]

    # Gather scorable student feedback comments for this school's courses
    platform_reviews = Modern7CourseReview.objects.filter(
        target_course__school_tenant=school_tenant,
        is_approved_for_public=True
    )[:5]

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
        'platform_courses': platform_courses,
        'platform_instructors': platform_instructors,
        'platform_reviews': platform_reviews,
    }
    return render(request, 'modern7/index.html', context)


# ==============================================================================
# 🛰️ CORE VIEWS SECTOR 2: CAMPUS ABOUT, FAQ, & CONTACT DECK ENGINES
# ==============================================================================

def modern7_aboutpage_view(request, slug):
    """
    ℹ️ CAMPUS HISTORICAL MISSION VIEW
    Streams institutional story lines, custom values text blocks,
    and loops approved reviews into the inner sub-page layout cleanly.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    # Gather matching student reviews to support the about page feedback deck
    platform_reviews = Modern7CourseReview.objects.filter(
        target_course__school_tenant=school_tenant,
        is_approved_for_public=True
    )[:5]

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
        'platform_reviews': platform_reviews,
    }
    return render(request, 'modern7/about.html', context)


def modern7_faqpage_view(request, slug):
    """
    ❓ CAMPUS FAQ CENTER INTERACTIVE VIEW
    Pulls school config records and streams collapsible questions blocks.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
    }
    return render(request, 'modern7/faq.html', context)


def modern7_contactpage_view(request, slug):
    """
    📞 ADMISSIONS DESK COORDINATES VIEW
    Loads the campus address lines, embedded map frame row text scripts,
    and handles input lead tracking variables safely.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
    }
    return render(request, 'modern7/contact.html', context)


# ==============================================================================
# 🛰️ CORE VIEWS SECTOR 3: COURSE PORTFOLIOS, SELECTION FILTERS, & FACULTY BOARDS
# ==============================================================================

def modern7_coursepage_view(request, slug):
    """
    🗂️ DYNAMIC MULTI-PAGE COURSE DIRECTORY CATALOG GRID
    Processes live search queries and category slugs to filter course lists
    safely with zero cross-tenant leak lines.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    # Start with all active visible courses sharded purely to this institution row
    courses_queryset = Modern7CourseListing.objects.filter(school_tenant=school_tenant, is_visible_on_catalog=True)

    # 🔍 FILTER PROTOCOL A: Handle search bar keyword query entries
    search_query = request.GET.get('search_query', '').strip()
    if search_query:
        courses_queryset = courses_queryset.filter(
            Q(course_title__icontains=search_query) |
            Q(course_description_main__icontains=search_query)
        )

    # 📁 FILTER PROTOCOL B: Handle side category menu row selections
    category_slug = request.GET.get('category_slug', '').strip()
    if category_slug:
        courses_queryset = courses_queryset.filter(dynamic_category__category_slug__iexact=category_slug)

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
        'platform_courses': courses_queryset,
        'search_query': search_query,
        'selected_category_slug': category_slug,
    }
    return render(request, 'modern7/course.html', context)


def modern7_course_detail_view(request, slug, pk):
    """
    📑 LECTURE CORE SPEC REVIEW CANVAS VIEW
    Pulls specific course detail matrices, loads the assigned instructor profile,
    streams approved text reviews, and gathers sibling courses in the same category.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)

    # Pull target course row card index matching this school context safely
    course = get_object_or_404(Modern7CourseListing, pk=pk, school_tenant=school_tenant)

    # Gather sibling track rows in matching category buckets excluding self track row
    sister_courses = Modern7CourseListing.objects.filter(
        school_tenant=school_tenant,
        dynamic_category=course.dynamic_category,
        is_visible_on_catalog=True
    ).exclude(pk=course.pk)[:3]

    # Fetch approved public scorable review threads for this lecture module
    platform_reviews = course.course_reviews.filter(is_approved_for_public=True)

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
        'course': course,
        'sister_courses': sister_courses,
        'platform_reviews': platform_reviews,
    }
    return render(request, 'modern7/course_details.html', context)


def modern7_instructorpage_view(request, slug):
    """
    👨‍🏫 FACULTY BOARD REGISTER DIRECTORY VIEW
    Streams all onboarded teacher portfolio entries sharded under this tenant code.
    """
    school_tenant, visual_config, system_categories = get_tenant_context_or_404(slug)
    platform_instructors = Modern7FacultyInstructor.objects.filter(school_tenant=school_tenant)

    context = {
        'active_tenant': school_tenant,
        'platform_config': visual_config,
        'course_categories': system_categories,
        'platform_instructors': platform_instructors,
    }
    return render(request, 'modern7/instructor.html', context)


# ==============================================================================
# 🛰️ CORE VIEWS SECTOR 4: TRANSACTIONS INTAKE SUBMITTERS (POST DATA ENGINES)
# ==============================================================================

def modern7_submit_contact_view(request, slug):
    """
    📩 STUDENT LEAD INTAKE TRANSACTIONS ENGINE
    Processes text fields from contact forms, saves them securely to the database,
    and returns a clean success response banner flash message.
    """
    school_tenant = get_object_or_404(Modern7SchoolTenant, slug_path__iexact=slug, is_active_node=True)

    if request.method == 'POST':
        client_name = request.POST.get('client_name', '').strip()
        client_email = request.POST.get('client_email', '').strip()
        lead_subject = request.POST.get('lead_subject', '').strip()
        message_content = request.POST.get('message_content', '').strip()

        if client_name and client_email and message_content:
            # Inject data values straight into your isolated tenant mailbox table rows
            Modern7StudentEnquiryLead.objects.create(
                school_tenant=school_tenant,
                client_name=client_name,
                client_email=client_email,
                lead_subject=lead_subject,
                message_content=message_content
            )
            messages.success(request,
                             f"Thank you {client_name}! Your admissions enquiry has been transmitted successfully to the registrar desk.")
        else:
            messages.error(request, "Submission Failed. Please verify all mandatory form input variables text fields.")

    return redirect('modern7_contactpage', slug=school_tenant.slug_path)


def modern7_submit_review_view(request, slug):
    """
    ⭐️ LIVE SCORABLE REVIEWS PROCESSOR
    Captures course review scores and commentary posts straight from details view form tables.
    """
    school_tenant = get_object_or_404(Modern7SchoolTenant, slug_path__iexact=slug, is_active_node=True)

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_name = request.POST.get('student_name', '').strip()
        student_email = request.POST.get('student_email', '').strip()
        rating_score = request.POST.get('rating_score', '5')
        feedback_comment_text = request.POST.get('feedback_comment_text', '').strip()

        # Verify the course index item belongs purely to this tenant context node safely
        target_course = get_object_or_404(Modern7CourseListing, pk=course_id, school_tenant=school_tenant)

        if student_name and student_email and feedback_comment_text:
            Modern7CourseReview.objects.create(
                target_course=target_course,
                student_name=student_name,
                student_email=student_email,
                rating_score=int(rating_score),
                feedback_comment_text=feedback_comment_text,
                is_approved_for_public=True  # Automatically active for student showcase fronts boards row tracks
            )
            messages.success(request,
                             f"Thank you {student_name}! Your verified course review has been saved successfully.")
            return redirect('modern7_course_detail', slug=school_tenant.slug_path, pk=target_course.id)

    messages.error(request, "Review submission could not be verified. Please reload form layers.")
    return redirect('modern7_coursepage', slug=school_tenant.slug_path)

