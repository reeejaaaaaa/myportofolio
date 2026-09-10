# 🔥 MyPortfolio

## 👤 Identitas

**Nama:** Rheza Abdilla  
**NPM:** 2506612184  
**Kelas:** PBP F  

> Saya suka PBP 🔥

---

# 📁 Struktur Folder

myportofolio/
│
├── env/                         # Python virtual environment
├── venv/                        # Virtual environment lain
│
├── main/
│   ├── migrations/              # Database migrations
│   ├── models.py                # Model Experience & Education
│   ├── tests.py                 # Unit tests
│   ├── urls.py                  # URL aplikasi main
│   └── views.py                 # View aplikasi main
│
├── portofolio/
│   ├── __pycache__/
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
│   └── img/
│       ├── education/
│       ├── favicon.png
│       └── rheza.jpeg
│
├── templates/
│   ├── education.html
│   ├── experience.html
│   └── index.html
│
├── .env
├── .env.prod
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt

# 📚 Refleksi Tugas

## 🧩 Tugas 1

### 1. 

Saya menggunakan elemen semantik untuk membuat dan mengedit bagian-bagian website agar lebih rapi, mudah dipahami, dan jelas.

Beberapa elemen yang saya gunakan antara lain:

- `<header>` untuk bagian atas halaman.
- `<nav>` untuk menu navigasi.
- `<main>` untuk isi utama.
- `<section>` untuk membagi konten.
- `<footer>` untuk bagian bawah halaman.

### 2. 

Tantangan responsive utama adalah mengatur layout desktop ke mobile, termasuk bagian **Education** dan **Skill Card**.

Lumayan capek karena harus berkali-kali mengecek hasilnya melalui browser desktop dan HP supaya tampilannya sesuai harapan dan tetap rapi.

### 3.

Static web lumayan repot karena perubahan harus diedit langsung di HTML dan CSS, lalu dicek berulang lewat development server.

Setelah itu, saya ingin menyelesaikan semua bagian yang sudah ada di navigator seperti **Education, Projects, Experience, dan Contact**.

### 🤖 AI Disclosure

Dalam pengembangan website portofolio ini, saya menggunakan ChatGPT sebagai AI assistant. ChatGPT saya gunakan untuk membantu:

### 🛠️ Penggunaan AI

1. Memberikan saran struktur HTML, CSS, Django routing, dan halaman Education.
2. Membantu debugging masalah static files, virtual environment, deployment PWS, dan konfigurasi Django.
3. Memberikan referensi responsive design, color palette, hover effect, dan navigasi antarhalaman.
4. Membantu membuat favicon/logo serta mengolah beberapa gambar agar sesuai dengan desain website.
5. Memberikan contoh kode saat saya mengalami masalah atau membutuhkan alternatif implementasi.

### 🧑‍💻 Pengerjaan Mandiri

Saya tetap melakukan implementasi, penyesuaian kode, pemilihan desain, pengujian localhost, pengecekan desktop/mobile, serta deployment secara mandiri. Beberapa solusi juga saya sesuaikan sendiri setelah melihat hasil langsung di browser.

### ⚠️ Keterbatasan AI

ChatGPT memiliki beberapa keterbatasan selama proses pengembangan ini:

1. Saran kode tidak selalu langsung cocok dengan kondisi project sehingga tetap perlu diuji dan disesuaikan.
3. Tidak dapat menjalankan atau mengubah environment lokal dan PWS saya secara langsung.
4. Beberapa masalah baru dapat diketahui setelah kode dijalankan pada development server.
4. Saran syntax masih harus dikembangkan lagi agar menyesuaikan keinginan (terkadang masih terkesan kuno)

Karena itu, AI saya gunakan sebagai alat bantu, sedangkan keputusan akhir, pengujian, dan implementasi tetap saya lakukan sendiri.
---

## 🎓 Tugas 2

### 1. 

Ketika pengguna membuka halaman **Education**, request pertama diterima oleh `urls.py` pada project.

`portofolio/urls.py` kemudian meneruskan request ke `main/urls.py`. Dari sana, Django menentukan view `show_education`.

View mengambil seluruh data dari model `Education`, kemudian memasukkannya ke dalam `context` dan meneruskannya ke `education.html`.

Template kemudian menggunakan Django Template Language untuk melakukan perulangan terhadap data sebelum hasil akhirnya ditampilkan pada browser. ```text
Browser
   ↓
portofolio/urls.py
   ↓
main/urls.py
   ↓
show_education()
   ↓
Education Model
   ↓
Context
   ↓
education.html
   ↓
Browser

### 2. 

Data Education lebih baik disimpan pada model daripada ditulis langsung pada HTML karena data menjadi lebih mudah untuk ditambah, diubah, dan dikelola.

Template juga menjadi lebih rapi karena hanya bertugas menampilkan data dari database. Jika nanti jumlah data bertambah, saya tidak perlu membuat card baru secara manual satu per satu di HTML.

### 3. 

makemigrations digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model.

Sedangkan migrate digunakan untuk menerapkan migration tersebut ke database.

Contohnya, ketika saya menambahkan model Education, saya harus menjalankan kedua perintah tersebut agar tabel Education dapat dibuat dan digunakan pada database.

## 🤖 AI Disclosure

Dalam pengembangan website portofolio ini, saya menggunakan ChatGPT sebagai AI assistant.

## 🛠️ Penggunaan AI

ChatGPT saya gunakan untuk membantu:

Memberikan saran struktur HTML, CSS, Django routing, model, dan halaman Education.
Membantu debugging masalah static files, virtual environment, migration, database, deployment PWS, dan konfigurasi Django.
Memberikan referensi implementasi Model-View-Template untuk Experience dan Education.
Membantu memberikan contoh unit test untuk memastikan URL, template, data model, dan empty state bekerja dengan benar.
Membantu menganalisis traceback atau error log yang muncul ketika development.

## 💬 Strategi Penggunaan AI

Saya menggunakan ChatGPT secara iteratif. Saya terlebih dahulu mencoba melakukan implementasi, kemudian memberikan error log ketika menemukan masalah.

Saran dari AI kemudian saya uji sendiri melalui development server. Jika hasilnya belum sesuai, saya melakukan penyesuaian atau memberikan hasil terbaru kepada AI untuk dianalisis kembali.

## 🧑‍💻 Pengerjaan Mandiri

Saya tetap melakukan implementasi, pengujian, penyesuaian kode, pemilihan desain, pengecekan localhost, pengecekan desktop dan mobile, migration database, Git, serta deployment secara mandiri.

Beberapa solusi dari AI juga saya ubah kembali agar sesuai dengan struktur project dan tampilan yang saya inginkan.

## ⚠️ Keterbatasan AI

ChatGPT memiliki beberapa keterbatasan selama proses pengembangan ini:

Saran kode tidak selalu langsung cocok dengan kondisi project sehingga tetap perlu diuji dan disesuaikan.
Tidak dapat menjalankan atau mengubah environment lokal dan PWS saya secara langsung.
Beberapa masalah baru dapat diketahui setelah kode dijalankan pada development server.
Saran syntax dan styling terkadang masih perlu dikembangkan kembali agar sesuai dengan desain yang saya inginkan dan tidak terkesan terlalu standar atau kuno.

Karena itu, AI saya gunakan sebagai alat bantu pengembangan, sedangkan keputusan akhir, implementasi, dan pengujian tetap saya lakukan sendiri.

