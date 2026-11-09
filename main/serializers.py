from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import (
    Education,
    Experience,
    Project,
)


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if (
            request is None
            or not request.user.is_authenticated
        ):
            return False

        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username
            for user in obj.starred_by.all()
        )

class ExperienceSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    is_ongoing = serializers.SerializerMethodField()

    education_name = serializers.SerializerMethodField()
    project_details = serializers.SerializerMethodField()

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience

        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_display",
            "thumbnail",
            "started_at",
            "ended_at",
            "is_ongoing",
            "education",
            "education_name",
            "projects",
            "project_details",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

        read_only_fields = [
            "id",
            "category_display",
            "is_ongoing",
            "education_name",
            "project_details",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]


    def validate_title(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )

        return value


    def validate_description(self, value):
        value = strip_tags(value).strip()

        if not value:
            raise serializers.ValidationError(
                "Description cannot be empty."
            )

        return value


    def get_category_display(self, obj):
        return obj.get_category_display()


    def get_is_ongoing(self, obj):
        return obj.is_ongoing


    def get_education_name(self, obj):
        if obj.education:
            return obj.education.institution

        return ""


    def get_project_details(self, obj):
        return [
            {
                "id": str(project.id),
                "title": project.title,
            }
            for project in obj.projects.all()
        ]


    def get_star_count(self, obj):
        return obj.starred_by.count()


    def get_is_starred(self, obj):
        request = self.context.get(
            "request"
        )

        if (
            request is None
            or not request.user.is_authenticated
        ):
            return False

        # Reuse the prefetched users when serializing a list.
        return any(user.pk == request.user.pk for user in obj.starred_by.all())


    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username
            for user in obj.starred_by.all()
        )