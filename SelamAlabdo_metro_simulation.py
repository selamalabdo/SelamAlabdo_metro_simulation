from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import networkx as nx
import matplotlib.pyplot as plt

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        """Başlangıç ve hedef istasyon arasında en az aktarma gerektiren rotayı bulur."""
        # İstasyonların var olup olmadığını kontrolu
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        kuyruk = deque()
        kuyruk.append([baslangic])
        ziyaret_edildi = set([baslangic])
        
        while kuyruk:
            rota = kuyruk.popleft()
            son_istasyon = rota[-1]
            # Hedef istasyona ulaşıldığında rotayı döndür
            if son_istasyon == hedef:
                return rota
            # Komşuları kontrol etme
            for komsu, _ in son_istasyon.komsular:
                if komsu not in ziyaret_edildi:
                    ziyaret_edildi.add(komsu)
                    yeni_rota = rota + [komsu]
                    kuyruk.append(yeni_rota)
        
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
    # Dijkstra algoritmasına benzer şekilde, öncelikli kuyruk (min-heap) oluşturuyorum.
    # Kuyruğa; (toplam maliyet, istasyonun bellek adresi, istasyon nesnesi, o ana kadar geçen süre, rota listesi) şeklinde tuple ekliyorum.
        
        oncelik_kuyrugu = []
        heapq.heappush(oncelik_kuyrugu, (0, id(baslangic), baslangic, 0, [baslangic]))
        
        maliyetler = {baslangic: 0}
        
        while oncelik_kuyrugu:
            mevcut_priority, _, mevcut_istasyon, mevcut_maliyet, mevcut_rota = heapq.heappop(oncelik_kuyrugu)
            
            if mevcut_istasyon == hedef:
                return (mevcut_rota, mevcut_maliyet)
            
            for komsu, sure in mevcut_istasyon.komsular:
                yeni_maliyet = mevcut_maliyet + sure
                
                if komsu not in maliyetler or yeni_maliyet < maliyetler.get(komsu, float('inf')):
    # Yeni maliyeti saklıyorum.

                    maliyetler[komsu] = yeni_maliyet
    # Rotaya bu komşuyu ekliyorum.

                    yeni_rota = mevcut_rota + [komsu]
 

    # Yeni maliyet ve rota bilgisiyle, komşuyu öncelikli kuyruğa ekliyorum.
    # Burada heuristic olarak 0 kullanıyorum; yani Dijkstra algoritması gibi çalışıyor.

                    heapq.heappush(oncelik_kuyrugu, (yeni_maliyet, id(komsu), komsu, yeni_maliyet, yeni_rota))
    
    def graf_goster(self):
    # metro ağını grafik olarak çizmek için bu metodu kullanıyorum.    

        """
            NetworkX kütüphanesini kullanarak boş bir grafik oluşturuyorum.

        """
        G = nx.Graph()
        
    # Renk tanımlamaları
        hat_renkleri = {
            "Kırmızı Hat": "red",
            "Mavi Hat": "blue",
            "Turuncu Hat": "orange"
        }
        
    # Tüm istasyonları düğüm olarak grafiğe ekliyorum.
    # Her düğüm için, istasyon adı ve hattı bilgilerini etiket olarak atıyorum.

        for istasyon in self.istasyonlar.values():
            G.add_node(
                istasyon.idx, 
                label=f"{istasyon.ad}\n({istasyon.hat})",
                color=hat_renkleri.get(istasyon.hat, "gray")
            )
    # İstasyonlar arasındaki bağlantıları (kenarları) grafiğe ekliyorum.
    # Eğer iki istasyon farklı hatlardan ise, ben bu kenarı "dashed" (kesik çizgi) olarak,
    # aynı hat içindeyse "solid" (düz çizgi) olarak gösteriyorum.

        for istasyon in self.istasyonlar.values():
            for komsu, sure in istasyon.komsular:
                G.add_edge(
                    istasyon.idx, 
                    komsu.idx, 
                    weight=sure,
                    style="dashed" if istasyon.hat != komsu.hat else "solid"
                )
        
        # Pozisyonları belirledim
        pos = nx.spring_layout(G, seed=42)# Grafiğin düğümlerinin konumlarını spring_layout algoritmasıyla belirledim ,,  seed=42 ile aynı düzeni tekrar elde edebiliriz
        
    # Grafiğin çizim boyutlarını ayarlıyorum.
        plt.figure(figsize=(15,10))
        
    # Her düğüm için, daha önce belirlediğim renkleri kullanarak düğümleri çiziyorum.

        node_colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000)
        
    # Kenarları, stil bilgisine göre iki gruba ayırıyorum: solid ve dashed.

        solid_edges = [(u,v) for u,v,d in G.edges(data=True) if d['style'] == "solid"]
        dashed_edges = [(u,v) for u,v,d in G.edges(data=True) if d['style'] == "dashed"]

    # Solid kenarları düz çizgi ve kalınlık ile çiziyorum.

        nx.draw_networkx_edges(G, pos, edgelist=solid_edges, style="solid", width=2)
   
    # Dashed kenarları kesik çizgi ve hafif şeffaflık ile çiziyorum.
       
        nx.draw_networkx_edges(G, pos, edgelist=dashed_edges, style="dashed", alpha=0.5)
        
    # düğümlerin etiketlerini grafiğe ekliyorum.
        labels = {n: G.nodes[n]['label'] for n in G.nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=10)
        
    # Kenarların ağırlıklarını (süre bilgilerini) etiket olarak çiziyorum.
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # Grafiğe başlık ekliyorum, eksenleri kaldırıyor ve grafiği ekrana getiriyorum.
        plt.title("Ankara Metro Ağı")
        plt.axis("off")
        plt.show()

        return None


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

        print("\n=== Metro Ağ Görseli ===")
    metro.graf_goster()