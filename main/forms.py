from django.forms import (
    CheckboxInput,
    ModelForm,
    NumberInput,
    Select,
    TextInput,
    Textarea,
    URLInput,
    DateTimeInput,
    DateInput,
)

from main.models import Education, Project, Skill, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class EducationForm(ModelForm):
    class Meta:
        model = Education

        fields = [
            "institution",
            "level",
            "entry_year",
            "graduation_year",
            "gpa",
            "utbk_score",
            "logo_path",
            "experience_anchor",
            "order",
            "is_current",
        ]

        labels = {
            "institution": "Nama Institusi",
            "level": "Jenjang Pendidikan",
            "entry_year": "Tahun Masuk",
            "graduation_year": "Tahun Lulus",
            "gpa": "GPA / Nilai",
            "utbk_score": "Nilai UTBK",
            "logo_path": "Path Logo",
            "experience_anchor": "Experience Anchor",
            "order": "Urutan",
            "is_current": "Sedang Dijalani",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                }
            ),
            "level": Select(),
            "entry_year": NumberInput(
                attrs={
                    "min": 1900,
                    "max": 2100,
                }
            ),
            "graduation_year": NumberInput(
                attrs={
                    "min": 1900,
                    "max": 2100,
                }
            ),
            "gpa": NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "3.50",
                }
            ),
            "utbk_score": NumberInput(
                attrs={
                    "placeholder": "783",
                }
            ),
            "logo_path": TextInput(
                attrs={
                    "placeholder": "img/education/ui.png",
                }
            ),
            "experience_anchor": TextInput(
                attrs={
                    "placeholder": "college",
                }
            ),
            "order": NumberInput(
                attrs={
                    "min": 0,
                    "placeholder": "1",
                }
            ),
            "is_current": CheckboxInput(),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill

        fields = [
            "name",
            "logo_url",
            "description",
            "projects",
            "order",
        ]

        labels = {
            "name": "Nama Skill",
            "logo_url": "URL Logo",
            "description": "Deskripsi",
            "projects": "Project yang Menggunakan Skill Ini",
            "order": "Urutan",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Python",
                }
            ),
            "logo_url": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Backend development, data processing, automation...",
                    "rows": 3,
                }
            ),
            "order": NumberInput(
                attrs={
                    "min": 0,
                }
            ),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "education",
            "projects",
        ]

        labels = {
            "title": "Judul Experience",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
            "education": "Pendidikan Terkait",
            "projects": "Project Terkait",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Asisten Dosen PBP",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman ini...",
                    "rows": 4,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }
