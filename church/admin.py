from django.contrib import admin

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
    PreacherMessage,
    SiteProfile,
    Slide,
    WeeklyActivity,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("church_name", "church_subtitle", "logo_path")}),
        ("Homepage Welcome", {"fields": ("welcome_heading", "welcome_text")}),
        ("Footer", {"fields": ("footer_tagline",)}),
        ("Contact", {"fields": ("contact_email", "contact_phone", "address", "office_hours")}),
        ("Social media", {"fields": ("facebook_url", "instagram_url", "youtube_url", "whatsapp_url")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Slide content", {"fields": ("title", "image_path", "video_path")}),
        ("Display", {"fields": ("order", "is_active")}),
    )
    list_display = ("title", "media_type", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title",)

    @admin.display(description="Media")
    def media_type(self, obj):
        return "Video" if obj.video_path else "Image"


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "detail")


class FaithCardDetailInline(admin.TabularInline):
    model = FaithCardDetail
    fields = ("title", "content")
    extra = 1
    max_num = 1
    can_delete = False


@admin.register(FaithCardGrid)
class FaithCardGridAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "content", "details__title", "details__content")
    inlines = (FaithCardDetailInline,)


@admin.register(WeeklyActivity)
class WeeklyActivityAdmin(admin.ModelAdmin):
    list_display = ("day", "activity", "time", "order", "is_active")
    list_filter = ("day", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("day", "activity", "time")


@admin.register(ClergyProfile)
class ClergyProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Pastor details", {"fields": ("name", "position", "image")}),
        ("Display", {"fields": ("is_lead_pastor", "order", "is_active")}),
    )
    list_display = ("name", "position", "is_lead_pastor", "order", "is_active")
    list_filter = ("is_lead_pastor", "is_active")
    list_editable = ("is_lead_pastor", "order", "is_active")
    search_fields = ("name", "position")


class DepartmentActivityPhotoInline(admin.TabularInline):
    model = DepartmentActivityPhoto
    extra = 1
    fields = ("image", "caption", "order", "is_active")


class DepartmentActivityArticleInline(admin.StackedInline):
    model = DepartmentActivityArticle
    extra = 1
    fields = ("title", "frequency", "body", "order", "is_active")


class DepartmentEventInline(admin.StackedInline):
    model = DepartmentEvent
    extra = 1
    fields = ("title", "date", "time", "venue", "description", "order", "is_active")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Department page", {"fields": ("name", "slug", "tagline", "hero_image", "introduction")}),
        ("Leader and executives", {"fields": ("leader_name", "leader_title", "leader_image", "executives_title", "executives_image")}),
        ("Display", {"fields": ("order", "is_active")}),
    )
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "tagline", "introduction", "leader_name")
    inlines = (
        DepartmentActivityPhotoInline,
        DepartmentActivityArticleInline,
        DepartmentEventInline,
    )


@admin.register(PreacherMessage)
class PreacherMessageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Message", {"fields": ("section_title", "title", "slug", "body")}),
        ("Preacher", {"fields": ("preacher_name", "preacher_image", "date_posted")}),
        ("Video", {"fields": ("youtube_url",)}),
        ("Homepage", {"fields": ("show_on_homepage", "image_path", "button_text")}),
        ("Display", {"fields": ("order", "is_active")}),
    )
    list_display = ("title", "preacher_name", "date_posted", "show_on_homepage", "order", "is_active")
    list_editable = ("show_on_homepage", "order", "is_active")
    list_filter = ("show_on_homepage", "is_active", "date_posted")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("section_title", "title", "body", "preacher_name")


class ChurchFamilySliderImageInline(admin.StackedInline):
    model = ChurchFamilySliderImage
    extra = 1
    fields = ("image", "write_up", "order", "is_active")


@admin.register(ChurchFamily)
class ChurchFamilyAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Family content", {"fields": ("name", "slug", "meaning", "body")}),
        ("Group leaders", {"fields": ("male_leader_name", "male_leader_image", "female_leader_name", "female_leader_image")}),
        ("Display", {"fields": ("order", "is_active")}),
    )
    list_display = ("name", "meaning", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "meaning", "body", "male_leader_name", "female_leader_name")
    inlines = (ChurchFamilySliderImageInline,)
