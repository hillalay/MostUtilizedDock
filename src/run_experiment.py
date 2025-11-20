import pandas as pd
import numpy as np
import time
import math
import os

# --- IMPORT ALGORITHMS ---
# src klasöründeki diğer dosyalarımızı dahil ediyoruz
try:
    from sequential import most_utilized_dock_sequential
    from divide_conquer import most_utilized_dock_dc
except ImportError as e:
    print("HATA: Algoritma dosyaları bulunamadı.")
    print("Lütfen 'sequential.py' ve 'divide_conquer.py' dosyalarının 'src' klasöründe olduğundan emin ol.")
    exit()

# --- FAZ 1: VERİ ÜRETİMİ (Opsiyonel - CSV Okuma) ---
# Bu fonksiyonu gerçek veriyi okumak istersek diye tutuyoruz
def build_U_from_logs(csv_path, R, delta_minutes=10):
    if not os.path.exists(csv_path):
        return None, 0
    df = pd.read_csv(csv_path)
    total_minutes = 1440 
    T = math.ceil(total_minutes / delta_minutes)
    U = np.zeros((R, T), dtype=int)
    for _, row in df.iterrows():
        dock_id = int(row['dock_id'])
        if dock_id >= R: continue
        h, m = map(int, row['arrival_time'].split(':'))
        start_min = h * 60 + m
        h_end, m_end = map(int, row['departure_time'].split(':'))
        end_min = h_end * 60 + m_end
        if end_min < start_min: end_min += 1440
        start_slot = math.floor(start_min / delta_minutes)
        end_slot = math.ceil(end_min / delta_minutes)
        for t in range(start_slot, min(end_slot, T)):
            U[dock_id, t] = 1
    return U, T

# --- FAZ 5: DENEY VE ÖLÇÜM FONKSİYONU ---
def run_all_experiments():
    """
    Farklı R ve T değerleri için algoritmaları yarıştırır, süreleri ölçer ve CSV'ye kaydeder.
    """
    
    # 1. TEST SENARYOLARI (CONFIGS)
    # Bilgisayarını kastırmadan algoritma farklarını göreceğimiz senaryolar
    configs = [
        {"R": 10,   "T": 144},   # Küçük (Normal bir gün)
        {"R": 50,   "T": 288},   # Orta
        {"R": 100,  "T": 1000},  # Büyük
        {"R": 200,  "T": 2000},  # Daha Büyük (D&C farkı burada açılmaya başlar)
       # {"R": 500,  "T": 5000}   # Stress Test (Yavaşlarsa bunu listeden çıkarabilirsin)
    ]
    
    results = []
    N_RUNS = 5 # Her testi 10 kere yapıp ortalamasını alacağız (Güvenilirlik için)
    
    print(f"--- FAZ 5: DENEY BAŞLIYOR ({len(configs)} Senaryo) ---")
    
    for cfg in configs:
        R_val = cfg["R"]
        T_val = cfg["T"]
        print(f"\nSenaryo Çalışıyor: R={R_val}, T={T_val}")
        
        # Rastgele Binary Matris Üretimi (Adil test için)
        # Gerçek CSV verisi sabit boyutlu olduğu için, büyük R ve T testlerinde random kullanıyoruz.
        U_test = np.random.randint(0, 2, size=(R_val, T_val))
        
        # --- A) SEQUENTIAL ÖLÇÜMÜ ---
        start_time = time.perf_counter()
        seq_result = None
        for _ in range(N_RUNS):
            seq_result = most_utilized_dock_sequential(U_test)
        end_time = time.perf_counter()
        # Toplam süreyi tekrar sayısına bölüp milisaniyeye çeviriyoruz
        avg_time_seq = ((end_time - start_time) / N_RUNS) * 1000 
        
        # --- B) DIVIDE & CONQUER ÖLÇÜMÜ ---
        start_time = time.perf_counter()
        dc_result = None
        for _ in range(N_RUNS):
            dc_result = most_utilized_dock_dc(U_test)
        end_time = time.perf_counter()
        avg_time_dc = ((end_time - start_time) / N_RUNS) * 1000 
        
        # --- C) DOĞRULUK KONTROLÜ ---
        if seq_result != dc_result:
            print(f"  HATA! Sonuçlar uyuşmuyor. Seq: {seq_result}, DC: {dc_result}")
        else:
            print(f"  Doğrulama: OK -> En Dolu Dock: {seq_result[0]} (Toplam: {seq_result[1]})")

        print(f"  Sequential Süre : {avg_time_seq:.4f} ms")
        print(f"  D&C Süre        : {avg_time_dc:.4f} ms")
        
        # Sonuçları kaydet
        results.append({
            "R": R_val,
            "T": T_val,
            "Time_Seq_ms": avg_time_seq,
            "Time_DC_ms": avg_time_dc
        })

    # CSV Çıktısı
    if not os.path.exists("data"):
        os.makedirs("data")
        
    df_res = pd.DataFrame(results)
    df_res.to_csv("data/results.csv", index=False)
    print(f"\n--- Deney Tamamlandı! ---")
    print(f"Sonuçlar 'data/results.csv' dosyasına kaydedildi.")

if __name__ == "__main__":
    run_all_experiments()