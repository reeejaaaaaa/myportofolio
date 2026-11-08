import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner",
            password="test-password",
            email="owner@example.com",
        )

        self.visitor = User.objects.create_user(
            username="visitor",
            password="test-password",
        )

        self.project = Project.objects.create(
            title="Portfolio",
            description="My website",
            tech_stack="Django",
        )

        self.list_url = reverse(
            "api:project-list"
        )

        self.detail_url = reverse(
            "api:project-detail",
            args=[self.project.id],
        )

        self.star_url = reverse(
            "api:project-star",
            args=[self.project.id],
        )

        self.payload = {
            "title": "New project",
            "description": "A useful app",
            "tech_stack": "Python",
            "project_url": "https://example.com/",
            "project_image_url": "",
        }


    def test_public_list_and_detail(self):
        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["id"],
            str(self.project.id),
        )

        self.assertFalse(
            response.data[0]["is_starred"]
        )

        self.assertNotIn(
            "fields",
            response.data[0],
        )

        self.assertEqual(
            self.client.get(
                self.detail_url
            ).status_code,
            status.HTTP_200_OK,
        )


    def test_search_and_empty_results(self):
        response = self.client.get(
            self.list_url,
            {
                "title": "PORT",
            },
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        response = self.client.get(
            self.list_url,
            {
                "title": "not-found",
            },
        )

        self.assertEqual(
            response.data,
            [],
        )


    def test_missing_project(self):
        url = reverse(
            "api:project-detail",
            args=[uuid.uuid4()],
        )

        self.assertEqual(
            self.client.get(
                url
            ).status_code,
            status.HTTP_404_NOT_FOUND,
        )


    def test_guest_and_visitor_cannot_write(self):
        for user in (
            None,
            self.visitor,
        ):
            self.client.force_authenticate(
                user=user
            )

            self.assertEqual(
                self.client.post(
                    self.list_url,
                    self.payload,
                    format="json",
                ).status_code,
                403,
            )

            self.assertEqual(
                self.client.patch(
                    self.detail_url,
                    {
                        "title": "Changed"
                    },
                    format="json",
                ).status_code,
                403,
            )

            self.assertEqual(
                self.client.delete(
                    self.detail_url
                ).status_code,
                403,
            )

        self.assertEqual(
            Project.objects.count(),
            1,
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.title,
            "Portfolio",
        )


    def test_owner_can_create(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Project.objects.filter(
                pk=response.data["id"]
            ).exists()
        )


    def test_validation(self):
        self.client.force_authenticate(
            user=self.owner
        )

        for changes, field in [
            (
                {
                    "title": "   "
                },
                "title",
            ),
            (
                {
                    "title":
                        '<img src="x" '
                        'onerror="alert(1)">'
                },
                "title",
            ),
            (
                {
                    "project_url":
                        "javascript:alert(1)"
                },
                "project_url",
            ),
        ]:
            response = self.client.post(
                self.list_url,
                {
                    **self.payload,
                    **changes,
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

            self.assertIn(
                field,
                response.data,
            )

        self.assertEqual(
            Project.objects.count(),
            1,
        )


    def test_patch_put_and_delete(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.patch(
            self.detail_url,
            {
                "title": "Changed"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.project.refresh_from_db()

        self.assertEqual(
            self.project.description,
            "My website",
        )

        response = self.client.put(
            self.detail_url,
            {
                "title": "Incomplete"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = self.client.delete(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            response.content,
            b"",
        )

        self.assertFalse(
            Project.objects.filter(
                id=self.project.id
            ).exists()
        )


    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(
                self.star_url
            ).status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.client.force_authenticate(
            user=self.visitor
        )

        response = self.client.post(
            self.star_url
        )

        self.assertTrue(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            1,
        )

        response = self.client.post(
            self.star_url
        )

        self.assertFalse(
            response.data["is_starred"]
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )


    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(
            user=self.owner
        )

        response = self.client.post(
            self.list_url,
            {
                **self.payload,
                "star_count": 99,
                "is_starred": True,
                "starred_by_names": "forged",
                "starred_by": [
                    self.visitor.id
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["star_count"],
            0,
        )

        self.assertFalse(
            response.data["is_starred"]
        )


    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()

        self.visitor.groups.add(
            Group.objects.create(
                name="Editor"
            )
        )

        self.client.force_authenticate(
            user=self.visitor
        )

        response = self.client.patch(
            self.detail_url,
            {
                "title": "Changed"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )


    def test_wrong_method(self):
        self.client.force_authenticate(
            user=self.owner
        )

        self.assertEqual(
            self.client.delete(
                self.list_url
            ).status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(
            enforce_csrf_checks=True
        )

        self.assertTrue(
            client.login(
                username="owner",
                password="test-password",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertEqual(
            Project.objects.count(),
            1,
        )


    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(
            enforce_csrf_checks=True
        )

        client.login(
            username="owner",
            password="test-password",
        )

        page = client.get(
            self.list_url,
            HTTP_ACCEPT="text/html",
        )

        self.assertEqual(
            page.status_code,
            status.HTTP_200_OK,
        )

        token = (
            client.cookies[
                "csrftoken"
            ].value
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

class ExperienceAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        from main.models import Education, Experience

        cls.owner = User.objects.create_superuser(
            username="experience-owner", password="test-password",
            email="owner@example.com",
        )
        cls.visitor = User.objects.create_user(
            username="experience-visitor", password="test-password",
        )
        cls.editor = User.objects.create_user(username="experience-editor")
        cls.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])
        cls.education = Education.objects.create(
            institution="University", level="undergraduate",
            entry_year=2024, graduation_year=2028, experience_anchor="api-test",
        )
        cls.project = Project.objects.create(
            title="Related project", description="App", tech_stack="Python",
        )
        cls.experience = Experience.objects.create(
            title="Research Assistant", description="Research work",
            category="research", started_at="2026-01-01",
            education=cls.education,
        )
        cls.experience.projects.add(cls.project)
        cls.list_url = reverse("api:experience-list")
        cls.detail_url = reverse("api:experience-detail", args=[cls.experience.id])
        cls.star_url = reverse("api:experience-star", args=[cls.experience.id])
        cls.payload = {
            "title": "New experience", "description": "Useful work",
            "category": "internship", "started_at": "2026-02-01",
            "ended_at": None, "thumbnail": "", "education": None,
            "projects": [str(cls.project.id)],
        }

    def test_public_representation_and_search(self):
        response = self.client.get(self.list_url, {"q": "RESEARCH"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        item = response.data[0]
        self.assertNotIn("fields", item)
        self.assertEqual(item["id"], str(self.experience.id))
        self.assertEqual(item["started_at"], "2026-01-01")
        self.assertTrue(item["is_ongoing"])
        self.assertFalse(item["is_starred"])
        self.assertEqual(item["education_name"], "University")
        self.assertEqual(item["project_details"], [
            {"id": str(self.project.id), "title": self.project.title}
        ])
        self.assertEqual(self.client.get(self.list_url, {"q": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.head(self.detail_url).status_code, 200)

    def test_guest_and_regular_user_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"title": "Forbidden"}),
                ("delete", self.detail_url, {}),
            ):
                with self.subTest(user=user, method=method):
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Research Assistant")

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.patch(
            self.detail_url, {"title": "Edited"}, format="json",
        ).status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited")
        self.assertEqual(self.experience.description, "Research work")
        self.assertEqual(self.client.put(
            self.detail_url, self.payload, format="json",
        ).status_code, 200)
        self.assertEqual(self.client.post(
            self.list_url, self.payload, format="json",
        ).status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_owner_crud_and_read_only_fields(self):
        from main.models import Experience

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by": [self.visitor.id], "education_name": "Forged",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["education_name"], "")
        item = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(list(item.projects.all()), [self.project])
        url = reverse("api:experience-detail", args=[item.id])
        response = self.client.patch(url, {
            "ended_at": "2026-03-01", "projects": [],
            "education": str(self.education.id),
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_ongoing"])
        self.assertEqual(response.data["projects"], [])
        self.assertEqual(response.data["education_name"], "University")
        self.assertEqual(self.client.put(url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(url, self.payload, format="json").status_code, 200)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=item.id).exists())

    def test_validation_and_sanitization(self):
        self.client.force_authenticate(user=self.owner)
        for field, value in (
            ("title", "<br>"), ("description", "<br>"),
            ("thumbnail", "javascript:alert(1)"), ("started_at", "invalid"),
            ("category", "invalid"), ("education", str(uuid.uuid4())),
            ("projects", [str(uuid.uuid4())]),
        ):
            with self.subTest(field=field):
                response = self.client.post(self.list_url, {
                    **self.payload, field: value,
                }, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        response = self.client.patch(self.detail_url, {
            "title": "<b>Safe</b>", "description": "<i>Text</i>",
        }, format="json")
        self.assertEqual(response.data["title"], "Safe")
        self.assertEqual(response.data["description"], "Text")

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.visitor)
        for starred, count in ((True, 1), (False, 0)):
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["is_starred"], starred)
            self.assertEqual(response.data["star_count"], count)
            self.assertEqual(response.data["starred_by_names"], self.visitor.username if starred else "")

    def test_missing_object_and_wrong_method(self):
        missing = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, 404)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)

    def test_page_endpoints_and_session_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=self.visitor.username, password="test-password"))
        self.assertEqual(client.post(self.star_url).status_code, 403)
        page = client.get(reverse("main:show_experience"))
        self.assertContains(page, 'data-experiences-url="' + self.list_url + '"')
        self.assertContains(page, 'data-star-pattern=')
        self.assertContains(page, 'data-detail-pattern=')
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertTrue(client.login(username=self.owner.username, password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        client.get(reverse("main:show_experience"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        ).status_code, 201)
