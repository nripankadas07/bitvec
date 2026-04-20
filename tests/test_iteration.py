"""Tests for BitVec iteration and container protocol."""
import pytest
from bitvec import BitVec, BitVecError


class TestLen:
    """Test __len__() method."""

    def test_len_zero(self) -> None:
        """Length of size=0 vector."""
        bv = BitVec(0)
        assert len(bv) == 0

    def test_len_non_zero(self) -> None:
        """Length of non-zero vector."""
        bv = BitVec(8)
        assert len(bv) == 8

    def test_len_non_aligned(self) -> None:
        """Length of non-byte-aligned vector."""
        bv = BitVec(13)
        assert len(bv) == 13

    def test_len_large(self) -> None:
        """Length of large vector."""
        bv = BitVec(10000)
        assert len(bv) == 10000

    def test_len_unchanged_after_operations(self) -> None:
        """Length is unchanged after set/clear operations."""
        bv = BitVec(8)
        assert len(bv) == 8
        bv.set(0)
        assert len(bv) == 8
        bv.set(7)
        assert len(bv) == 8
        bv.clear(0)
        assert len(bv) == 8


class TestIter:
    """Test __iter__() method (yields set bit indices)."""

    def test_iter_empty(self) -> None:
        """Iterate over empty vector."""
        bv = BitVec(8)
        indices = list(bv)
        assert indices == []

    def test_iter_single_bit(self) -> None:
        """Iterate over single set bit."""
        bv = BitVec(8)
        bv.set(3)
        indices = list(bv)
        assert indices == [3]

    def test_iter_multiple_bits(self) -> None:
        """Iterate over multiple set bits."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(2)
        bv.set(4)
        indices = list(bv)
        assert indices == [0, 2, 4]

    def test_iter_all_bits(self) -> None:
        """Iterate over all set bits."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        indices = list(bv)
        assert indices == list(range(8))

    def test_iter_in_order(self) -> None:
        """Iteration order is ascending."""
        bv = BitVec(10)
        # Set in reverse order
        for i in range(9, -1, -1):
            bv.set(i)
        indices = list(bv)
        assert indices == sorted(indices)

    def test_iter_large_vector(self) -> None:
        """Iterate over large vector."""
        bv = BitVec(1000)
        for i in range(0, 1000, 3):
            bv.set(i)
        indices = list(bv)
        assert len(indices) == 334
        assert indices == list(range(0, 1000, 3))

    def test_iter_non_aligned_size(self) -> None:
        """Iterate over non-byte-aligned vector."""
        bv = BitVec(13)
        for i in range(13):
            if i % 2 == 0:
                bv.set(i)
        indices = list(bv)
        assert indices == list(range(0, 13, 2))

    def test_iter_twice(self) -> None:
        """Can iterate multiple times."""
        bv = BitVec(8)
        bv.set(1)
        bv.set(3)
        result1 = list(bv)
        result2 = list(bv)
        assert result1 == result2


class TestBool:
    """Test __bool__() conversion."""

    def test_bool_empty(self) -> None:
        """Empty vector is falsy."""
        bv = BitVec(8)
        assert bool(bv) is False

    def test_bool_with_bits(self) -> None:
        """Vector with bits is truthy."""
        bv = BitVec(8)
        bv.set(3)
        assert bool(bv) is True

    def test_bool_zero_size(self) -> None:
        """Zero-size vector is falsy."""
        bv = BitVec(0)
        assert bool(bv) is False

    def test_bool_in_if_statement(self) -> None:
        """__bool__ works in if statements."""
        bv = BitVec(8)
        if bv:
            assert False, "Should be falsy"
        bv.set(0)
        if not bv:
            assert False, "Should be truthy"


