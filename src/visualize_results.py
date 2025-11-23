import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math

# Bu dosyada gerçek hocanın verisini kullanarak:
# - U matrisini oluşturuyorum
# - Heatmap ve bar chart çizip figures klasörüne kaydediyorum.


# --- 1. VERİ SETİNİ OLUŞTUR (Eğer yoksa) ---
def ensure_data_exists():
    # data klasörü yoksa oluşturuyorum.
    if not os.path.exists("data"):
        os.makedirs("data")

    file_path = "data/raw_logs.csv"

    # Buradaki csv_content, hocanın verdiği gerçek veriyi temsil ediyor.
    # Eğer dosya zaten varsa bile üzerine yazıyorum ki format garanti olsun.
    csv_content = """date,dock_id,truck_id,carrier,order_id,arrival_time,departure_time,load_type,weight_kg,priority,facility_timezone
2025-10-29,Dock-1,TRK-1001,Anadolu Logistics,ORD-50001,2025-10-29 08:04,2025-10-29 09:28,inbound,20558,normal,Europe/Istanbul
2025-10-29,Dock-1,TRK-1002,EgeKargo,ORD-50002,2025-10-29 10:18,2025-10-29 11:34,outbound,6967,normal,Europe/Istanbul
2025-10-29,Dock-1,TRK-1003,Bosphorus Freight,ORD-50003,2025-10-29 12:18,2025-10-29 13:54,outbound,14897,high,Europe/Istanbul
2025-10-29,Dock-1,TRK-1004,Bosphorus Freight,ORD-50004,2025-10-29 14:14,2025-10-29 14:48,outbound,19982,normal,Europe/Istanbul
2025-10-29,Dock-1,TRK-1005,EgeKargo,ORD-50005,2025-10-29 15:11,2025-10-29 16:03,outbound,12082,low,Europe/Istanbul
2025-10-29,Dock-1,TRK-1006,EgeKargo,ORD-50006,2025-10-29 16:52,2025-10-29 18:35,outbound,15623,low,Europe/Istanbul
2025-10-29,Dock-1,TRK-1007,Bosphorus Freight,ORD-50007,2025-10-29 18:45,2025-10-29 19:54,inbound,4225,normal,Europe/Istanbul
2025-10-29,Dock-1,TRK-1008,Bosphorus Freight,ORD-50008,2025-10-29 20:40,2025-10-29 21:20,outbound,22995,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1009,Aegean Express,ORD-50009,2025-10-29 07:29,2025-10-29 08:20,outbound,4537,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1010,Aegean Express,ORD-50010,2025-10-29 08:52,2025-10-29 09:52,outbound,5306,high,Europe/Istanbul
2025-10-29,Dock-2,TRK-1011,Bosphorus Freight,ORD-50011,2025-10-29 10:13,2025-10-29 12:02,outbound,16281,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1012,Bosphorus Freight,ORD-50012,2025-10-29 12:12,2025-10-29 12:49,inbound,6716,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1013,Bosphorus Freight,ORD-50013,2025-10-29 13:07,2025-10-29 14:54,outbound,21886,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1014,MarmaraTrans,ORD-50014,2025-10-29 15:35,2025-10-29 17:15,outbound,3419,normal,Europe/Istanbul
2025-10-29,Dock-2,TRK-1015,Anadolu Logistics,ORD-50015,2025-10-29 17:34,2025-10-29 19:01,outbound,8617,low,Europe/Istanbul
2025-10-29,Dock-2,TRK-1016,EgeKargo,ORD-50016,2025-10-29 19:27,2025-10-29 20:36,outbound,10504,high,Europe/Istanbul
2025-10-29,Dock-2,TRK-1017,EgeKargo,ORD-50017,2025-10-29 20:46,2025-10-29 22:00,inbound,15077,normal,Europe/Istanbul
2025-10-29,Dock-3,TRK-1018,MarmaraTrans,ORD-50018,2025-10-29 07:34,2025-10-29 08:47,inbound,8070,high,Europe/Istanbul
2025-10-29,Dock-3,TRK-1019,Anadolu Logistics,ORD-50019,2025-10-29 09:27,2025-10-29 11:13,outbound,13699,high,Europe/Istanbul
2025-10-29,Dock-3,TRK-1020,Anadolu Logistics,ORD-50020,2025-10-29 11:29,2025-10-29 12:43,inbound,23667,high,Europe/Istanbul
2025-10-29,Dock-3,TRK-1021,Aegean Express,ORD-50021,2025-10-29 13:12,2025-10-29 14:10,outbound,7596,low,Europe/Istanbul
2025-10-29,Dock-3,TRK-1022,Anadolu Logistics,ORD-50022,2025-10-29 14:30,2025-10-29 15:04,outbound,23255,normal,Europe/Istanbul
2025-10-29,Dock-3,TRK-1023,Anadolu Logistics,ORD-50023,2025-10-29 15:32,2025-10-29 17:08,inbound,9927,normal,Europe/Istanbul
2025-10-29,Dock-3,TRK-1024,Aegean Express,ORD-50024,2025-10-29 17:22,2025-10-29 18:24,outbound,14586,normal,Europe/Istanbul
2025-10-29,Dock-3,TRK-1025,Aegean Express,ORD-50025,2025-10-29 19:17,2025-10-29 21:03,inbound,5962,low,Europe/Istanbul
2025-10-29,Dock-3,TRK-1026,EgeKargo,ORD-50026,2025-10-29 21:22,2025-10-29 21:52,outbound,22004,normal,Europe/Istanbul
2025-10-29,Dock-4,TRK-1027,Bosphorus Freight,ORD-50027,2025-10-29 07:49,2025-10-29 08:57,inbound,13474,high,Europe/Istanbul
2025-10-29,Dock-4,TRK-1028,MarmaraTrans,ORD-50028,2025-10-29 09:21,2025-10-29 10:26,inbound,2204,normal,Europe/Istanbul
2025-10-29,Dock-4,TRK-1029,Bosphorus Freight,ORD-50029,2025-10-29 11:09,2025-10-29 11:43,outbound,9401,normal,Europe/Istanbul
2025-10-29,Dock-4,TRK-1030,Bosphorus Freight,ORD-50030,2025-10-29 11:54,2025-10-29 13:21,outbound,19896,low,Europe/Istanbul
2025-10-29,Dock-4,TRK-1031,Aegean Express,ORD-50031,2025-10-29 13:47,2025-10-29 15:21,inbound,23388,low,Europe/Istanbul
2025-10-29,Dock-4,TRK-1032,Bosphorus Freight,ORD-50032,2025-10-29 15:32,2025-10-29 17:14,outbound,18783,low,Europe/Istanbul
2025-10-29,Dock-4,TRK-1033,Aegean Express,ORD-50033,2025-10-29 17:29,2025-10-29 18:32,outbound,10937,high,Europe/Istanbul
2025-10-29,Dock-4,TRK-1034,Aegean Express,ORD-50034,2025-10-29 19:25,2025-10-29 20:03,inbound,21761,normal,Europe/Istanbul
2025-10-29,Dock-4,TRK-1035,MarmaraTrans,ORD-50035,2025-10-29 20:42,2025-10-29 22:00,outbound,13214,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1036,Bosphorus Freight,ORD-50036,2025-10-29 07:03,2025-10-29 07:48,inbound,24525,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1037,Aegean Express,ORD-50037,2025-10-29 08:06,2025-10-29 09:48,outbound,22554,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1038,Aegean Express,ORD-50038,2025-10-29 10:14,2025-10-29 10:52,outbound,14851,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1039,Aegean Express,ORD-50039,2025-10-29 11:10,2025-10-29 12:11,outbound,9860,high,Europe/Istanbul
2025-10-29,Dock-5,TRK-1040,Bosphorus Freight,ORD-50040,2025-10-29 12:36,2025-10-29 13:30,inbound,2462,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1041,Anadolu Logistics,ORD-50041,2025-10-29 14:22,2025-10-29 16:01,outbound,13899,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1042,Aegean Express,ORD-50042,2025-10-29 16:36,2025-10-29 18:24,outbound,20306,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1043,EgeKargo,ORD-50043,2025-10-29 18:49,2025-10-29 19:30,outbound,4062,high,Europe/Istanbul
2025-10-29,Dock-5,TRK-1044,MarmaraTrans,ORD-50044,2025-10-29 19:52,2025-10-29 20:29,inbound,8850,normal,Europe/Istanbul
2025-10-29,Dock-5,TRK-1045,MarmaraTrans,ORD-50045,2025-10-29 21:21,2025-10-29 22:00,inbound,4889,normal,Europe/Istanbul
2025-10-29,Dock-6,TRK-1046,MarmaraTrans,ORD-50046,2025-10-29 06:56,2025-10-29 08:39,inbound,6472,normal,Europe/Istanbul
2025-10-29,Dock-6,TRK-1047,MarmaraTrans,ORD-50047,2025-10-29 09:25,2025-10-29 11:02,inbound,5250,low,Europe/Istanbul
2025-10-29,Dock-6,TRK-1048,MarmaraTrans,ORD-50048,2025-10-29 11:38,2025-10-29 12:16,inbound,877,high,Europe/Istanbul
2025-10-29,Dock-6,TRK-1049,MarmaraTrans,ORD-50049,2025-10-29 12:59,2025-10-29 14:17,outbound,18465,low,Europe/Istanbul
2025-10-29,Dock-6,TRK-1050,Aegean Express,ORD-50050,2025-10-29 15:07,2025-10-29 16:15,outbound,17596,high,Europe/Istanbul
2025-10-29,Dock-6,TRK-1051,Aegean Express,ORD-50051,2025-10-29 16:32,2025-10-29 17:49,outbound,13463,high,Europe/Istanbul
2025-10-29,Dock-6,TRK-1052,EgeKargo,ORD-50052,2025-10-29 18:19,2025-10-29 19:41,inbound,4918,low,Europe/Istanbul
2025-10-29,Dock-6,TRK-1053,Anadolu Logistics,ORD-50053,2025-10-29 20:07,2025-10-29 21:01,inbound,6917,normal,Europe/Istanbul
2025-10-29,Dock-6,TRK-1054,Aegean Express,ORD-50054,2025-10-29 21:16,2025-10-29 22:00,inbound,24317,low,Europe/Istanbul"""

    with open(file_path, "w", encoding='utf-8') as f:
        f.write(csv_content)

    print("✅ Gerçek veri seti (data/raw_logs.csv) oluşturuldu/güncellendi.")


