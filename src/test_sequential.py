import numpy as np
from sequential import most_utilized_dock_sequential

# Bu dosyada Sequential fonksiyonum için küçük unit testler yazdım.
# Amacım: Farklı U matrislerinde beklediğim sonucu veriyor mu diye hızlıca kontrol etmek.


def test_sequential():
    print("Running Sequential Tests...\n")

    # Test 1
    # Burada 3x3 küçük bir U matrisi kullandım.
    # En dolu satır: 1. index (ikinci satır) → toplam 3 tane 1 var.
    U1 = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
    row, count = most_utilized_dock_sequential(U1)
    assert row == 1 and count == 3
    print("Test 1 passed ✓")

    # Test 2 - tie-handling required
    # İkinci testte eşitlik durumunu özellikle kontrol ediyorum.
    # İlk iki satırda da toplam 2'şer tane 1 var.
    # Ödevin kuralına göre index'i küçük olan kazanmalı → 0 dönmesini bekliyorum.
    U2 = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    row, count = most_utilized_dock_sequential(U2)
    assert row == 0 and count == 2
    print("Test 2 passed ✓")

    # Test 3
    # Bu testte de en dolu satırın en altta olduğu bir senaryo kurdum.
    # En dolu dock: index 2, toplam 3 tane 1.
    U3 = [
        [0, 0, 0],
        [1, 0, 1],
        [1, 1, 1]
    ]
    row, count = most_utilized_dock_sequential(U3)
    assert row == 2 and count == 3
    print("Test 3 passed ✓")

    print("\nAll Sequential tests passed successfully!")


# Dosyayı direkt çalıştırırsam (python test_sequential.py),
# bütün testleri koşup başarı durumunu ekrana yazdırıyor.
if __name__ == "__main__":
    test_sequential()
