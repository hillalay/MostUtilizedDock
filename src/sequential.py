import numpy as np

# Bu dosyada "Most Utilized Dock" problemini
# en temel (sıralı / baseline) yöntemle çözdüğüm fonksiyon var.
# Amaç: U matrisinde en çok 1 içeren satırı (dock'u) bulmak.


def most_utilized_dock_sequential(U):
    """
    Most Utilized Dock - Sequential (Baseline) Method

    Parametreler
    ------------
    U : 2D array-like (R x T)
        Binary occupancy matrisi.
        U[i, t] = 1 ise: i. dock, t. zaman slotunda dolu.
        U[i, t] = 0 ise: boş.

    Dönüş
    ------
    best_row : int
        En çok 1 içeren satırın (dock'un) indeksi.
        Eşitlik (tie) durumunda en küçük satır indeksi.
    best_count : int
        Bu satırdaki 1'lerin sayısı.
    """

    # Burada U'yu numpy array'e çeviriyorum.
    # Böylece hem liste hem de numpy girdisi gelse sorunsuz çalışıyor.
    U = np.array(U)

    # En iyi satır index'ini ve o satırdaki 1 sayısını tutmak için
    # başlangıç değerlerini tanımladım.
    # best_count = -1 veriyorum ki ilk satır mutlaka bunu geçsin.
    best_row = 0
    best_count = -1

    # Toplam satır sayısını (dock sayısını) alıyorum.
    R = U.shape[0]

    # Bütün satırları (dock'ları) tek tek geziyorum.
    for row_index in range(R):
        # row: şu an baktığım satır (dock'un tüm zaman slotları)
        row = U[row_index]

        # Bu satırda kaç tane 1 olduğunu hesaplıyorum.
        # np.sum(row) → toplam 1 sayısı, int'e cast ediyorum.
        count = int(np.sum(row))

        # Eğer bu satırdaki 1 sayısı, şu ana kadarki en iyi değerden büyükse
        # direkt yeni "best" olarak güncelliyorum.
        if count > best_count:
            best_count = count
            best_row = row_index

        # Eğer eşitlik durumu varsa (count == best_count)
        # ve bu satırın index'i daha küçükse, ödeve göre
        # küçük index'i seçmem gerekiyor (tie-breaking).
        elif count == best_count and row_index < best_row:
            best_row = row_index

    # Dönen sonuç:
    # - best_row: en çok 1'e sahip satırın index'i
    # - best_count: o satırdaki toplam 1 sayısı
    return best_row, best_count


# --- Mini test ---

# Bu fonksiyon tamamen kendi kendime hızlı kontrol amaçlı.
# Küçük bir U matrisi üzerinde algoritmanın doğru çalışıp çalışmadığını test ediyorum.
def _mini_test():
    U_test = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]

    # Fonksiyonu örnek matris üzerinde çalıştırıyorum.
    best_row, best_count = most_utilized_dock_sequential(U_test)

    print("FAZ 2 Mini Test Sonucu:")
    print("Beklenen row = 1, count = 3")
    print(f"Hesaplanan row = {best_row}, count = {best_count}")

    # Burada da beklediğim sonuçla çıkan sonucu karşılaştırıyorum.
    # Küçük bir görsel feedback için "OK!" veya "HATA!" yazdırıyorum.
    print("OK!" if best_row == 1 and best_count == 3 else "HATA!")


# Bu dosyayı direkt çalıştırdığımda (python sequential.py)
# otomatik olarak mini testi koşturuyorum.
if __name__ == "__main__":
    _mini_test()