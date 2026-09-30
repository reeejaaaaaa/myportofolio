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

## 🧩 Tugas 5

Pada Tugas 5, saya menerapkan pola interaktivitas berbasis JavaScript dan AJAX pada halaman Experience. Data Experience tidak lagi dirender langsung oleh Django template, tetapi diambil melalui endpoint JSON menggunakan Fetch API.

Implementasi yang dilakukan:
- menampilkan data Experience menggunakan AJAX dan Fetch API;
- menyusun respons JSON secara manual menggunakan `JsonResponse`;
- menampilkan jumlah star dan status star pengguna yang sedang login;
- menambahkan loading, empty, dan error state;
- menambahkan pencarian Experience tanpa reload;
- menerapkan debounce 300 ms pada pencarian;
- menambahkan Experience melalui modal dan AJAX;
- menangani response HTTP 201, 400, dan 403;
- menyertakan CSRF token pada request POST;
- menampilkan toast untuk response success maupun error;
- melakukan escaping data pada JavaScript sebelum memasukkannya ke HTML;
- melakukan sanitasi server-side menggunakan `strip_tags`;
- menambahkan AJAX Star/Unstar tanpa reload;
- menambahkan filter berdasarkan kategori Experience.

### Pertanyaan Reflektif

1. **Apa itu debouncing dan mengapa penting pada pencarian AJAX?**

   Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan aksi selama waktu tertentu. Pada fitur pencarian saya menggunakan delay 300 ms. Tanpa debouncing, setiap karakter yang diketik dapat langsung menghasilkan request baru ke server. Hal tersebut dapat menghasilkan banyak request yang sebenarnya tidak diperlukan. Dengan debouncing, aplikasi menunggu pengguna berhenti mengetik terlebih dahulu sehingga request menjadi lebih sedikit dan penggunaan server maupun jaringan lebih efisien.

2. **Apa fungsi `await` ketika menggunakan `fetch()`? Apa yang terjadi jika tidak menggunakan `await`?**

   `fetch()` bersifat asynchronous dan menghasilkan sebuah Promise. Keyword `await` digunakan agar eksekusi pada fungsi `async` menunggu Promise tersebut selesai sebelum melanjutkan proses berikutnya. Misalnya, saya menggunakan `await fetch(...)` agar mendapatkan object `Response`, kemudian menggunakan `await response.json()` untuk menunggu body response selesai dikonversi menjadi data JavaScript.

   Jika `await` tidak digunakan, variabel yang diperoleh masih berupa Promise dan bukan hasil request yang sebenarnya. Program harus menangani Promise tersebut menggunakan `.then()` atau mekanisme asynchronous lainnya. Jika langsung diperlakukan seperti hasil response biasa, kode dapat menghasilkan error atau berjalan sebelum data tersedia.

3. **Apa itu XSS dan mengapa data AJAX/JavaScript lebih rentan dibanding data yang langsung dirender Django template?**

   Cross-Site Scripting atau XSS adalah serangan ketika input berbahaya berupa HTML atau JavaScript berhasil dimasukkan ke halaman dan kemudian dijalankan oleh browser pengguna lain. Contohnya adalah input seperti `<img src="x" onerror="alert('XSS!')">`.

   Django template secara default melakukan escaping terhadap nilai yang dirender menggunakan sintaks `{{ variable }}`. Sebaliknya, ketika data dari AJAX dimasukkan secara manual menggunakan JavaScript seperti melalui `innerHTML`, developer bertanggung jawab melakukan escaping sendiri. Oleh karena itu, setiap nilai teks yang saya masukkan ke HTML melalui JavaScript diproses menggunakan `escapeHtml`. Selain itu, input teks juga dibersihkan di server menggunakan `strip_tags` pada `ModelForm` sebagai perlindungan tambahan.

### 🤖 AI Disclosure

Pada Tugas 5, saya menggunakan ChatGPT sebagai alat bantu untuk memahami dan meninjau implementasi AJAX, Fetch API, debouncing, CSRF, response HTTP, modal, sanitasi input, dan perlindungan XSS.

Strategi penggunaan AI yang saya lakukan meliputi:
- memberikan struktur project dan kode yang sedang digunakan agar saran menyesuaikan implementasi aktual;
- meminta pengecekan terhadap alur dari Django view, endpoint JSON, template, hingga JavaScript;
- menggunakan AI untuk membantu menemukan kode lama yang tidak lagi diperlukan setelah halaman diubah menjadi AJAX;
- meminta bantuan dalam menyusun test untuk berbagai role dan response HTTP;
- meminta penjelasan penyebab error sebelum menerapkan perubahan.

Saya tetap melakukan implementasi, menjalankan migration/check/test, memeriksa hasil melalui browser, menguji role pengguna, serta melakukan debugging secara manual sebelum perubahan disimpan ke Git.

### Keterbatasan Penggunaan AI

AI tidak dapat mengetahui kondisi browser, database, session, atau environment lokal secara langsung tanpa informasi yang saya berikan. Beberapa solusi juga perlu disesuaikan ketika struktur project berubah dari tugas sebelumnya. Karena itu, setiap saran AI tetap saya verifikasi menggunakan Django system check, automated test, browser developer tools, dan pengujian manual sebelum digunakan.