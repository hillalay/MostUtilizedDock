import numpy as np
from sequential import most_utilized_dock_sequential

def test_sequential():
    print("Running Sequential Tests...\n")

    # Test 1
    U1 = [
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
    row, count = most_utilized_dock_sequential(U1)
    assert row == 1 and count == 3
    print("Test 1 passed ✓")

    # Test 2 - tie-handling required
    U2 = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    row, count = most_utilized_dock_sequential(U2)
    assert row == 0 and count == 2
    print("Test 2 passed ✓")

    # Test 3
    U3 = [
        [0, 0, 0],
        [1, 0, 1],
        [1, 1, 1]
    ]
    row, count = most_utilized_dock_sequential(U3)
    assert row == 2 and count == 3
    print("Test 3 passed ✓")

    print("\nAll Sequential tests passed successfully!")


if __name__ == "__main__":
    test_sequential()
