from django.shortcuts import render

from main.models import Experience



from django.shortcuts import render

from main.models import Experience


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