class TestEquality:
    """Test __eq__() method."""

    def test_eq_same_content(self) -> None:
        """Equal vectors with same content."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(3)
        bv2.set(3)
        assert bv1 == bv2

    def test_eq_empty_vectors(self) -> None:
        """Empty vectors are equal."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        assert bv1 == bv2

    def test_eq_different_content(self) -> None:
        """Vectors with different content are not equal."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(3)
        bv2.set(4)
        assert bv1 != bv2

    def test_eq_different_sizes(self) -> None:
        """Vectors of different sizes are not equal."""
        bv1 = BitVec(8)
        bv2 = BitVec(16)
        assert bv1 != bv2

    def test_eq_self(self) -> None:
        """Vector equals itself."""
        bv = BitVec(8)
        bv.set(3)
        assert bv == bv

    def test_eq_with_non_bitvec(self) -> None:
        """Comparison with non-BitVec returns False."""
        bv = BitVec(8)
        assert bv != "hello"
        assert bv != 42
        assert bv != [0, 1, 1, 0]

    def test_eq_reflexive(self) -> None:
        """Equality is reflexive (a == a)."""
        bv = BitVec(10)
        for i in range(0, 10, 2):
            bv.set(i)
        assert bv == bv

    def test_eq_symmetric(self) -> None:
        """Equality is symmetric (a == b implies b == a)."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        for i in range(0, 8, 2):
            bv1.set(i)
            bv2.set(i)
        assert bv1 == bv2
        assert bv2 == bv1

    def test_eq_transitive(self) -> None:
        """Equality is transitive (a == b && b == c implies a == c)."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv3 = BitVec(8)
        bv1.set(5)
        bv2.set(5)
        bv3.set(5)
        assert bv1 == bv2
        assert bv2 == bv3
        assert bv1 == bv3


class TestRepr:
    """Test __repr__() method."""

    def test_repr_empty(self) -> None:
        """Repr of empty vector."""
        bv = BitVec(8)
        r = repr(bv)
        assert isinstance(r, str)
        assert "BitVec" in r or "bitvec" in r.lower()
        assert "8" in r

    def test_repr_with_bits(self) -> None:
        """Repr of vector with bits."""
        bv = BitVec(8)
        bv.set(3)
        r = repr(bv)
        assert isinstance(r, str)

    def test_repr_is_informative(self) -> None:
        """Repr contains useful information."""
        bv = BitVec(16)
        bv.set(0)
        bv.set(15)
        r = repr(bv)
        # Should mention size
        assert "16" in r

    def test_repr_zero_size(self) -> None:
        """Repr of size=0 vector."""
        bv = BitVec(0)
        r = repr(bv)
        assert isinstance(r, str)


class TestAny:
    """Test any() method."""

    def test_any_empty(self) -> None:
        """any() of empty vector."""
        bv = BitVec(8)
        assert bv.any() is False

    def test_any_single_bit(self) -> None:
        """any() with single set bit."""
        bv = BitVec(8)
        bv.set(3)
        assert bv.any() is True

    def test_any_multiple_bits(self) -> None:
        """any() with multiple set bits."""
        bv = BitVec(8)
        bv.set(1)
        bv.set(5)
        assert bv.any() is True

    def test_any_zero_size(self) -> None:
        """any() of zero-size vector."""
        bv = BitVec(0)
        assert bv.any() is False


class TestAll:
    """Test all() method."""

    def test_all_empty(self) -> None:
        """all() of empty vector (all 0 bits)."""
        bv = BitVec(8)
        assert bv.all() is False

    def test_all_single_bit_set(self) -> None:
        """all() with single bit set (not all set)."""
        bv = BitVec(8)
        bv.set(3)
        assert bv.all() is False

    def test_all_all_bits_set(self) -> None:
        """all() with all bits set."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        assert bv.all() is True

    def test_all_zero_size(self) -> None:
        """all() of zero-size vector (vacuous truth)."""
        bv = BitVec(0)
        assert bv.all() is True

    def test_all_non_aligned(self) -> None:
        """all() with non-byte-aligned size."""
        bv = BitVec(13)
        for i in range(13):
            bv.set(i)
        assert bv.all() is True
        bv.clear(5)
        assert bv.all() is False


class TestNone:
    """Test none() method."""

    def test_none_empty(self) -> None:
        """none() of empty vector (no bits set)."""
        bv = BitVec(8)
        assert bv.none() is True

    def test_none_single_bit(self) -> None:
        """none() with single set bit."""
        bv = BitVec(8)
        bv.set(3)
        assert bv.none() is False

    def test_none_multiple_bits(self) -> None:
        """none() with multiple set bits."""
        bv = BitVec(8)
        bv.set(1)
        bv.set(5)
        assert bv.none() is False

    def test_none_zero_size(self) -> None:
        """none() of zero-size vector."""
        bv = BitVec(0)
        assert bv.none() is True

    def test_none_all_set(self) -> None:
        """none() with all bits set."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        assert bv.none() is False
