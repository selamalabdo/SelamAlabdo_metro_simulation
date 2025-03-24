# SelamAlabdo_metro_simulation


# Ankara Metro Ağı Simülasyonu
Bu proje, Ankara metrosunun belirli hatlarını ve istasyonlarını modelleyerek farklı güzergah seçenekleri sunan, nesne tabanlı bir simülasyon uygulamasıdır. Kullanıcı, istasyonlar arasında en az aktarmalı veya en hızlı rotayı hesaplayabilir, ayrıca metro ağı grafiksel olarak görselleştirilebilir.
---
## İçindekiler
- [Proje Tanımı](#proje-tanımı)
- [Kullanılan Teknolojiler ve Kütüphaneler](#kullanılan-teknolojiler-ve-kütüphaneler)
- [Projenin Yapısı](#projenin-yapısı)
- [Algoritmaların Çalışma Mantığı](#algoritmaların-çalışma-mantığı)
  - [1. En Az Aktarmalı Rota (BFS)](#1-en-az-aktarmalı-rota-bulma-bfs)
  - [2. En Hızlı Rota (Dijkstra Benzeri)](#2-en-hızlı-rota-bulma-dijkstra-benzeri)
- [Grafiksel Görselleştirme](#grafiksel-görselleştirme)
- [Kurulum](#kurulum)
- [Örnek Kullanım Senaryoları ve Çıktılar](#örnek-kullanım-senaryoları-ve-çıktılar)
- [Geliştirici Notları ve Gelecek Çalışmalar](#geliştirici-notları-ve-gelecek-çalışmalar)
- [Katkıda Bulunma](#katkıda-bulunma)
---
## Proje Tanımı
Bu projede, Ankara metrosunun hatları ve istasyonları nesne tabanlı olarak modellenmiştir. Her istasyon; benzersiz bir ID, ad ve ait olduğu hat bilgisi içerir. İstasyonlar arasındaki bağlantılar (komşular) seyahat süreleriyle birlikte tanımlanarak, iki farklı algoritma kullanılarak:
- En Az Aktarmalı Rota: İstasyonlar arasında minimum transfer sayısı ile istenilen hedefe ulaşan güzergahı,
- En Hızlı Rota: Toplam seyahat süresi en düşük olacak şekilde istenilen hedefe ulaşan güzergahı
hesaplanır. Ek olarak, metro ağı NetworkX ve Matplotlib kullanılarak grafiksel olarak görselleştirilmektedir.
---
## Kullanılan Teknolojiler ve Kütüphaneler
Proje, aşağıdaki teknolojiler ve Python kütüphaneleri kullanılarak geliştirilmiştir:
- Python 3.x: Projenin ana programlama dili.
- Collections: `defaultdict`, `deque` gibi veri yapıları kullanılarak, verimli veri yönetimi sağlanmıştır.
- Heapq : Öncelikli kuyruk işlemleri için kullanılarak, Dijkstra algoritmasına benzer yaklaşım uygulanmıştır.
- NetworkX: Metro ağı gibi graf yapılarının modellenmesi için kullanılmıştır.
- Matplotlib: Metro ağı görselleştirmesi ve grafiksel sunum için tercih edilmiştir.
-  Typing: Tip belirteçleri (type hints) kullanılarak kod okunabilirliği ve bakım kolaylığı sağlanmıştır.
----
## Projenin Yapısı
Proje iki ana sınıf etrafında organize edilmiştir:
- Istasyon:
  - Özellikler: `idx` (benzersiz ID), `ad` (istasyon adı), `hat` (istasyonun ait olduğu hat) ve `komsular` (komşu istasyonlar ve seyahat süresi bilgisi).  
  - Metotlar: `komsu_ekle` ile belirli bir istasyona komşu eklenir.
- MetroAgi:  
  - Özellikler: `istasyonlar` (tüm istasyonların sözlüğü) ve `hatlar` (her hattaki istasyonların listesi).  
  - Metotlar:
    - `istasyon_ekle`: Yeni bir istasyon ekler.  
    - `baglanti_ekle`: İki istasyon arasında çift yönlü bağlantı kurar.  
    - `en_az_aktarma_bul`: BFS algoritması ile minimum transfer içeren rota hesaplar.  
    -  en_hizli_rota_bul`: Dijkstra algoritmasına benzer bir yöntemle toplam süre üzerinden en hızlı rotayı bulur.  
    - `graf_goster`: Metro ağını NetworkX ve Matplotlib ile görselleştirir.
---
## Algoritmaların Çalışma Mantığı
### 1. En Az Aktarmalı Rota Bulma (BFS)
Yöntem: Breadth-First Search (BFS)
Nasıl Çalışır?
- Başlangıç: Başlangıç istasyonu, rota olarak kuyruk yapısına eklenir.
- Kuyruk İşlemi: Kuyruğun başındaki rota çıkarılır; rotanın sonundaki istasyon kontrol edilir.
- Kontrol: Eğer son istasyon hedef ise, o rota döndürülür.
- Genişleme: Son istasyonun tüm komşuları ziyaret edilir; daha önce ziyaret edilmemişse, yeni rota oluşturulur ve kuyruğa eklenir.
- Sonuç: Hedefe ulaşıncaya kadar bu adımlar tekrarlanır. Bu yöntem transfer (aktarma) sayısını minimize eder fakat seyahat sürelerini hesaba katmaz.
---
### 2. En Hızlı Rota Bulma (Dijkstra Benzeri)
Yöntem: Öncelikli Kuyruk (Min-Heap) kullanılarak Dijkstra algoritması benzeri yaklaşım
Nasıl Çalışır?
- Başlangıç: Başlangıç istasyonu, toplam maliyeti 0 olarak öncelikli kuyrukta başlatılır.
- Öncelik Kuyruğu: Kuyruktan en düşük maliyetli rota çıkarılır.
- Maliyet Hesaplama: Her komşu için, mevcut maliyet üzerine seyahat süresi eklenir; eğer bu toplam daha düşükse, o istasyonun rotası güncellenir ve öncelikli kuyruğa eklenir.
- Heuristic: Bu yaklaşımda, ekstra bir tahmin (heuristic) kullanılmamış olup, klasik Dijkstra algoritması gibi çalışmaktadır.
- Sonuç: Hedefe ulaşıldığında, oluşturulan rota ve toplam seyahat süresi döndürülür. Bu yöntem, toplam seyahat süresini minimize etmeye yöneliktir.
------
## Grafiksel Görselleştirme
Metro ağı,  NetworkX kullanılarak düğümler (istasyonlar) ve kenarlar (bağlantılar) şeklinde modellenir. Her istasyon:
- Düğüm: İstasyon adı ve hattı bilgisiyle etiketlenir; ilgili hatlara göre farklı renklerde gösterilir.
- Kenar: İki istasyon arasındaki bağlantılar, aktarma olup olmadığına göre stil olarak ayırt edilir:
  - Solid (Düz): Aynı hat içindeki direkt bağlantılar.
  - Dashed (Kesik): Farklı hatlar arası aktarma noktaları.
  
Yerleşim düzeni, `spring_layout` algoritması kullanılarak belirlenir ve Matplotlib ile grafiksel sunum sağlanır.
---
## Kurulum

- Python 3.7 veya üstü
- Aşağıdaki Python kütüphaneleri:
  - `networkx`
  - `matplotlib`

Örnek Kullanım Senaryoları ve Çıktılar
Projede, farklı senaryolar test edilmiştir:
	1. AŞTİ'den OSB'ye:
		○ En Az Aktarmalı Rota: BFS algoritması kullanılarak hesaplanır.
		○ En Hızlı Rota: Dijkstra benzeri algoritma ile toplam süre üzerinden belirlenir.
		○ Çıktı Örneği: AŞTİ -> Kızılay -> ... -> OSB şeklinde rota ve toplam süre konsola yazdırılır.
	2. Batıkent'ten Keçiören'e:
Hem minimum transfer hem de en hızlı rota hesaplamaları uygulanır.
	3. Keçiören'den AŞTİ'ye:
Transfer gerektiren güzergahların karşılaştırılması yapılır.

