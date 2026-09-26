# 🔥 MyPortfolio

## 👤 Identitas

**Nama:** Rheza Abdilla  
**NPM:** 2506612184  
**Kelas:** PBP F  

> Saya suka PBP 🔥

---

## 📁 Struktur Folder

```text
myportofolio/
├── main/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── portofolio/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       ├── education/
│       ├── favicon.png
│       └── rheza.jpeg
│
├── templates/
│   ├── components/
│   │   └── project_delete_modal.html
│   ├── base.html
│   ├── education.html
│   ├── education_form.html
│   ├── experience.html
│   ├── index.html
│   ├── projects.html
│   └── projects_form.html
│
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

# 📚 Refleksi Tugas

## 🧩 Tugas 4

Pada Tugas 4, saya mengimplementasikan authentication dan authorization menggunakan sistem bawaan Django.

Implementasi yang dilakukan:
- Register, login, dan logout pengguna.
- Session dan cookie `last_login`.
- Role `Editor` menggunakan Django Group.
- Pembatasan akses untuk visitor, regular user, Editor, dan superuser.
- Create dan delete Education hanya untuk superuser.
- Update Education untuk Editor dan superuser.
- Tombol CRUD disembunyikan sesuai hak akses.
- Fitur star/unstar pada Experience menggunakan `ManyToManyField` ke `User`.
- Menampilkan jumlah star dan status star pengguna.
- Endpoint JSON tetap dapat digunakan tanpa mengekspos ID pengguna secara langsung.


### 🤖 AI Disclosure

Pada Tugas 4, AI digunakan untuk membantu memahami alur authentication, authorization, Django Group, session/cookie, serta debugging implementasi role dan relasi antar model. Saya tetap melakukan implementasi, konfigurasi role melalui Django Admin, pengujian manual setiap level akses, dan penyesuaian struktur kode secara mandiri.

### 🛠️ Penggunaan AI
AI digunakan untuk membantu:
- memahami alur authentication, session, dan cookie pada Django;
- memahami perbedaan authentication dan authorization;
- membantu implementasi role visitor, regular user, Editor, dan superuser;
- membantu penggunaan Django Group untuk role Editor;
- membantu implementasi server-side access control menggunakan `login_required`, `is_superuser`, dan pengecekan Group;
- membantu membuat fitur star/unstar menggunakan relasi `ManyToManyField` ke `User`;
- membantu menjaga endpoint JSON tetap aman dengan natural foreign key;
- membantu debugging error pada routing, form, template, permission, dan relasi model;
- membantu merapikan UI tombol Create, Edit, Delete, Star, modal konfirmasi, dan tampilan Experience;

### 🧑‍💻 Pengerjaan Mandiri

Saya tetap melakukan implementasi, penyesuaian kode, pemilihan desain, pengecekan desktop/mobile, serta deployment secara mandiri. Beberapa solusi juga saya sesuaikan sendiri setelah melihat hasil langsung di browser.

### ⚠️ Keterbatasan AI

ChatGPT memiliki beberapa keterbatasan selama proses pengembangan ini:

- AI tidak dapat melihat kondisi project dan environment lokal secara langsung tanpa kode, screenshot, atau error log yang diberikan.
- Solusi yang diberikan AI masih perlu diuji karena bisa saja tidak sepenuhnya sesuai dengan struktur project terbaru.
- AI dapat memberikan saran yang secara konsep benar tetapi masih membutuhkan penyesuaian pada routing, import, indentation, atau template yang sudah ada.
- AI tidak menggantikan proses debugging dan verifikasi manual, terutama untuk permission, migration, dan behavior aplikasi di browser.
- Saran syntax masih harus dikembangkan lagi agar menyesuaikan keinginan (terkadang masih terkesan kuno)

Karena itu, AI saya gunakan sebagai alat bantu, sedangkan keputusan akhir, pengujian, dan implementasi tetap saya lakukan sendiri.
---

