from urllib.parse import parse_qs, urlparse

from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def media_url(file_field):
    if not file_field:
        return ""

    value = file_field.name
    if value.startswith(("http://", "https://")):
        return value
    if value.startswith("church/"):
        return static(value)
    return file_field.url


def youtube_video_id(url):
    if not url:
        return ""

    parsed_url = urlparse(url)
    host = parsed_url.netloc.lower().replace("www.", "")
    path_parts = [part for part in parsed_url.path.split("/") if part]

    if host == "youtu.be" and path_parts:
        return path_parts[0]
    elif host.endswith("youtube.com"):
        if path_parts[:1] == ["watch"]:
            return parse_qs(parsed_url.query).get("v", [""])[0]
        elif path_parts[:1] in (["embed"], ["shorts"], ["live"]) and len(path_parts) > 1:
            return path_parts[1]

    return ""


def youtube_embed_url(url):
    video_id = youtube_video_id(url)
    return f"https://www.youtube.com/embed/{video_id}" if video_id else ""


def iframe_embed_url(url):
    return youtube_embed_url(url) or url


def youtube_thumbnail_url(url):
    video_id = youtube_video_id(url)
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else ""


class SiteProfile(models.Model):
    church_name = models.CharField(max_length=120, default="St. Bartholomew's")
    church_subtitle = models.CharField(max_length=120, default="Anglican Church Enugu.")
    logo_path = models.CharField(max_length=255, default="church/images/images.png")
    welcome_heading = models.CharField(max_length=160, default="Welcome to the Fountain of Purity")
    welcome_text = models.TextField()
    footer_tagline = models.CharField(max_length=180, default="Raising a worshipping, word-grounded, and Christ-centered community.")
    contact_email = models.EmailField(default="info@gracechurch.org")
    contact_phone = models.CharField(max_length=40, blank=True, default="")
    address = models.CharField(max_length=180, default="Enugu, Nigeria")
    office_hours = models.CharField(max_length=140, blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    whatsapp_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Site profile"
        verbose_name_plural = "Site profile"

    def __str__(self):
        return self.church_name


class Slide(models.Model):
    title = models.CharField(max_length=120)
    image_path = models.FileField(
        upload_to="slides/images/",
        max_length=500,
        help_text="Upload an image for this slide. Used when no video is uploaded.",
    )
    video_path = models.FileField(
        upload_to="slides/videos/",
        max_length=500,
        blank=True,
        help_text="Optional. Upload a short video. If set, the video is shown instead of the image.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return media_url(self.image_path)

    @property
    def video_url(self):
        return media_url(self.video_path)


class CoreValue(models.Model):
    title = models.CharField(max_length=120)
    detail = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class FaithCardGrid(models.Model):
    title = models.CharField(max_length=120)
    content = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Faith card"
        verbose_name_plural = "Faith cards"

    def __str__(self):
        return self.title


class FaithCardDetail(models.Model):
    grid = models.ForeignKey(FaithCardGrid, related_name="details", on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField(help_text="Enter each bullet point on a new line.")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(fields=["grid"], name="unique_faith_card_detail_per_grid")
        ]

    def __str__(self):
        return self.title

    def content_lines(self):
        return [line.strip() for line in self.content.splitlines() if line.strip()]


class WeeklyActivity(models.Model):
    day = models.CharField(max_length=20)
    activity = models.CharField(max_length=120)
    time = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Weekly activities"

    def __str__(self):
        return f"{self.day}: {self.activity}"


class LiveService(models.Model):
    title = models.CharField(max_length=120, default="Live services on YouTube")
    video_url = models.URLField(
        default="https://www.youtube.com/shorts/URXsWWWoTfk",
        help_text=(
            "Paste the live service video link. YouTube watch, shorts, live, "
            "and embed links are converted automatically."
        ),
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        return iframe_embed_url(self.video_url)


class ClergyProfile(models.Model):
    name = models.CharField(max_length=120)
    position = models.CharField(max_length=120)
    image = models.FileField(upload_to="clergy/images/", max_length=500)
    is_lead_pastor = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-is_lead_pastor", "order", "id"]

    def __str__(self):
        return f"{self.name} - {self.position}"

    @property
    def image_url(self):
        return media_url(self.image)


class PreacherMessage(models.Model):
    section_title = models.CharField(max_length=120, default="Preachers Desk")
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, blank=True)
    body = models.TextField()
    image_path = models.CharField(max_length=255, default="church/images/worshippers.jfif")
    preacher_name = models.CharField(max_length=120, default="Preacher Name")
    preacher_image = models.FileField(
        upload_to="preachers/images/",
        max_length=500,
        blank=True,
        default="church/images/worshippers.jfif",
        help_text="Small head image shown beside the message.",
    )
    date_posted = models.DateField(default=timezone.now)
    youtube_url = models.URLField(
        blank=True,
        default="",
        help_text="Optional YouTube page link for the message video.",
    )
    button_text = models.CharField(max_length=30, default="More")
    order = models.PositiveIntegerField(default=0)
    show_on_homepage = models.BooleanField(
        default=False,
        help_text="Show this message in the Preachers Desk section on the home page.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_posted", "order", "id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:180]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "preachers_desk_detail",
            kwargs={"pk": self.pk, "slug": self.slug or slugify(self.title) or "message"},
        )

    @property
    def preacher_image_url(self):
        return media_url(self.preacher_image)

    @property
    def youtube_embed_url(self):
        return youtube_embed_url(self.youtube_url)

    @property
    def youtube_thumbnail_url(self):
        return youtube_thumbnail_url(self.youtube_url)


class ChurchFamily(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    meaning = models.CharField(max_length=120, help_text="Example: Love Group")
    body = models.TextField()
    image = models.FileField(
        upload_to="families/images/",
        max_length=500,
        blank=True,
        default="church/images/worshippers.jfif",
    )
    male_leader_name = models.CharField(max_length=120, default="Male Group Leader")
    male_leader_image = models.FileField(
        upload_to="families/leaders/",
        max_length=500,
        blank=True,
        default="church/images/5883.jpg",
    )
    female_leader_name = models.CharField(max_length=120, default="Female Group Leader")
    female_leader_image = models.FileField(
        upload_to="families/leaders/",
        max_length=500,
        blank=True,
        default="church/images/13338.jpg",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Church families"

    def __str__(self):
        return f"{self.name} - {self.meaning}"

    @property
    def image_url(self):
        return media_url(self.image)

    @property
    def male_leader_image_url(self):
        return media_url(self.male_leader_image)

    @property
    def female_leader_image_url(self):
        return media_url(self.female_leader_image)


class ChurchFamilySliderImage(models.Model):
    family = models.ForeignKey(ChurchFamily, related_name="slider_images", on_delete=models.CASCADE)
    image = models.FileField(upload_to="families/slider/", max_length=500)
    write_up = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.family.name} slider image"

    @property
    def image_url(self):
        return media_url(self.image)


class Department(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    tagline = models.CharField(max_length=180, blank=True)
    hero_image = models.FileField(upload_to="departments/hero/", max_length=500, blank=True)
    introduction = models.TextField(help_text="A short paragraph explaining who this department is.")
    leader_name = models.CharField(max_length=120, blank=True)
    leader_title = models.CharField(max_length=120, default="Department Leader", blank=True)
    leader_image = models.FileField(upload_to="departments/leaders/", max_length=500, blank=True)
    executives_title = models.CharField(max_length=120, default="Executives", blank=True)
    executives_image = models.FileField(upload_to="departments/executives/", max_length=500, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def hero_image_url(self):
        return media_url(self.hero_image)

    @property
    def leader_image_url(self):
        return media_url(self.leader_image)

    @property
    def executives_image_url(self):
        return media_url(self.executives_image)


class DepartmentActivityPhoto(models.Model):
    department = models.ForeignKey(Department, related_name="activity_photos", on_delete=models.CASCADE)
    image = models.FileField(upload_to="departments/activities/", max_length=500)
    caption = models.CharField(max_length=140, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"{self.department.name} activity photo"

    @property
    def image_url(self):
        return media_url(self.image)


class DepartmentActivityArticle(models.Model):
    department = models.ForeignKey(Department, related_name="activity_articles", on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    frequency = models.CharField(max_length=40, default="Weekly")
    body = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.department.name}: {self.title}"


class DepartmentEvent(models.Model):
    department = models.ForeignKey(Department, related_name="events", on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    date = models.DateField()
    time = models.CharField(max_length=40, blank=True)
    venue = models.CharField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "order", "id"]

    def __str__(self):
        return f"{self.department.name}: {self.title}"
