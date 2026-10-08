from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from .models import (
    ChurchFamily,
    ChurchFamilySliderImage,
    ClergyProfile,
    CoreValue,
    Department,
    DepartmentActivityArticle,
    DepartmentActivityPhoto,
    DepartmentEvent,
    FaithCardDetail,
    FaithCardGrid,
    LiveService,
    PreacherMessage,
    SiteProfile,
    Slide,
    WeeklyActivity,
)


def home(request):
    weekly_activities_by_day = {}
    for activity in WeeklyActivity.objects.filter(is_active=True):
        weekly_activities_by_day.setdefault(activity.day, []).append(activity)

    weekly_activities = [
        {"day": day, "activities": activities}
        for day, activities in weekly_activities_by_day.items()
    ]

    context = {
        "site_profile": SiteProfile.objects.first(),
        "slides": Slide.objects.filter(is_active=True),
        "core_values": CoreValue.objects.filter(is_active=True),
        "faith_cards": FaithCardGrid.objects.filter(is_active=True).prefetch_related(
            Prefetch("details", queryset=FaithCardDetail.objects.filter(is_active=True))
        ),
        "weekly_activities": weekly_activities,
        "live_service": LiveService.objects.filter(is_active=True).first(),
        "preacher_message": PreacherMessage.objects.filter(
            is_active=True,
            show_on_homepage=True,
        ).first(),
    }
    return render(request, 'church/home.html', context)


def our_history(request):
    return render(request, 'church/our_history.html', {"site_profile": SiteProfile.objects.first()})


def mission_vision(request):
    return render(request, 'church/mission_vision.html', {"site_profile": SiteProfile.objects.first()})


def clergies(request):
    clergy_profiles = list(ClergyProfile.objects.filter(is_active=True))
    lead_pastor = next((profile for profile in clergy_profiles if profile.is_lead_pastor), None)

    if lead_pastor is None and clergy_profiles:
        lead_pastor = clergy_profiles[0]

    other_pastors = [
        profile
        for profile in clergy_profiles
        if lead_pastor is None or profile.id != lead_pastor.id
    ]

    return render(
        request,
        'church/clergies.html',
        {
            "site_profile": SiteProfile.objects.first(),
            "lead_pastor": lead_pastor,
            "other_pastors": other_pastors,
        },
    )


def church_families(request):
    slider_images = ChurchFamilySliderImage.objects.filter(is_active=True)

    return render(
        request,
        "church/church_families.html",
        {
            "site_profile": SiteProfile.objects.first(),
            "families": ChurchFamily.objects.filter(is_active=True).prefetch_related(
                Prefetch("slider_images", queryset=slider_images)
            ),
        },
    )


def contact(request):
    return render(request, "church/contact.html", {"site_profile": SiteProfile.objects.first()})


def preachers_desk(request, pk=None, slug=None):
    messages = PreacherMessage.objects.filter(is_active=True)

    if pk is None:
        message = messages.first()
    else:
        message = get_object_or_404(messages, pk=pk)

    return render(
        request,
        "church/preachers_desk.html",
        {
            "site_profile": SiteProfile.objects.first(),
            "message": message,
            "messages": messages,
        },
    )


def department_detail(request, slug):
    department = get_object_or_404(
        Department.objects.prefetch_related(
            Prefetch("activity_photos", queryset=DepartmentActivityPhoto.objects.filter(is_active=True)),
            Prefetch("activity_articles", queryset=DepartmentActivityArticle.objects.filter(is_active=True)),
            Prefetch("events", queryset=DepartmentEvent.objects.filter(is_active=True)),
        ),
        slug=slug,
        is_active=True,
    )

    return render(
        request,
        "church/department_detail.html",
        {
            "site_profile": SiteProfile.objects.first(),
            "department": department,
        },
    )
