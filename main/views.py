from django.shortcuts import render
from main.models import Education, Experience
from django.contrib import messages
from main.forms import ProjectForm
from main.models import Project
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render



def show_main(request):
    context = {
        "name": "Rheza Abdilla",
        "npm": "2506612184",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan cyber security dan pendidikan."
        ),
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rheza Abdilla",
        "experience_list": Experience.objects.all().order_by("-started_at"),
    }

    return render(request, "experience.html", context)


def show_education(request):
    context = {
        "name": "Rheza Abdilla",
        "education_list": Education.objects.all(),
    }

    return render(request, "education.html", context)



def create_project(request):
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
    title_query = request.GET.get("title", "").strip()

    project_list = Project.objects.all()

    if title_query:
        project_list = project_list.filter(
            title__icontains=title_query
        )

    context = {
        "project_list": project_list,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")