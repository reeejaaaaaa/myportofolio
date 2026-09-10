from django.shortcuts import render
from main.models import Education, Experience


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


def show_experience(request):
    context = {
        "name": "Rheza Abdilla",
        "experience_list": Experience.objects.all().order_by("-started_at"),
    }

    return render(request, "experience.html", context)
