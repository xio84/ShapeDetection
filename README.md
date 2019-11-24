# Shape-Detection-KBS

Program KBS untuk mendeteksi shape polygon sederhana.

Proses updating dan inferencing fakta yang terlibat dengan memanfaatkan CLIPS yang pertama dengan menghitung jumlah sisi dari bangun yang dimasukkan pengguna. Apabila sudah terdeteksi sebagai salah satu bangun (misalnya segitiga) melalui defrule triangle, maka rule lain yang memiliki prasyarat bangun segitiga akan diteruskan karena strategi penyelesaian yang digunakan adalah Depth-first (dimana rule yang baru diaktifkan akan dijalankan terlebih dahulu). Misalkan pengguna memasukkan segitiga sama kaki (30º, 30º, 120º). Ketika defrule equilateral dijalankan, rule akan berhenti pada pembacaan sudut ke-1 karena sudut pertama sudah tidak memenuhi kondisi rule (sudut 60º). defrule isosceles kemudian dijalankan, dan ternyata masukan pengguna memenuhi rule yang disiapkan (sudut 1 bernilai α, sudut 2 juga bernilai α) sehingga segitiga masukan pengguna diklasifikasikan sebagai segitiga sama kaki.

## Dibuat oleh
1. 13517020 - T. Antra Oksidian Tafly
2. 13517050 - Christopher Billy Setiawan
3. 13517059 - Nixon Andhika
4. 13517146 - Hansen

## Petunjuk Penggunaan Program
### Instal requirements dan Run
```sh
$ pip install -r requirements.txt py GUI.py
```
### Run
```sh
$ py GUI.py
```
### Alur
Alur utama dari program:
1. Jalankan program dengan command di atas
2. Klik "Open Image"
3. Pilih gambar dengan shape
4. Klik "Back to Main Menu"
5. Klik shape yang ingin dideteksi pada tree
6. Klik tombol "Search"
7. Hasil akan muncul

#### Rule dapat dilihat dan diubah dengan klik tombol "Open Rule Editor"
