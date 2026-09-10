from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")


class EducationTest(TestCase):

    def setUp(self):
        self.education = Education.objects.create(
            institution="SMA Pradita Dirgantara",
            level="senior-high",
            entry_year=2022,
            graduation_year=2025,
            gpa="94.48",
            utbk_score=783,
            logo_path="img/education/pradita.png",
            experience_anchor="sma",
            order=1,
            is_current=False,
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTemplateUsed(
            response,
            "education.html",
        )

    def test_education_data_appears_on_page(self):

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "SMA Pradita Dirgantara",
        )

        self.assertContains(
            response,
            "Senior High School",
        )

        self.assertContains(
            response,
            "783",
        )

    def test_education_empty_state(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Belum ada data pendidikan yang ditambahkan.",
        )

    def test_education_string_representation(self):

        self.assertEqual(
            str(self.education),
            "SMA Pradita Dirgantara",
        )
