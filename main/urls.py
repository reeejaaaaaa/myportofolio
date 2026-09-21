from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_education,
    create_project,
    show_projects,
    get_projects_json,
    delete_project,
    get_education_json,
    create_education,
    update_education,
    delete_education,
    get_skills_json,
    create_skill,
    update_skill,
    delete_skill,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("education/", show_education, name="show_education"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path(
        "api/projects/",
        get_projects_json,
        name="get_projects_json",
    ),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path(
        "api/education/",
        get_education_json,
        name="get_education_json",
    ),
    path(
        "education/add/",
        create_education,
        name="create_education",
    ),
    path(
        "education/<uuid:education_id>/edit/",
        update_education,
        name="update_education",
    ),
    path(
        "education/<uuid:education_id>/delete/",
        delete_education,
        name="delete_education",
    ),
    path(
        "api/skills/",
        get_skills_json,
        name="get_skills_json",
    ),
    path(
        "skills/add/",
        create_skill,
        name="create_skill",
    ),
    path(
        "skills/<uuid:skill_id>/edit/",
        update_skill,
        name="update_skill",
    ),
    path(
        "skills/<uuid:skill_id>/delete/",
        delete_skill,
        name="delete_skill",
    ),
]