# --- 2. U MATRİSİNİ HESAPLA (Gerçek Formata Göre) ---
def build_U(csv_path, R=6, delta=10):
    # CSV'yi pandas ile okuyorum.
    df = pd.read_csv(csv_path)

    total_minutes = 1440  # 1 gün
    T = math.ceil(total_minutes / delta)

    # U: R x T boyutunda sıfırlarla dolu bir occupancy matrisi.
    U = np.zeros((R, T), dtype=int)

    for _, row in df.iterrows():
        # Dock ID "Dock-1" gibi string geliyor.
        # Burada '1' kısmını alıp index'e çeviriyorum.
        dock_str = row['dock_id']  # "Dock-1"
        try:
            dock_num = int(dock_str.split('-')[1])  # 1
            dock_idx = dock_num - 1                # 0 tabanlı index
        except:
            continue  # Format bozuksa o kaydı es geçiyorum.

        if dock_idx >= R:
            continue

        # Tarih/saat formatı "2025-10-29 08:04" şeklinde.
        # Benim için HH:MM kısmı yeterli.
        start_full = row['arrival_time']
        end_full = row['departure_time']

        h1, m1 = map(int, start_full.split(' ')[1].split(':'))
        t_start = h1 * 60 + m1

        h2, m2 = map(int, end_full.split(' ')[1].split(':'))
        t_end = h2 * 60 + m2

        # Gece yarısını geçiyorsa düzeltme yapıyorum.
        if t_end < t_start:
            t_end += 1440

        # Dakikayı slot index'ine çeviriyorum.
        s_start = math.floor(t_start / delta)
        s_end = math.ceil(t_end / delta)

        # Bu aralıktaki slotları 1 yapıyorum.
        for t in range(s_start, min(s_end, T)):
            U[dock_idx, t] = 1

    return U, T


