import pandas as pd
import numpy as np
import time
import math
import os

# --- IMPORT ALGORITHMS ---
# Burada kendi yazdığım iki algoritmayı içeri alıyorum:
# - most_utilized_dock_sequential  → Sıralı (baseline) yöntem
# - most_utilized_dock_dc          → Divide & Conquer yöntemim
# Deney kısmında bu ikisini aynı matris üzerinde yarıştıracağım.
try:
    from sequential import most_utilized_dock_sequential
    from divide_conquer import most_utilized_dock_dc
except ImportError as e:
    # Eğer import kısmında sıkıntı varsa kullanıcıya net bir uyarı veriyorum.
    print("HATA: Algoritma dosyaları bulunamadı.")
    print("Lütfen 'sequential.py' ve 'divide_conquer.py' dosyalarının 'src' klasöründe olduğundan emin ol.")
    exit()


# --- FAZ 1: VERİ ÜRETİMİ (Opsiyonel - CSV Okuma) ---
# Bu fonksiyon, istersem küçük bir CSV dosyasından U matrisi oluşturmak için.
# Asıl deneylerde random matris kullanıyorum ama hocanın verdiği formatı da destekli kalsın istedim.
def build_U_from_logs(csv_path, R, delta_minutes=10):
    # Dosya yoksa None döndürüp T=0 veriyorum (kullanmak zorunda değilim).
    if not os.path.exists(csv_path):
        return None, 0

    df = pd.read_csv(csv_path)

    total_minutes = 1440  # 1 gün (24 * 60)
    T = math.ceil(total_minutes / delta_minutes)

    # Boyutu R x T olan, sıfırlarla dolu bir U matrisi oluşturuyorum.
    U = np.zeros((R, T), dtype=int)

    # Her satır bir dock kullanım kaydı (arrival/departure) temsil ediyor.
    for _, row in df.iterrows():
        dock_id = int(row['dock_id'])
        if dock_id >= R:
            continue  # Eğer dock_id benim tanımladığım R sınırının dışındaysa, o kaydı atlıyorum.

        # Başlangıç zamanı (HH:MM formatını parse ediyorum)
        h, m = map(int, row['arrival_time'].split(':'))
        start_min = h * 60 + m

        # Bitiş zamanı
        h_end, m_end = map(int, row['departure_time'].split(':'))
        end_min = h_end * 60 + m_end

        # Eğer bitiş başlangıçtan küçükse, demek ki gece yarısını geçti → 24 saat ekliyorum.
        if end_min < start_min:
            end_min += 1440

        # Zamanı dakikadan slot indeksine çeviriyorum.
        start_slot = math.floor(start_min / delta_minutes)
        end_slot = math.ceil(end_min / delta_minutes)

        # İlgili slot aralığını 1'liyorum (bu dock o zamanlarda dolu demek).
        for t in range(start_slot, min(end_slot, T)):
            U[dock_id, t] = 1

    return U, T


# --- FAZ 5: DENEY VE ÖLÇÜM FONKSİYONU ---
def run_all_experiments():
    """
    Farklı R ve T değerleri için algoritmaları yarıştırır, süreleri ölçer ve CSV'ye kaydeder.
    """
    # Burada deney senaryolarını manuel belirledim.
    # R: dock sayısı, T: zaman slotu sayısı.
    # T değeri büyüdükçe matris genişliyor ve algoritma daha zorlanıyor.
    configs = [
        {"R": 10,   "T": 144},   # Küçük senaryo (normal bir gün gibi)
        {"R": 50,   "T": 288},   # Orta seviye
        {"R": 100,  "T": 1000},  # Büyük senaryo
        {"R": 200,  "T": 2000},  # Daha büyük (D&C overhead burada daha net)
        # {"R": 500,  "T": 5000} # İstersem ekstra stres testi için bunu da açabilirim.
    ]

    results = []

    # Her konfigürasyonu birden fazla defa çalıştırıp ortalama alıyorum.
    # Böylece tek seferlik dalgalanmaları azaltmış oluyorum.
    N_RUNS = 5  # 5 tekrar bana yeterli diye düşündüm.

    print(f"--- FAZ 5: DENEY BAŞLIYOR ({len(configs)} Senaryo) ---")

    for cfg in configs:
        R_val = cfg["R"]
        T_val = cfg["T"]
        print(f"\nSenaryo Çalışıyor: R={R_val}, T={T_val}")

        # Her senaryoda, adil olsun diye aynı boyutta random binary U matrisi üretiyorum.
        # Gerçek CSV verisi sabit boyutlu olduğu için burada random tercih ettim.
        U_test = np.random.randint(0, 2, size=(R_val, T_val))

        # --- SEQUENTIAL ÖLÇÜMÜ ---
        start_time = time.perf_counter()
        seq_result = None

        # Aynı matris üzerinde N_RUNS defa sequential'ı koşturup süreyi ölçüyorum.
        for _ in range(N_RUNS):
            seq_result = most_utilized_dock_sequential(U_test)
        end_time = time.perf_counter()

        # Toplam süreyi tekrar sayısına bölüp milisaniyeye çeviriyorum.
        avg_time_seq = ((end_time - start_time) / N_RUNS) * 1000

        # ---  DIVIDE & CONQUER ÖLÇÜMÜ ---
        start_time = time.perf_counter()
        dc_result = None

        # Aynı şekilde D&C algoritmasını da N_RUNS defa çalıştırıyorum.
        for _ in range(N_RUNS):
            dc_result = most_utilized_dock_dc(U_test)
        end_time = time.perf_counter()

        avg_time_dc = ((end_time - start_time) / N_RUNS) * 1000

        # --- DOĞRULUK KONTROLÜ ---
        # İki algoritma da aynı problemi çözdüğü için,
        # çıkan sonuçların birebir aynı olmasını bekliyorum.
        if seq_result != dc_result:
            print(f"  HATA! Sonuçlar uyuşmuyor. Seq: {seq_result}, DC: {dc_result}")
        else:
            print(f"  Doğrulama: OK -> En Dolu Dock: {seq_result[0]} (Toplam: {seq_result[1]})")

        print(f"  Sequential Süre : {avg_time_seq:.4f} ms")
        print(f"  D&C Süre        : {avg_time_dc:.4f} ms")

        # Bu senaryonun sonuçlarını daha sonra CSV'ye dökmek için listeye ekliyorum.
        results.append({
            "R": R_val,
            "T": T_val,
            "Time_Seq_ms": avg_time_seq,
            "Time_DC_ms": avg_time_dc
        })

    #sonuçları data/results.csv dosyasına yazıyorum.
    if not os.path.exists("data"):
        os.makedirs("data")

    df_res = pd.DataFrame(results)
    df_res.to_csv("data/results.csv", index=False)

    print(f"\n--- Deney Tamamlandı! ---")
    print(f"Sonuçlar 'data/results.csv' dosyasına kaydedildi.")


# Bu dosyayı direkt çalıştırırsam (python run_experiment.py),
# otomatik olarak bütün deney senaryolarını koşturacak.
if __name__ == "__main__":
    run_all_experiments()
