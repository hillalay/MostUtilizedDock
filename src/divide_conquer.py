import numpy as np
from sequential import most_utilized_dock_sequential


def dc_column_sum(U, col_start, col_end):
    """
    Divide & Conquer sütun toplama fonksiyonu.

    U : 2D numpy array (R x T)
    col_start, col_end : [col_start, col_end) sütun aralığı
    """

    # Burada güvenli olması için U'yu numpy array'e çeviriyorum.
    # Böylece hem list hem de numpy gelse aynı şekilde çalışıyor.
    U = np.array(U)
    R, T = U.shape

    # Base case:
    # Eğer elimde sadece 1 sütun kalmışsa (col_end - col_start == 1),
    # o sütunun bütün satırlar için değerlerini direkt döndürüyorum.
    if col_end - col_start == 1:
        # R uzunluğunda bir vektör döndürüyorum: her satır için U[i, col_start]
        return U[:, col_start].astype(int)

    # Recursive case:
    # Sütun aralığını ortadan ikiye bölüyorum.
    mid = (col_start + col_end) // 2

    # Sol tarafın sütunlarını toplayan recursive çağrı
    left_counts = dc_column_sum(U, col_start, mid)
    # Sağ tarafın sütunlarını toplayan recursive çağrı
    right_counts = dc_column_sum(U, mid, col_end)

    # Combine aşaması:
    # Sol ve sağdan gelen vektörleri eleman eleman topluyorum.
    # Böylece her satır için toplam 1 sayısını elde etmiş oluyorum.
    total_counts = left_counts + right_counts
    return total_counts


def dc_argmax(counts, start, end):
    """
    Divide & Conquer ile max değer ve index bulma.

    counts : 1D array-like
    start, end : [start, end) index aralığı
    """

    # Yine güvenlik için numpy array'e çeviriyorum.
    counts = np.array(counts)

    # Base case:
    # Eğer aralıkta tek bir eleman kaldıysa (end - start == 1),
    # o elemanın index ve değerini geri döndürüyorum.
    if end - start == 1:
        return start, int(counts[start])

    # Recursive case:
    # Aralığı ortadan ikiye bölüyorum.
    mid = (start + end) // 2

    # Sol tarafta maksimumu bul
    left_index, left_value = dc_argmax(counts, start, mid)
    # Sağ tarafta maksimumu bul
    right_index, right_value = dc_argmax(counts, mid, end)

    # Şimdi bu iki sonucu kıyaslayıp, hangisinin daha büyük olduğuna karar veriyorum.
    if left_value > right_value:
        return left_index, left_value
    elif right_value > left_value:
        return right_index, right_value
    else:
        # Buraya geldiysem değerler eşit demektir.
        # Ödevin tie-breaking kuralına göre index'i küçük olan kazanıyor.
        if left_index < right_index:
            return left_index, left_value
        else:
            return right_index, right_value


def most_utilized_dock_dc(U):
    """
    Most Utilized Dock - Divide & Conquer Method

    Adımlar:
    1) U matrisi sütunlar boyunca D&C ile toplanır → counts (her satır için toplam 1 sayısı)
    2) counts üzerinde D&C argmax ile en büyük değer ve satır indeksi bulunur.
    """

    # Yine gelen U'yu numpy array'e çeviriyorum.
    U = np.array(U)
    R, T = U.shape

    # 1) Önce bütün sütunları D&C ile toplayıp
    # her satır için toplam 1 sayısını içeren bir vektör elde ediyorum.
    counts = dc_column_sum(U, 0, T)

    # 2) Sonra bu vektör üzerinde D&C argmax ile
    # en yüksek değeri ve o değerin satır index'ini buluyorum.
    best_row, best_count = dc_argmax(counts, 0, R)

    # Sonuç: Sequential fonksiyonla aynı tipte (row_index, count) dönüyorum.
    return best_row, best_count


# --- Mini test: Sequential ile aynı sonucu veriyor mu? ---

# Bu fonksiyonu, Divide & Conquer versiyonunu
# Sequential fonksiyon ile kıyaslamak için yazdım.
# Ödevde iki yöntem de aynı sonucu vermeli, burada onu kontrol ediyorum.
def _mini_test_dc():
    U_test = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]

    # Sequential yöntemle sonucu alıyorum.
    s_row, s_count = most_utilized_dock_sequential(U_test)
    # Divide & Conquer yöntemle sonucu alıyorum.
    d_row, d_count = most_utilized_dock_dc(U_test)

    print("Sequential:", s_row, s_count)
    print("D&C       :", d_row, d_count)

    # Eğer iki sonuç birebir aynı değilse assertion ile hata fırlatıyorum.
    assert (s_row, s_count) == (d_row, d_count), \
        f"HATA! Sequential sonucu {s_row, s_count}, D&C sonucu {d_row, d_count}"

    print("OK! D&C sonucu Sequential ile aynı.")


# Dosyayı direkt çalıştırdığımda (python divide_conquer.py)
# otomatik olarak bu mini test koşsun istedim.
if __name__ == "__main__":
    _mini_test_dc()
