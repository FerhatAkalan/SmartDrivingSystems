# 🚗 Akıllı Sürücü Takip ve Sürüş Analizi Raporlama Sistemi

## 📖 Proje Hakkında

Bu proje, ticari araç sürücülerinin sürüş esnasında tehlikeli davranışlarını tespit ederek sürüş profillerini çıkarıp raporlamayı amaçlamaktadır. Proje, sürücülerin yorgunluk, dikkatsizlik gibi davranışlarını analiz ederek kaza risklerini azaltmayı hedefler. Yük ve yolcu taşımacılığı yapan firmaların, sürücülerin performansını değerlendirebilmesini sağlar.

## 🎯 Amaçlar

- **🛡️ Güvenli Sürüş**: Sürücü yorgunluğu, dikkatsizlik gibi tehlikeli davranışların tespiti. Sürücü kaynaklı hataların ve tehlikeli davranışlarının tespit edilmesi.
- **🚦 Trafik Kurallarına Uyum**: Hız sınırları ve trafik ışıklarına uyumun denetlenmesi.
- **📈 Performans Analizi**: Sürücü performansının detaylı analizi ve raporlanması. Sürücü profillerinin oluşturulması ve raporlanması
- **📱 Kullanıcı Dostu Arayüz**: Analiz sonuçları, kullanıcı dostu bir arayüz ile raporlanır.


## Yöntem

### Veri Toplama ve Model Eğitimi
- YOLO algoritması kullanılarak iki farklı model oluşturulmuştur:
  - Araç içi model: Yorgunluk, telefonla ilgilenme, sigara içme, yeme-içme davranışlarını tespit eder.
  - Araç dışı model: Hız sınırı ve kırmızı ışık ihlallerini tespit eder.
- Kullanılan yazılım dili ve teknolojiler:
  - Python
  - TensorFlow
  - OpenCV

### Model Entegrasyonu ve Yazılımlar
- Derin öğrenme modelleri web uygulamasına entegre edilmiştir.
- Model çıktıları görselleştirilmiştir.

### Donanım ve Yazılım Testi
- Veri toplama sistemi, Raspberry Pi 4, webcam, Raspberry Pi modüle 3 NOIR kamera ve OBD II cihazı ile kurulmuştur.

## 🛠️ Kullanılan Teknolojiler
- **💻 Yazılım Dilleri ve Kütüphaneler**:
  - Python
  - Django
  - SQLite
  - YOLOv8
  - OpenCV
  - Web Teknolojileri (HTML, CSS, JavaScript)
  - Bootstrap
- **🔧 Donanımlar**:
  - Raspberry Pi
  - OBD-II
  - Araç İçi ve Dışı Kameralar

## Kullanım
1. Sistem, sürüş boyunca video kaydını otomatik olarak yapar.
2. Kaydedilen videolar, analiz yazılımına yüklenerek sürüş davranışları analiz edilir.
3. Analiz sonuçları, kullanıcı dostu bir arayüz ile raporlanır.

## Proje Görselleri

### Login Page
![Project Banner](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/29334c32-0018-4419-a319-1ace2287c666)
---
### Analyse Page
![AnalysePage](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/f591c551-8f4a-4be2-bf6f-d1f08db3cf56)
---
### Report Page
![ReporPage](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/1fd713aa-f9d7-4ea1-be33-97dca2e768dc)
![PieGraphic](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/7f59fe77-3e5d-47cd-84ab-b865430922dc)
![FrequenceGraphic](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/9e6b016c-09a7-4054-b0ae-3e861827324a)
![TespitEdilenEtiketler](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/30ea797d-ef0d-40fc-aafd-3f082417f919)
![Hız İhlali Tespit](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/f1bace18-313a-4955-9bed-43d4c2b4e62a)
---
### All Statistics Page
![Ekran görüntüsü 2024-06-13 161831](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/1744a885-ebda-4413-9e40-99169d469c1b)
---
### About Page
![Ekran görüntüsü 2024-06-13 191823](https://github.com/FerhatAkalan/smartdrivingsystems/assets/102834897/df1f9a3a-7a6f-4f26-b51b-bf655bd8e88c)
---


## Katkıda Bulunanlar
- [Ferhat Akalan](https://github.com/ferhatakalan)
- [Betül Mumcu](https://github.com/betuullm)
