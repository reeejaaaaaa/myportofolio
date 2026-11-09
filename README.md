# MyPortfolio — Tugas 6

## 👤 Identitas

**Nama:** Rheza Abdilla  
**NPM:** 2506612184  
**Kelas:** PBP F  

> Saya suka PBP 🔥

---

Website portofolio pribadi berbasis Django. Tugas 6 berfokus pada API Experience menggunakan Django REST Framework, integrasi Fetch API, hak akses empat peran, dan pengujian.

## 📁 Struktur Folder

```text
myportofolio/
├── main/
│   ├── migrations/
│   ├── admin.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests_api.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── portofolio/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── img/
│   │   ├── education/
│   │   ├── favicon.png
│   │   └── rheza.jpeg
│   │
│   └── js/
│       ├── experience-api.js
│       ├── experience-edit.js
│       ├── experience.js
│       ├── toast.js
│       └── utils.js
│
├── templates/
│   ├── components/
│   │   ├── experience_form_modal.html
│   │   ├── experience_star.html
│   │   ├── project_delete_modal.html
│   │   ├── project_form_modal.html
│   │   ├── project_star.html
│   │   └── toast.html
│   │
│   ├── base.html
│   ├── education.html
│   ├── education_form.html
│   ├── experience.html
│   ├── experience_form.html
│   ├── index.html
│   ├── login.html
│   ├── projects.html
│   ├── projects_form.html
│   ├── register.html
│   └── skill_form.html
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## Refleksi

### Tugas 6

1. **REST, JSON, serta perbedaan PUT dan PATCH**

   REST (Representational State Transfer) adalah gaya arsitektur untuk sistem terdistribusi dengan batasan client-server, stateless, cache, uniform interface, layered system, serta code-on-demand yang opsional. Resource dikenali melalui URI dan dimanipulasi lewat representasinya. Menghasilkan JSON saja hanya menentukan format data; API juga perlu mengikuti semantik operasi, status respons, dan prinsip REST. Sebagai contoh, GET tidak boleh dipakai untuk menghapus Experience. API proyek ini menggunakan pola resource `/api/v1/experiences/` dan metode HTTP, tetapi memakai sesi Django untuk login sehingga tidak diklaim memenuhi seluruh batasan REST secara ketat.

   PUT digunakan ketika klien mengirim representasi pengganti yang lengkap, misalnya menyimpan seluruh field Experience dari klien API. PATCH digunakan untuk pembaruan sebagian, misalnya hanya mengubah `title` tanpa mengubah `description`. Pada DRF proyek ini, PUT memvalidasi field wajib, sedangkan PATCH memakai `partial=True`. Field opsional yang tidak dikirim masih mengikuti perilaku serializer; jika ingin mengosongkan relasi atau tanggal, kirim `projects: []` atau `ended_at: null` secara eksplisit. Halaman Edit memakai PATCH.

2. **Peran serializer dan keuntungannya**

   Serializer mengubah model menjadi tipe data Python yang dapat dirender sebagai JSON, serta memvalidasi data masuk sebelum menyimpannya. `ExperienceSerializer` memiliki daftar field eksplisit, validasi `title` dan `description` dengan `strip_tags`, validasi tipe/relasi dari model, serta field star yang read-only. Dibandingkan dictionary manual dan `JsonResponse`, representasi, validasi, pesan kesalahan, serta proses create/update menjadi terpusat dan lebih mudah diuji. Field akun sensitif tidak dimasukkan ke respons. Rujukan: [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/).

3. **Autentikasi dan otorisasi**

   Autentikasi menentukan identitas pemanggil, sedangkan otorisasi menentukan tindakan yang boleh dilakukan identitas tersebut. `SessionAuthentication` mengenali akun melalui sesi Django. Permission Experience mengizinkan pembacaan publik, update oleh Editor/superuser, dan create/delete hanya oleh superuser. Endpoint star memakai `IsAuthenticated` dan mengambil pengguna dari `request.user`. Menyembunyikan tombol hanya mengatur tampilan: pengguna masih dapat mengirim HTTP request secara langsung, sehingga server wajib memeriksa permission. Rujukan: [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/).

4. **CSRF pada SessionAuthentication dan pengujiannya**

   Browser dapat menyertakan cookie sesi secara otomatis. Tanpa pemeriksaan CSRF, situs lain dapat mencoba memicu perubahan menggunakan sesi korban. Karena itu, request perubahan yang terautentikasi melalui sesi harus menyertakan token CSRF, termasuk POST, PUT, PATCH, dan DELETE. Frontend mengirim `X-CSRFToken`. `force_authenticate` melewati autentikasi normal sehingga tidak membuktikan pemeriksaan CSRF pada sesi. Test menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`, membuktikan request tanpa token ditolak dengan 403 dan database tetap sama, lalu request bertoken berhasil. Rujukan: [DRF SessionAuthentication](https://www.django-rest-framework.org/api-guide/authentication/#sessionauthentication) dan [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/#csrf-validation).

## Implementasi dan menjalankan Tugas 6

Bagian mandiri yang digunakan adalah **Experience**, dengan model dan data dari tugas sebelumnya. API list/create, detail/update/delete, star, serializer, dan permission melanjutkan pekerjaan Tutorial 07. Tugas 6 melengkapi penyimpanan Edit lewat PATCH tanpa reload, pesan error API pada toast, format tanggal form edit, pengujian database setelah penolakan, dan dokumentasi. Informasi star menggunakan hasil prefetch untuk menghindari query tambahan per Experience pada daftar.

| Endpoint | Metode | Fungsi |
| --- | --- | --- |
| `/api/v1/experiences/?q=research` | GET | Daftar dan pencarian judul |
| `/api/v1/experiences/` | POST | Tambah oleh superuser |
| `/api/v1/experiences/<uuid>/` | GET, PUT, PATCH, DELETE | Detail, update Editor/superuser, delete superuser |
| `/api/v1/experiences/<uuid>/star/` | POST | Star/unstar akun yang login |

Dari folder proyek di PowerShell, gunakan virtualenv yang sudah ada:

```powershell
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test main.tests_api --verbosity 2
python manage.py test main
python manage.py runserver
```

Untuk checkout baru, buat virtualenv terlebih dahulu dengan `python -m venv env`. Buka `/experience/`, `/projects/`, serta `/api/v1/experiences/` untuk Browsable API. Editor adalah akun anggota grup bernama persis `Editor`; superuser dapat dibuat dengan `python manage.py createsuperuser` dan grup diatur melalui admin Django. Jangan gunakan `is_staff` sebagai pengganti izin Editor.

Pemeriksaan browser: guest membaca/search/filter/sort; pengguna biasa star/unstar; Editor membuka Edit dan menyimpan tanpa reload; superuser menambah/menghapus. Pada Network, penyimpanan Edit harus menggunakan PATCH. Input invalid dan request yang ditolak ditampilkan lewat toast, dan isian form dipertahankan ketika gagal. Tombol Simpan dinonaktifkan selama request untuk menghindari submit ganda. Halaman Projects tetap menggunakan API Tutorial 07. Endpoint lama dipertahankan untuk kompatibilitas, dengan batas izin yang sama.

## AI Disclosure

Pada Tugas 6, saya menggunakan ChatGPT dan OpenAI Codex sebagai alat bantu dalam pengembangan fitur Experience pada proyek portofolio yang sudah saya kerjakan pada tugas sebelumnya.

AI membantu memberikan penjelasan dan saran terkait Django REST Framework, meninjau kesesuaian implementasi dengan instruksi tugas, serta membantu perubahan kode dan debugging. Bantuan tersebut mencakup integrasi form Edit melalui PATCH, penanganan pesan error API, CSRF, pengujian hak akses, dan penyusunan dokumentasi.

Dalam prosesnya, saya memberikan konteks proyek dan instruksi tugas, meminta agar fungsi sebelumnya tetap dipertahankan, serta mengecek kesesuaian kode terbaru di VS Code. Codex membantu menerapkan perubahan pada repository lokal dan menjalankan pengujian otomatis.

### Keterbatasan Penggunaan AI

Hasil bantuan AI tetap perlu ditinjau dan dipahami. Pengujian otomatis membantu memeriksa fungsi API dan hak akses, tetapi belum menjamin seluruh interaksi tampilan di browser berjalan sesuai harapan. Karena itu, pemeriksaan manual pada alur pengguna tetap diperlukan.