# --- 3. ÇİZİM VE KAYIT ---
def plot_all():
    # Önce gerçek verinin data/raw_logs.csv olarak hazır olduğundan emin oluyorum.
    ensure_data_exists()

    # figures klasörü yoksa oluşturuyorum.
    if not os.path.exists("figures"):
        os.makedirs("figures")

    # Hocanın verisinde 6 tane dock var (Dock-1 ... Dock-6)
    REAL_R = 6
    U, T = build_U("data/raw_logs.csv", R=REAL_R)

    # 3.1 HEATMAP
    plt.figure(figsize=(14, 6))

    # U matrisini heatmap olarak çiziyorum.
    # Viridis colormap: yoğunluk arttıkça renk değişiyor.
    plt.imshow(U, aspect='auto', cmap='viridis', interpolation='nearest')

    # X ekseni için saat etiketleri (örnek olarak her 6 slotta bir).
    hour_ticks = range(0, T, 6)
    hour_labels = [f"{int(h * 10 / 60):02d}:00" for h in hour_ticks]
    plt.xticks(hour_ticks, hour_labels, rotation=45)

    # Y ekseni için dock isimlerini yazıyorum.
    plt.yticks(range(REAL_R), [f"Dock-{i+1}" for i in range(REAL_R)])

    plt.title("Dock Occupancy Heatmap (Actual Data)")
    plt.xlabel("Time")
    plt.ylabel("Docks")
    plt.colorbar(label="Occupancy")
    plt.tight_layout()

    # Heatmap'i figures klasörüne kaydediyorum.
    plt.savefig("figures/heatmap.png", dpi=300)
    print("✅ figures/heatmap.png güncellendi (Gerçek Veriyle!).")

    # 3.2 BAR CHART
    # Her satır (dock) için toplam 1 sayısını hesaplıyorum.
    counts = [np.sum(row) for row in U]

    plt.figure(figsize=(10, 6))
    plt.bar(range(REAL_R), counts, color='#ffc107', edgecolor='black')
    plt.xticks(range(REAL_R), [f"Dock-{i+1}" for i in range(REAL_R)])
    plt.title("Total Occupied Slots per Dock")
    plt.xlabel("Docks")
    plt.ylabel("Count")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    # Bar chart'ı da kaydediyorum.
    plt.savefig("figures/bar_totals.png", dpi=300)
    print("✅ figures/bar_totals.png güncellendi.")


# Bu dosyayı direkt çalıştırırsam:
# → hem veriyi oluşturuyor
# → hem de görselleri üretip figures klasörüne atıyor.
if __name__ == "__main__":
    plot_all()
