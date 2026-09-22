from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education, Project
from django.contrib.auth.models import User


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

    def test_education_json_endpoint(self):
        response = self.client.get(reverse("main:get_education_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )

        data = response.json()

        self.assertEqual(len(data), 1)
        self.assertEqual(
            data[0]["fields"]["institution"],
            "SMA Pradita Dirgantara",
        )

    def test_create_education(self):
        response = self.client.post(
            reverse("main:create_education"),
            {
                "institution": "Universitas Indonesia",
                "level": "undergraduate",
                "entry_year": 2025,
                "graduation_year": 2029,
                "gpa": "3.01",
                "utbk_score": "",
                "logo_path": "img/education/ui.png",
                "experience_anchor": "college",
                "order": 2,
                "is_current": "on",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Education.objects.filter(institution="Universitas Indonesia").exists()
        )

    def test_update_education(self):
        response = self.client.post(
            reverse(
                "main:update_education",
                args=[self.education.id],
            ),
            {
                "institution": "SMA Pradita Dirgantara",
                "level": "senior-high",
                "entry_year": 2022,
                "graduation_year": 2025,
                "gpa": "95.00",
                "utbk_score": 790,
                "logo_path": "img/education/pradita.png",
                "experience_anchor": "sma",
                "order": 1,
                "is_current": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.education.refresh_from_db()

        self.assertEqual(
            str(self.education.gpa),
            "95.00",
        )

        self.assertEqual(
            self.education.utbk_score,
            790,
        )

    def test_delete_education(self):
        response = self.client.post(
            reverse(
                "main:delete_education",
                args=[self.education.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Education.objects.filter(id=self.education.id).exists())


class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rheza",
            password="testpass123",
        )

    def test_login(self):
        response = self.client.post(
            reverse("main:login"),
            {
                "username": "rheza",
                "password": "testpass123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)


    def test_logout(self):
        self.client.login(
            username="rheza",
            password="testpass123",
        )

        response = self.client.get(
            reverse("main:logout")
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            "_auth_user_id" in self.client.session
        )
    
    def test_toggle_star_project(self):
        project = Project.objects.create(
            title="Portfolio Website",
            description="Website portfolio pribadi.",
            tech_stack="Django",
            project_url="",
            project_image_url="",
        )

        self.client.login(
            username="rheza",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "main:toggle_star",
                args=[project.id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            project.starred_by.filter(
                id=self.user.id
            ).exists()
        )

        response = self.client.post(
            reverse(
                "main:toggle_star",
                args=[project.id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            project.starred_by.filter(
                id=self.user.id
            ).exists()
        )
    
    def test_anonymous_cannot_create_project(self):
        response = self.client.get(
            reverse("main:create_project")
        )

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/login/",
            response.url,
        )