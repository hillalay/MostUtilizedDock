import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta

def time_to_minutes(t_str):
    """'HH:MM' formatındaki saati günün başından itibaren dakikaya çevirir."""
    t = datetime.strptime(t_str, "%H:%M")
    return t.hour * 60 + t.minute

def build_U_from_logs(csv_path, R, delta_minutes=10):
    """
    Verilen CSV'den U (R x T) matrisini oluşturur.
    R: Toplam Dock sayısı
    delta_minutes: Her slotun kaç dakika olduğu
    """
    # 1. Veriyi Oku
    df = pd.read_csv(csv_path)
    
    # 2. T (Zaman Slotu Sayısı) Hesabı
    # 1 gün = 1440 dakika
    total_minutes = 1440 
    T = math.ceil(total_minutes / delta_minutes)
    
    # 3. Boş Matris Oluştur (R satır, T sütun)
    U = np.zeros((R, T), dtype=int)
    
    print(f"Veri İşleniyor... R={R}, T={T}, Slot Süresi={delta_minutes}dk")
    
    # 4. Logları Dön ve Matrisi Doldur
    for _, row in df.iterrows():
        dock_id = int(row['dock_id'])
        
        # Dock ID güvenliği (Eğer R'den büyük dock_id varsa hata vermesin, atlasın veya uyarın)
        if dock_id >= R:
            print(f"Uyarı: Dock ID {dock_id}, R={R} sınırının dışında. Atlanıyor.")
            continue
            
        start_min = time_to_minutes(row['arrival_time'])
        end_min = time_to_minutes(row['departure_time'])
        
        # Gece yarısı geçişi varsa (örn: 23:00 -> 02:00), günü bitirip başa sarma mantığı eklenebilir.
        # Ödev basitliği için 'end_min < start_min' ise sonraki gün sayıp 1440 ekleyebiliriz 
        # ya da o günü 23:59'da kesebiliriz. Basit yöntem:
        if end_min < start_min: 
            end_min += 1440 # Ertesi güne sarkma
            
        # Zaman aralığını slotlara çevir
        # Mantık: Eğer bir slotun herhangi bir kısmı bu aralığa denk geliyorsa 1 yap (Overlap kuralı)
        start_slot = math.floor(start_min / delta_minutes)
        end_slot = math.ceil(end_min / delta_minutes)
        
        # Slotları işaretle
        # min(end_slot, T) -> Günü aşan kısımları kesmek için
        for t in range(start_slot, min(end_slot, T)):
            U[dock_id, t] = 1
            
    return U, T

# --- TEST KISMI ---
if __name__ == "__main__":
    # Parametreler (Ödevde belirlediğimiz gibi)
    R_param = 10       # Dock Sayısı
    DELTA_param = 10   # 10 dakikalık slotlar
    CSV_FILE = "data/raw_logs.csv" # Dosya yolu
    
    try:
        U_matrix, T_calculated = build_U_from_logs(CSV_FILE, R_param, DELTA_param)
        
        # Sonuçları Raporla (Ödevin istediği Faz 1 çıktıları)
        total_ones = np.sum(U_matrix)
        total_elements = R_param * T_calculated
        sparsity = total_ones / total_elements
        
        print("\n--- FAZ 1 SONUÇLARI ---")
        print(f"Dock Sayısı (R): {R_param}")
        print(f"Zaman Slotu (T): {T_calculated}")
        print(f"Matris Boyutu  : {U_matrix.shape}")
        print(f"Toplam '1' Sayısı: {total_ones}")
        print(f"Doluluk Oranı (Sparsity): {sparsity:.4f}")
        print("\nİlk 5 Satır ve İlk 20 Sütun Önizleme:")
        print(U_matrix[:5, :20])
        print("\nBaşarılı! U matrisi oluşturuldu.")
        
    except FileNotFoundError:
        print(f"HATA: '{CSV_FILE}' dosyası bulunamadı. Lütfen data klasörünü kontrol et.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")