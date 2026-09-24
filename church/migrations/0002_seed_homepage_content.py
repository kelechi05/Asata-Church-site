from django.db import migrations


def seed_homepage_content(apps, schema_editor):
    SiteProfile = apps.get_model("church", "SiteProfile")
    Slide = apps.get_model("church", "Slide")
    Service = apps.get_model("church", "Service")
    ServiceTime = apps.get_model("church", "ServiceTime")
    CoreValue = apps.get_model("church", "CoreValue")
    WeeklyActivity = apps.get_model("church", "WeeklyActivity")
    PreacherMessage = apps.get_model("church", "PreacherMessage")

    SiteProfile.objects.get_or_create(
        church_name="St. Bartholomew's",
        defaults={
            "church_subtitle": "Anglican Church Enugu.",
            "logo_path": "church/images/images.png",
            "welcome_heading": "Welcome to the Fountain of Purity",
            "welcome_text": (
                "We are a caring and united church family devoted to sharing the Gospel of Jesus Christ, "
                "nurturing spiritual growth, and transforming lives. Through Christ's love, we serve our "
                "community with compassion, integrity, and purpose, striving to reflect His light and make "
                "a lasting impact in the world around us."
            ),
            "footer_tagline": "Raising a worshipping, word-grounded, and Christ-centered community.",
            "contact_email": "info@gracechurch.org",
            "address": "Enugu, Nigeria",
        },
    )

    slides = [
        ("Christ Our Hope\nLiving for His Glory", "church/images/St.-Barts-Asata-Enugu.png"),
        ("Growing Together in Faith", "https://images.unsplash.com/photo-1478146896981-b80fe463b330"),
        ("Join Us This Sunday", "https://images.unsplash.com/photo-1492724441997-5dc865305da7"),
    ]
    for order, (title, image_path) in enumerate(slides):
        Slide.objects.get_or_create(title=title, defaults={"image_path": image_path, "order": order})

    service, _ = Service.objects.get_or_create(
        title="Our Service",
        defaults={
            "description": (
                "Join us every Sunday for our weekly vibrant worship service. Where we gather to praise, "
                "hear His Word, and fellowship with one another in faith."
            ),
            "image_path": "church/images/worshippers.jfif",
        },
    )
    for order, time in enumerate(["6:30am", "8:30am"]):
        ServiceTime.objects.get_or_create(service=service, time=time, defaults={"order": order})

    core_values = [
        ("Bible-Based Foundation", "Rooted in the Scripture as the ultimate authority."),
        ("Spiritually Dynamic", "Empowered by the Holy Spirit."),
        ("United and Disciplined", "Fostering unity within the Anglican Communion and maintaining structural discipline."),
        ("Pragmatic Evangelism", "Actively spreading the gospel in practical, relevant ways."),
        ("Social Welfare/Holistic Ministry", "Engaging in community development and social support."),
        ("Self-Supporting", "Aiming for financial and structural independence."),
        ("Love of Christ", "Reflecting Jesus's love in all actions."),
    ]
    for order, (title, detail) in enumerate(core_values):
        CoreValue.objects.get_or_create(title=title, defaults={"detail": detail, "order": order})

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    activities = [
        ("ACM Meetings", "6:30am"),
        ("EFAC Meeting", "8:30am"),
        ("PCC 2nd Week", "5:00pm"),
        ("Choir Practice", "6:00pm"),
    ]
    order = 0
    for day in days:
        for activity, time in activities:
            WeeklyActivity.objects.get_or_create(
                day=day,
                activity=activity,
                defaults={"time": time, "order": order},
            )
            order += 1

    PreacherMessage.objects.get_or_create(
        title="As we move towards the Mark",
        defaults={
            "section_title": "Preachers Desk",
            "body": (
                "Join us every Sunday for our weekly vibrant worship service. Where we gather to praise, "
                "hear His Word, and fellowship with one another in faith."
            ),
            "image_path": "church/images/worshippers.jfif",
            "button_text": "More",
        },
    )


def unseed_homepage_content(apps, schema_editor):
    for model_name in [
        "PreacherMessage",
        "WeeklyActivity",
        "CoreValue",
        "ServiceTime",
        "Service",
        "Slide",
        "SiteProfile",
    ]:
        apps.get_model("church", model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("church", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_homepage_content, unseed_homepage_content),
    ]
