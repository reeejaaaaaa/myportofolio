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

# 📚 Refleksi Tugas

## 🧩 Tugas 5

Pada Tugas 5, saya menerapkan pola interaktivitas berbasis JavaScript dan AJAX pada halaman Experience.

Implementasi yang dilakukan:
- Menampilkan data Experience menggunakan Fetch API dan AJAX.
- Menyusun respons JSON secara manual menggunakan `JsonResponse`.
- Menampilkan informasi star berupa jumlah star dan status star pengguna yang sedang login.
- Menambahkan loading state, empty state, dan error state.
- Menambahkan pencarian Experience tanpa reload halaman.
- Menggunakan debounce selama 300 ms pada pencarian.
- Menambahkan Experience melalui modal dengan AJAX.
- Menangani HTTP response 201, 400, dan 403.
- Mengirim CSRF token pada request POST.
- Menampilkan toast untuk kondisi berhasil maupun gagal.
- Melakukan escaping data pada JavaScript sebelum data dimasukkan ke HTML.
- Membersihkan input teks menggunakan `strip_tags` pada `ExperienceForm`.
- Menambahkan Star/Unstar menggunakan AJAX tanpa reload halaman.
- Menambahkan filter berdasarkan kategori Experience.
- Menambahkan pengurutan berdasarkan newest, oldest, jumlah star, dan judul A-Z.
- Menambahkan summary interaktif untuk total Experience, ongoing Experience, project terkait, dan total star.
- Menambahkan Delete Experience melalui AJAX tanpa reload halaman.

### Pertanyaan Reflektif

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan suatu aksi selama periode waktu tertentu. Pada fitur pencarian Experience, saya menggunakan delay 300 ms.

   Tanpa debouncing, setiap karakter yang diketik pengguna dapat langsung mengirim request baru ke server. Hal ini dapat menghasilkan banyak request yang sebenarnya tidak diperlukan. Dengan debouncing, request baru dikirim setelah pengguna berhenti mengetik sehingga penggunaan jaringan dan server menjadi lebih efisien.

2. **Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?**

   `fetch()` merupakan operasi asynchronous dan mengembalikan sebuah Promise. `await` digunakan di dalam fungsi `async` agar program menunggu Promise tersebut selesai sebelum melanjutkan ke proses berikutnya.

   Pada implementasi saya, `await fetch(...)` digunakan untuk menunggu response dari server, sedangkan `await response.json()` digunakan untuk menunggu body response selesai dikonversi menjadi data JavaScript.

   Jika tidak menggunakan `await`, variabel yang diperoleh masih berupa Promise dan bukan hasil response yang sebenarnya. Promise tersebut harus ditangani menggunakan `.then()` atau mekanisme asynchronous lainnya. Jika langsung digunakan seperti data biasa, program dapat berjalan sebelum data tersedia dan menghasilkan error.

3. **Jelaskan apa itu serangan XSS dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**

   Cross-Site Scripting atau XSS adalah serangan ketika input berbahaya berupa HTML atau JavaScript berhasil dimasukkan ke halaman dan kemudian dijalankan oleh browser.

   Django template secara default melakukan escaping terhadap nilai yang dirender menggunakan `{{ variable }}`. Namun, ketika data dari endpoint AJAX disisipkan secara manual menggunakan JavaScript seperti `innerHTML`, developer harus memastikan sendiri bahwa nilai tersebut sudah aman.

   Pada halaman Experience, setiap nilai teks yang dimasukkan ke HTML melalui JavaScript diproses menggunakan `escapeHtml()`. Selain itu, input teks seperti title dan description dibersihkan di sisi server menggunakan `strip_tags()` pada `ExperienceForm`. Dengan demikian perlindungan dilakukan baik di frontend maupun backend.

### 🤖 AI Disclosure

Pada Tugas 5, saya menggunakan ChatGPT sebagai alat bantu untuk memahami, meninjau, dan melakukan debugging implementasi AJAX, Fetch API, JavaScript, debouncing, CSRF, modal, toast, authorization, serta perlindungan XSS.

AI digunakan untuk membantu:
- meninjau struktur project Django yang sudah dibuat pada tugas sebelumnya;
- merancang perubahan halaman Experience dari server-side rendering menjadi AJAX;
- membantu penyusunan endpoint JSON manual;
- membantu implementasi pencarian dengan debouncing;
- membantu implementasi modal dan AJAX POST;
- membantu implementasi AJAX Star/Unstar dan Delete;
- membantu mengidentifikasi kode lama yang sudah tidak dibutuhkan setelah halaman menggunakan AJAX;
- membantu debugging error pada JavaScript dan Django;
- membantu menyusun automated test untuk fitur Tugas 5;
- membantu meninjau perlindungan XSS pada frontend dan backend.

Saya tetap melakukan implementasi pada project lokal, menjalankan Django system check dan automated test, menguji aplikasi melalui browser dan Developer Tools, menguji berbagai role pengguna, serta memverifikasi hasil setiap perubahan secara manual.

### Keterbatasan Penggunaan AI

AI tidak dapat mengetahui secara langsung keadaan browser, database, session, environment lokal, maupun perubahan file terbaru tanpa kode atau error log yang saya berikan. Beberapa saran juga perlu disesuaikan kembali karena struktur project berkembang dari tugas-tugas sebelumnya.

Karena itu, setiap saran dari AI tetap saya verifikasi menggunakan `python manage.py check`, automated test, browser Developer Tools, serta pengujian manual sebelum digunakan.