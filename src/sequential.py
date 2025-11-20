import numpy as np

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

    # 1) U'yu Numpy array'e çevir (liste de gelse sorun olmaz)
    U = np.array(U)

    # 2) En iyi satır index'i ve en iyi 1 sayısı için başlangıç değerleri
    best_row = 0
    best_count = -1

    # 3) Toplam satır sayısını al (R)
    R = U.shape[0]

    # 4) Her satırı sırayla gez
    for row_index in range(R):
        row = U[row_index]          # i. satırı al
        count = int(np.sum(row))    # o satırdaki 1'leri say

        # 5) Eğer bu satırdaki 1 sayısı, şu ana kadarki en iyiden büyükse → güncelle
        if count > best_count:
            best_count = count
            best_row = row_index

        # 6) Tie-handling (eşitlik durumu):
        # Eğer yeni satırın sayısı mevcut best_count'a eşitse
        # ve index daha küçükse, best_row'u güncelle.
        elif count == best_count and row_index < best_row:
            best_row = row_index

    # 7) En iyi satır index'i ve 1 sayısını döndür
    return best_row, best_count


# --- Mini test ---
def _mini_test():
    U_test = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]

    best_row, best_count = most_utilized_dock_sequential(U_test)

    print("FAZ 2 Mini Test Sonucu:")
    print("Beklenen row = 1, count = 3")
    print(f"Hesaplanan row = {best_row}, count = {best_count}")
    print("OK!" if best_row == 1 and best_count == 3 else "HATA!")



if __name__ == "__main__":
    _mini_test()