from django.test import TestCase

from .models import Department, FaithCardDetail, FaithCardGrid


class FaithCardModelsTest(TestCase):
    def test_create_faith_card_grid_and_detail_items(self):
        grid = FaithCardGrid.objects.create(title="Worship", content="Join us in worship", order=1)
        detail = FaithCardDetail.objects.create(
            grid=grid,
            title="Sunday Worship",
            content="Praise and prayer\nWord and Sacrament",
            order=1,
        )

        self.assertEqual(str(grid), "Worship")
        self.assertEqual(list(grid.details.all()), [detail])
        self.assertEqual(detail.content_lines(), ["Praise and prayer", "Word and Sacrament"])


class DepartmentPageTest(TestCase):
    def test_department_detail_page_renders_reusable_sections(self):
        Department.objects.filter(slug="the-choir").update(
            introduction="The choir leads the church in worship."
        )

        response = self.client.get("/departments/the-choir/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Choir")
        self.assertContains(response, "Who We Are")
        self.assertContains(response, "Weekly And Monthly Activities")
        self.assertContains(response, "Upcoming Events")


class ContactPageTest(TestCase):
    def test_contact_page_renders_contact_and_social_sections(self):
        response = self.client.get("/contact/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Us")
        self.assertContains(response, "Get In Touch")
        self.assertContains(response, "Social Media")
        self.assertContains(response, "Get Directions")
        self.assertContains(response, "Off Ogui Road")
