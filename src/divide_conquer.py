import numpy as np
from sequential import most_utilized_dock_sequential


def dc_column_sum(U, col_start, col_end):
    """
    Divide & Conquer sütun toplama fonksiyonu.

    U : 2D numpy array (R x T)
    col_start, col_end : [col_start, col_end) sütun aralığı
    """
    U = np.array(U)
    R, T = U.shape

    # Base case: Tek sütun kaldıysa, o sütunun değerlerini döndür
    if col_end - col_start == 1:
        # R uzunluğunda vektör: her satır için U[i, col_start]
        return U[:, col_start].astype(int)

    # Recursive case: Sütun aralığını ikiye böl
    mid = (col_start + col_end) // 2

    left_counts = dc_column_sum(U, col_start, mid)
    right_counts = dc_column_sum(U, mid, col_end)

    # Combine: sol ve sağ vektörleri eleman eleman topla
    total_counts = left_counts + right_counts
    return total_counts


def dc_argmax(counts, start, end):
    """
    Divide & Conquer ile max değer ve index bulma.

    counts : 1D array-like
    start, end : [start, end) index aralığı
    """
    counts = np.array(counts)

    # Base case: Tek eleman
    if end - start == 1:
        return start, int(counts[start])

    # Recursive case: Aralığı ikiye böl
    mid = (start + end) // 2

    left_index, left_value = dc_argmax(counts, start, mid)
    right_index, right_value = dc_argmax(counts, mid, end)

    # Karşılaştırma + tie-handling
    if left_value > right_value:
        return left_index, left_value
    elif right_value > left_value:
        return right_index, right_value
    else:
        # Tie: daha küçük index kazansın
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
    U = np.array(U)
    R, T = U.shape

    counts = dc_column_sum(U, 0, T)
    best_row, best_count = dc_argmax(counts, 0, R)

    return best_row, best_count


# --- Mini test: Sequential ile aynı sonucu veriyor mu? ---
def _mini_test_dc():
    U_test = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]

    s_row, s_count = most_utilized_dock_sequential(U_test)
    d_row, d_count = most_utilized_dock_dc(U_test)

    print("Sequential:", s_row, s_count)
    print("D&C       :", d_row, d_count)

    if (s_row, s_count) == (d_row, d_count):
        print("OK! D&C sonucu Sequential ile aynı.")
    else:
        print("HATA! Sonuçlar farklı.")


if __name__ == "__main__":
    _mini_test_dc()
