"""Tests for BitVec bitwise operations."""
import pytest
from bitvec import BitVec, BitVecError


class TestAnd:
    """Test __and__ (bitwise AND) operator."""

    def test_and_empty_vectors(self) -> None:
        """AND of two empty vectors."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        result = bv1 & bv2
        assert result.count() == 0

    def test_and_disjoint_sets(self) -> None:
        """AND of disjoint bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv2.set(1)
        bv2.set(3)
        result = bv1 & bv2
        assert result.count() == 0

    def test_and_overlapping_sets(self) -> None:
        """AND of overlapping bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv1.set(4)
        bv2.set(2)
        bv2.set(4)
        bv2.set(6)
        result = bv1 & bv2
        assert result.count() == 2
        assert result.get(2) is True
        assert result.get(4) is True

    def test_and_same_vector(self) -> None:
        """AND of vector with itself."""
        bv = BitVec(8)
        bv.set(3)
        bv.set(5)
        result = bv & bv
        assert result.count() == 2
        assert result.get(3) is True
        assert result.get(5) is True

    def test_and_different_sizes_raises(self) -> None:
        """AND of different-sized vectors raises error."""
        bv1 = BitVec(8)
        bv2 = BitVec(16)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv1 & bv2

    def test_and_returns_new_vector(self) -> None:
        """AND returns new vector, doesn't modify operands."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv2.set(0)
        result = bv1 & bv2
        bv1.clear(0)
        assert result.get(0) is True
        assert bv1.get(0) is False


class TestOr:
    """Test __or__ (bitwise OR) operator."""

    def test_or_empty_vectors(self) -> None:
        """OR of two empty vectors."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        result = bv1 | bv2
        assert result.count() == 0

    def test_or_disjoint_sets(self) -> None:
        """OR of disjoint bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv2.set(1)
        bv2.set(3)
        result = bv1 | bv2
        assert result.count() == 4
        assert result.get(0) is True
        assert result.get(1) is True
        assert result.get(2) is True
        assert result.get(3) is True

    def test_or_overlapping_sets(self) -> None:
        """OR of overlapping bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv2.set(2)
        bv2.set(4)
        result = bv1 | bv2
        assert result.count() == 3
        assert result.get(0) is True
        assert result.get(2) is True
        assert result.get(4) is True

    def test_or_same_vector(self) -> None:
        """OR of vector with itself."""
        bv = BitVec(8)
        bv.set(3)
        bv.set(5)
        result = bv | bv
        assert result.count() == 2
        assert result.get(3) is True
        assert result.get(5) is True

    def test_or_different_sizes_raises(self) -> None:
        """OR of different-sized vectors raises error."""
        bv1 = BitVec(8)
        bv2 = BitVec(16)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv1 | bv2

    def test_or_returns_new_vector(self) -> None:
        """OR returns new vector, doesn't modify operands."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv2.set(1)
        result = bv1 | bv2
        bv1.set(2)
        assert result.get(2) is False


class TestXor:
    """Test __xor__ (bitwise XOR) operator."""

    def test_xor_empty_vectors(self) -> None:
        """XOR of two empty vectors."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        result = bv1 ^ bv2
        assert result.count() == 0

    def test_xor_disjoint_sets(self) -> None:
        """XOR of disjoint bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv2.set(1)
        bv2.set(3)
        result = bv1 ^ bv2
        assert result.count() == 4
        assert result.get(0) is True
        assert result.get(1) is True
        assert result.get(2) is True
        assert result.get(3) is True

    def test_xor_identical_sets(self) -> None:
        """XOR of identical bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv2.set(0)
        bv2.set(2)
        result = bv1 ^ bv2
        assert result.count() == 0

    def test_xor_overlapping_sets(self) -> None:
        """XOR of overlapping bit sets."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv1.set(2)
        bv1.set(4)
        bv2.set(2)
        bv2.set(4)
        bv2.set(6)
        result = bv1 ^ bv2
        assert result.count() == 2
        assert result.get(0) is True
        assert result.get(6) is True

    def test_xor_different_sizes_raises(self) -> None:
        """XOR of different-sized vectors raises error."""
        bv1 = BitVec(8)
        bv2 = BitVec(16)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv1 ^ bv2

    def test_xor_self_is_zero(self) -> None:
        """XOR of vector with itself is zero."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv ^ bv
        assert result.count() == 0


class TestInvert:
    """Test __invert__ (bitwise NOT) operator."""

    def test_invert_empty(self) -> None:
        """Invert zero-initialized vector."""
        bv = BitVec(8)
        result = ~bv
        assert result.count() == 8
        for i in range(8):
            assert result.get(i) is True

    def test_invert_all_set(self) -> None:
        """Invert fully set vector."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = ~bv
        assert result.count() == 0

    def test_invert_mixed(self) -> None:
        """Invert mixed vector."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(2)
        bv.set(4)
        result = ~bv
        assert result.count() == 5
        assert result.get(0) is False
        assert result.get(1) is True
        assert result.get(2) is False

    def test_invert_non_aligned_size(self) -> None:
        """Invert with non-byte-aligned size masks trailing bits."""
        bv = BitVec(13)
        result = ~bv
        assert len(result) == 13
        assert result.count() == 13
