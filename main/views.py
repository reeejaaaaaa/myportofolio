from django.shortcuts import render
from main.models import Education, Experience, Skill
from django.contrib import messages
from main.forms import EducationForm, ProjectForm, SkillForm
from main.models import Project
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout as auth_logout
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def show_main(request):
    json_response = get_skills_json(request)

    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    skill_list = [skill.object for skill in skills]
    
    last_login = request.COOKIES.get(
        "last_login",
        "No active login session / Cookie not found",
    )

    context = {
        "name": "Rheza Abdilla",
        "npm": "2506612184",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan cyber security dan pendidikan."
        ),
        "skill_list": skill_list,
        "last_login": last_login,
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rheza Abdilla",
        "experience_list": Experience.objects.all().order_by("-started_at"),
    }

    return render(request, "experience.html", context)


def show_education(request):
    json_response = get_education_json(request)

    educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    education_list = [education.object for education in educations]

    context = {
        "name": "Rheza Abdilla",
        "education_list": education_list,
    }

    return render(
        request,
        "education.html",
        context,
    )


def get_education_json(request):
    educations = Education.objects.all()

    education_json = serializers.serialize(
        "json",
        educations,
    )

    return HttpResponse(
        education_json,
        content_type="application/json",
    )


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Data pendidikan berhasil ditambahkan!",
        )
        return redirect("main:show_education")

    context = {
        "name": "Rheza Abdilla",
        "form": form,
    }

    return render(
        request,
        "education_form.html",
        context,
    )

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Rheza",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rheza Abdilla",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True, )
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def update_education(request, education_id):
    education = get_object_or_404(
        Education,
        pk=education_id,
    )

    form = EducationForm(
        request.POST or None,
        instance=education,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Data pendidikan berhasil diperbarui!",
        )

        return redirect("main:show_education")

    context = {
        "name": "Rheza Abdilla",
        "form": form,
        "education": education,
        "is_edit": True,
    }

    return render(
        request,
        "education_form.html",
        context,
    )


def delete_education(request, education_id):
    education = get_object_or_404(
        Education,
        pk=education_id,
    )

    if request.method == "POST":
        education.delete()

        messages.success(
            request,
            "Data pendidikan berhasil dihapus!",
        )

        return redirect("main:show_education")

    return redirect("main:show_education")


def get_skills_json(request):
    skills = Skill.objects.all()

    skills_json = serializers.serialize(
        "json",
        skills,
    )

    return HttpResponse(
        skills_json,
        content_type="application/json",
    )


def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Skill berhasil ditambahkan!",
        )

        return redirect("main:show_main")

    context = {
        "name": "Rheza Abdilla",
        "form": form,
    }

    return render(
        request,
        "skill_form.html",
        context,
    )


def update_skill(request, skill_id):
    skill = get_object_or_404(
        Skill,
        pk=skill_id,
    )

    form = SkillForm(
        request.POST or None,
        instance=skill,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Skill berhasil diperbarui!",
        )

        return redirect("main:show_main")

    context = {
        "name": "Rheza Abdilla",
        "form": form,
        "skill": skill,
        "is_edit": True,
    }

    return render(
        request,
        "skill_form.html",
        context,
    )


def delete_skill(request, skill_id):
    skill = get_object_or_404(
        Skill,
        pk=skill_id,
    )

    if request.method == "POST":
        skill.delete()

        messages.success(
            request,
            "Skill berhasil dihapus!",
        )

        return redirect("main:show_main")

    return redirect("main:show_main")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Account created successfully. Please log in.",
        )

        return redirect("main:login")

    context = {
        "name": "Rheza Abdilla",
        "form": form,
    }

    return render(
        request,
        "register.html",
        context,
    )


def login_user(request):
    if request.user.is_authenticated:
        return redirect("main:show_main")

    form = AuthenticationForm(
        request,
        data=request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)

        messages.success(
            request,
            "Login berhasil.",
        )

        response = redirect("main:show_main")

        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        return response

    context = {
        "form": form,
    }

    return render(
        request,
        "login.html",
        context,
    )


def logout_user(request):
    auth_logout(request)

    messages.success(
        request,
        "Logout berhasil.",
    )

    response = redirect("main:show_main")

    response.delete_cookie("last_login")

    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(
        Project,
        pk=project_id,
    )

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")