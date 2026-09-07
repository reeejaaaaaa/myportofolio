Nama : Rheza Abdilla

NPM : 2506612184

Kelas : PBP F

Saya suka PBP

####

Tugas 1.

1. Saya menggunakan elemen semantik untuk membuat dan mengedit bagian bagian yang saya inginkan agar lebih rapih, mudah dipahami dan jelas. Kurang lebih part - partnya ada <header> untuk bagian atas, <nav> untuk menu, <main> untuk isi utama, <section> untuk membagi konten, dan <footer> untuk bagian bawah agar struktur lebih rapi.
2. Tantangan responsive utama adalah mengatur layout desktop ke mobile, termasuk bagian Education dan skill card. Lumayan capek karena harus berkali-kali cek hasilnya di browser desktop dan HP supaya tampilannya sesuai harapan dan tetap rapi.
3. Static web lumayan repot karena perubahan harus diedit langsung di HTML dan CSS, lalu dicek berulang lewat development server. Setelah ini saya ingin menyelesaikan semua bagian yang sudah ada di navigator seperti Education, Projects, Experience, dan Contact.

Struktur Folder

myportofolio/
│
├── env/                     # Python virtual environment
├── venv/                    # Python virtual environment lain
│
├── portofolio/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
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
│   └── index.html
│
├── .env
├── .env.prod
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt

AI Disclosure

Dalam pengembangan website portofolio ini, saya menggunakan ChatGPT sebagai AI assistant. ChatGPT saya gunakan untuk membantu:

1. Memberikan saran struktur HTML, CSS, Django routing, dan halaman Education.
2. Membantu debugging masalah static files, virtual environment, deployment PWS, dan konfigurasi Django.
3. Memberikan referensi responsive design, color palette, hover effect, dan navigasi antarhalaman.
4. Membantu membuat favicon/logo serta mengolah beberapa gambar agar sesuai dengan desain website.
5. Memberikan contoh kode saat saya mengalami masalah atau membutuhkan alternatif implementasi.

Saya tetap melakukan implementasi, penyesuaian kode, pemilihan desain, pengujian localhost, pengecekan desktop/mobile, serta deployment secara mandiri. Beberapa solusi juga saya sesuaikan sendiri setelah melihat hasil langsung di browser.

Keterbatasan AI

ChatGPT memiliki beberapa keterbatasan selama proses pengembangan ini:

1. Tidak dapat melihat hasil website secara langsung kecuali saya memberikan screenshot atau kode terbaru.
2. Saran kode tidak selalu langsung cocok dengan kondisi project sehingga tetap perlu diuji dan disesuaikan.
3. Tidak dapat menjalankan atau mengubah environment lokal dan PWS saya secara langsung.
4. Beberapa masalah baru dapat diketahui setelah kode dijalankan pada development server.
5. Saran syntax masih harus dikembangkan lagi agar menyesuaikan keinginan (terkadang masih terkesan kuno)

Karena itu, AI saya gunakan sebagai alat bantu, sedangkan keputusan akhir, pengujian, dan implementasi tetap saya lakukan sendiri.