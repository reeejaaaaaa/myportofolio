from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education, Project
from django.contrib.auth.models import User, Group
from datetime import date


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2026, 1, 1),
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
        self.experience.ended_at = date(2026, 2, 1)
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

        self.admin = User.objects.create_superuser(
            username="admin",
            password="testpass123",
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
        self.client.force_login(self.admin)
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
        self.client.force_login(self.admin)
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
        self.client.force_login(self.admin)
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

        response = self.client.get(reverse("main:logout"))

        self.assertEqual(response.status_code, 302)

        self.assertFalse("_auth_user_id" in self.client.session)

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
        self.assertTrue(project.starred_by.filter(id=self.user.id).exists())

        response = self.client.post(
            reverse(
                "main:toggle_star",
                args=[project.id],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(project.starred_by.filter(id=self.user.id).exists())

    def test_anonymous_cannot_create_project(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/login/",
            response.url,
        )


class Tugas4Test(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user(
            username="regular",
            password="testpass123",
        )

        self.editor_user = User.objects.create_user(
            username="editor",
            password="testpass123",
        )

        self.superuser = User.objects.create_superuser(
            username="admin",
            password="testpass123",
        )

        editor_group = Group.objects.create(
            name="Editor",
        )

        self.editor_user.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            level="undergraduate",
            entry_year=2025,
            graduation_year=2029,
            gpa="3.50",
            logo_path="img/education/ui.png",
            experience_anchor="college-test",
            order=1,
            is_current=True,
        )

        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Website portfolio.",
            tech_stack="Django",
            project_url="",
            project_image_url="",
        )

        self.experience = Experience.objects.create(
            title="Asisten Dosen",
            description="Pengalaman mengajar.",
            category="part-time",
            started_at=date(2026, 1, 1),
            ended_at=None,
            education=self.education,
        )

        self.experience.projects.add(self.project)

    def test_anonymous_user_redirected_from_create(self):
        education_response = self.client.get(reverse("main:create_education"))

        experience_response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(
            education_response.status_code,
            302,
        )

        self.assertEqual(
            experience_response.status_code,
            302,
        )

        self.assertIn(
            "/login/",
            education_response.url,
        )

        self.assertIn(
            "/login/",
            experience_response.url,
        )

    def test_regular_user_cannot_modify_data(self):
        self.client.login(
            username="regular",
            password="testpass123",
        )

        create_response = self.client.get(reverse("main:create_experience"))

        update_response = self.client.get(
            reverse(
                "main:update_experience",
                args=[self.experience.id],
            )
        )

        delete_response = self.client.post(
            reverse(
                "main:delete_experience",
                args=[self.experience.id],
            )
        )

        self.assertEqual(
            create_response.status_code,
            403,
        )

        self.assertEqual(
            update_response.status_code,
            403,
        )

        self.assertEqual(
            delete_response.status_code,
            403,
        )

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.login(
            username="editor",
            password="testpass123",
        )

        update_response = self.client.get(
            reverse(
                "main:update_experience",
                args=[self.experience.id],
            )
        )

        create_response = self.client.get(reverse("main:create_experience"))

        delete_response = self.client.post(
            reverse(
                "main:delete_experience",
                args=[self.experience.id],
            )
        )

        self.assertEqual(
            update_response.status_code,
            200,
        )

        self.assertEqual(
            create_response.status_code,
            403,
        )

        self.assertEqual(
            delete_response.status_code,
            403,
        )

    def test_superuser_can_create_experience(self):
        self.client.login(
            username="admin",
            password="testpass123",
        )

        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Research Assistant",
                "description": "Mengerjakan penelitian.",
                "category": "research",
                "thumbnail": "",
                "started_at": "2026-02-01",
                "ended_at": "",
                "education": str(self.education.id),
                "projects": [str(self.project.id)],
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(Experience.objects.filter(title="Research Assistant").exists())

    def test_editor_can_update_experience(self):
        self.client.login(
            username="editor",
            password="testpass123",
        )

        response = self.client.post(
            reverse(
                "main:update_experience",
                args=[self.experience.id],
            ),
            {
                "title": "Updated Experience",
                "description": "Deskripsi baru.",
                "category": "part-time",
                "thumbnail": "",
                "started_at": "2026-01-01",
                "ended_at": "",
                "education": str(self.education.id),
                "projects": [str(self.project.id)],
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated Experience",
        )

    def test_regular_user_can_star_and_unstar_experience(self):
        self.client.login(
            username="regular",
            password="testpass123",
        )

        star_url = reverse(
            "main:toggle_star_experience",
            args=[self.experience.id],
        )

        response = self.client.post(star_url)

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertTrue(
            self.experience.starred_by.filter(id=self.regular_user.id).exists()
        )

        self.client.post(star_url)

        self.assertFalse(
            self.experience.starred_by.filter(id=self.regular_user.id).exists()
        )

    def test_anonymous_user_cannot_star_experience(self):
        response = self.client.post(
            reverse(
                "main:toggle_star_experience",
                args=[self.experience.id],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertIn(
            "/login/",
            response.url,
        )

    def test_experience_json_endpoint(self):
        self.experience.starred_by.add(self.regular_user)

        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )

        data = response.json()

        self.assertEqual(
            len(data),
            1,
        )

        self.assertEqual(
            data[0]["fields"]["title"],
            "Asisten Dosen",
        )

        response_text = response.content.decode("utf-8")

        self.assertIn(
            "regular",
            response_text,
        )

        self.assertNotIn(
            "testpass123",
            response_text,
        )

    def test_education_controls_follow_roles(self):
        self.client.login(
            username="regular",
            password="testpass123",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertNotContains(
            response,
            "Add Education",
        )

        self.assertNotContains(
            response,
            ">Edit<",
            html=False,
        )

        self.client.logout()

        self.client.login(
            username="editor",
            password="testpass123",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Edit",
        )

        self.assertNotContains(
            response,
            "Add Education",
        )

        self.client.logout()

        self.client.login(
            username="admin",
            password="testpass123",
        )

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "Add Education",
        )

        self.assertContains(
            response,
            "Edit",
        )

        self.assertContains(
            response,
            "Delete",
        )
