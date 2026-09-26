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
    register,
    login_user,
    logout_user,
    toggle_star,
    get_experiences_json,
    create_experience,
    update_experience,
    delete_experience,
    toggle_star_experience,
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
    path(
        "register/",
        register,
        name="register",
    ),
    path(
        "login/",
        login_user,
        name="login",
    ),
    path(
        "logout/",
        logout_user,
        name="logout",
    ),
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
    path(
        "api/experiences/",
        get_experiences_json,
        name="get_experiences_json",
    ),
    path(
        "experience/add/",
        create_experience,
        name="create_experience",
    ),
    path(
        "experience/<uuid:experience_id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path(
        "experience/<uuid:experience_id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path(
        "experience/<uuid:experience_id>/star/",
        toggle_star_experience,
        name="toggle_star_experience",
    ),
]
