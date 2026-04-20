"""Tests for BitVec construction and creation methods."""
import pytest
from bitvec import BitVec, BitVecError


class TestBasicConstruction:
    """Test BitVec() constructor."""

    def test_zero_size(self) -> None:
        """Empty bit vector of size 0."""
        bv = BitVec(0)
        assert len(bv) == 0

    def test_small_size(self) -> None:
        """Small bit vector is zero-initialized."""
        bv = BitVec(8)
        assert len(bv) == 8
        assert bv.count() == 0

    def test_non_aligned_size(self) -> None:
        """Size not aligned to byte boundary (e.g., size=13)."""
        bv = BitVec(13)
        assert len(bv) == 13
        assert bv.count() == 0

    def test_large_size(self) -> None:
        """Very large bit vector (size=10000)."""
        bv = BitVec(10000)
        assert len(bv) == 10000
        assert bv.count() == 0

    def test_negative_size(self) -> None:
        """Negative size raises error."""
        with pytest.raises((ValueError, BitVecError)):
            BitVec(-1)


class TestFromBytes:
    """Test BitVec.from_bytes() constructor."""

    def test_from_bytes_aligned(self) -> None:
        """Create from bytes with aligned size."""
        data = b'\xFF\x00'
        bv = BitVec.from_bytes(data, 16)
        assert len(bv) == 16
        assert bv.count() == 8

    def test_from_bytes_non_aligned(self) -> None:
        """Create from bytes with non-aligned size."""
        data = b'\xFF'
        bv = BitVec.from_bytes(data, 5)
        assert len(bv) == 5
        assert bv.count() == 5

    def test_from_bytes_insufficient_bytes(self) -> None:
        """from_bytes with insufficient bytes raises error."""
        data = b'\xFF'
        with pytest.raises((ValueError, BitVecError)):
            BitVec.from_bytes(data, 16)

    def test_from_bytes_excess_bytes(self) -> None:
        """from_bytes with excess bytes ignores them."""
        data = b'\xFF\xAA\xBB'
        bv = BitVec.from_bytes(data, 16)
        assert len(bv) == 16

    def test_from_bytes_zero_size(self) -> None:
        """from_bytes with size=0 and no data."""
        bv = BitVec.from_bytes(b'', 0)
        assert len(bv) == 0

    def test_from_bytes_single_bit(self) -> None:
        """from_bytes with size=1."""
        bv = BitVec.from_bytes(b'\x01', 1)
        assert len(bv) == 1
        assert bv.get(0) is True


class TestFromIterable:
    """Test BitVec.from_iterable() constructor."""

    def test_from_iterable_empty(self) -> None:
        """Create from empty iterable."""
        bv = BitVec.from_iterable([], 8)
        assert len(bv) == 8
        assert bv.count() == 0

    def test_from_iterable_single(self) -> None:
        """Create from iterable with single bit."""
        bv = BitVec.from_iterable([5], 8)
        assert len(bv) == 8
        assert bv.count() == 1
        assert bv.get(5) is True

    def test_from_iterable_multiple(self) -> None:
        """Create from iterable with multiple bits."""
        bv = BitVec.from_iterable([0, 2, 4, 6], 8)
        assert len(bv) == 8
        assert bv.count() == 4
        assert bv.get(0) is True
        assert bv.get(2) is True
        assert bv.get(4) is True
        assert bv.get(6) is True
        assert bv.get(1) is False

    def test_from_iterable_duplicates(self) -> None:
        """from_iterable with duplicate indices."""
        bv = BitVec.from_iterable([3, 3, 3], 8)
        assert len(bv) == 8
        assert bv.count() == 1
        assert bv.get(3) is True

    def test_from_iterable_out_of_range(self) -> None:
        """from_iterable with index >= size raises error."""
        with pytest.raises((IndexError, BitVecError)):
            BitVec.from_iterable([8], 8)

    def test_from_iterable_negative_index(self) -> None:
        """from_iterable with negative index raises error."""
        with pytest.raises((IndexError, BitVecError)):
            BitVec.from_iterable([-1], 8)

    def test_from_iterable_large_vector(self) -> None:
        """from_iterable on large vector."""
        indices = [100, 500, 1000, 5000]
        bv = BitVec.from_iterable(indices, 10000)
        assert len(bv) == 10000
        assert bv.count() == 4
        for idx in indices:
            assert bv.get(idx) is True


class TestConstructionEdgeCases:
    """Edge cases and error conditions for construction."""

    def test_size_is_positive(self) -> None:
        """Size must be non-negative."""
        BitVec(0)
        BitVec(1)

    def test_from_bytes_empty_with_zero_size(self) -> None:
        """Empty bytes with size=0 should work."""
        bv = BitVec.from_bytes(b'', 0)
        assert len(bv) == 0

    def test_construction_preserves_size(self) -> None:
        """All construction methods preserve exact size."""
        bv1 = BitVec(13)
        assert len(bv1) == 13
        bv2 = BitVec.from_bytes(b'\x00\x00', 13)
        assert len(bv2) == 13
        bv3 = BitVec.from_iterable([], 13)
        assert len(bv3) == 13
