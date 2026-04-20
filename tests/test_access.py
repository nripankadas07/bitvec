"""Tests for BitVec bit access and manipulation."""
import pytest
from bitvec import BitVec, BitVecError


class TestGet:
    """Test get() method."""

    def test_get_zero_bit(self) -> None:
        """Get unset bit returns False."""
        bv = BitVec(8)
        assert bv.get(0) is False

    def test_get_after_set(self) -> None:
        """Get after set returns True."""
        bv = BitVec(8)
        bv.set(3)
        assert bv.get(3) is True

    def test_get_boundary(self) -> None:
        """Get at size boundary."""
        bv = BitVec(8)
        bv.set(7)
        assert bv.get(7) is True
        assert bv.get(0) is False

    def test_get_out_of_range_positive(self) -> None:
        """Get with index >= size raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv.get(8)

    def test_get_out_of_range_negative(self) -> None:
        """Get with negative index raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv.get(-1)

    def test_get_non_integer(self) -> None:
        """Get with non-integer index raises error."""
        bv = BitVec(8)
        with pytest.raises((TypeError, BitVecError)):
            bv.get("0")  # type: ignore


class TestSet:
    """Test set() method."""

    def test_set_single_bit(self) -> None:
        """Set a single bit."""
        bv = BitVec(8)
        bv.set(0)
        assert bv.get(0) is True
        assert bv.count() == 1

    def test_set_multiple_bits(self) -> None:
        """Set multiple bits independently."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(4)
        bv.set(7)
        assert bv.count() == 3
        assert bv.get(0) is True
        assert bv.get(4) is True
        assert bv.get(7) is True

    def test_set_already_set(self) -> None:
        """Setting already-set bit is idempotent."""
        bv = BitVec(8)
        bv.set(3)
        bv.set(3)
        assert bv.count() == 1
        assert bv.get(3) is True

    def test_set_out_of_range(self) -> None:
        """Set with index >= size raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv.set(8)

    def test_set_on_large_vector(self) -> None:
        """Set on large vector."""
        bv = BitVec(10000)
        bv.set(9999)
        assert bv.get(9999) is True
        assert bv.count() == 1


class TestClear:
    """Test clear() method."""

    def test_clear_set_bit(self) -> None:
        """Clear a set bit."""
        bv = BitVec(8)
        bv.set(3)
        bv.clear(3)
        assert bv.get(3) is False
        assert bv.count() == 0

    def test_clear_unset_bit(self) -> None:
        """Clearing unset bit is idempotent."""
        bv = BitVec(8)
        bv.clear(3)
        assert bv.get(3) is False
        assert bv.count() == 0

    def test_clear_multiple_bits(self) -> None:
        """Clear multiple bits independently."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(4)
        bv.set(7)
        bv.clear(0)
        bv.clear(4)
        assert bv.count() == 1
        assert bv.get(7) is True

    def test_clear_out_of_range(self) -> None:
        """Clear with index >= size raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv.clear(8)


class TestToggle:
    """Test toggle() method."""

    def test_toggle_unset_bit(self) -> None:
        """Toggle unset bit sets it."""
        bv = BitVec(8)
        bv.toggle(3)
        assert bv.get(3) is True

    def test_toggle_set_bit(self) -> None:
        """Toggle set bit clears it."""
        bv = BitVec(8)
        bv.set(3)
        bv.toggle(3)
        assert bv.get(3) is False

    def test_toggle_twice_idempotent(self) -> None:
        """Toggling twice returns to original state."""
        bv = BitVec(8)
        bv.toggle(5)
        bv.toggle(5)
        assert bv.get(5) is False

    def test_toggle_out_of_range(self) -> None:
        """Toggle with index >= size raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv.toggle(8)


class TestIndexing:
    """Test __getitem__ and __setitem__ with single indices."""

    def test_getitem_unset(self) -> None:
        """Indexing unset bit returns False."""
        bv = BitVec(8)
        assert bv[3] is False

    def test_setitem_true(self) -> None:
        """Setting index to True sets the bit."""
        bv = BitVec(8)
        bv[3] = True
        assert bv[3] is True
        assert bv.count() == 1

    def test_setitem_false(self) -> None:
        """Setting index to False clears the bit."""
        bv = BitVec(8)
        bv.set(3)
        bv[3] = False
        assert bv[3] is False
        assert bv.count() == 0

    def test_getitem_out_of_range(self) -> None:
        """Indexing out of range raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            _ = bv[8]

    def test_setitem_out_of_range(self) -> None:
        """Setting out of range raises error."""
        bv = BitVec(8)
        with pytest.raises((IndexError, BitVecError)):
            bv[8] = True


class TestSlicing:
    """Test __getitem__ and __setitem__ with slices."""

    def test_getitem_slice_all(self) -> None:
        """Slice all bits."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(7)
        result = bv[:]
        assert isinstance(result, list)
        assert len(result) == 8
        assert result[0] is True
        assert result[7] is True
        assert result[1] is False

    def test_getitem_slice_range(self) -> None:
        """Slice a range of bits."""
        bv = BitVec(10)
        bv.set(3)
        bv.set(4)
        bv.set(5)
        result = bv[2:6]
        assert len(result) == 4
        assert result[1] is True
        assert result[2] is True
        assert result[3] is True

    def test_getitem_slice_with_step(self) -> None:
        """Slice with step parameter."""
        bv = BitVec(10)
        for i in range(10):
            bv.set(i)
        result = bv[::2]
        assert len(result) == 5
        assert all(result)

    def test_getitem_negative_indices(self) -> None:
        """Slice with negative indices."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[-4:]
        assert len(result) == 4
        assert all(result)

    def test_setitem_slice_all_true(self) -> None:
        """Set all bits via slice."""
        bv = BitVec(8)
        bv[:] = True
        assert bv.count() == 8

    def test_setitem_slice_all_false(self) -> None:
        """Clear all bits via slice."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        bv[:] = False
        assert bv.count() == 0

    def test_setitem_slice_range(self) -> None:
        """Set a range of bits via slice."""
        bv = BitVec(10)
        bv[2:5] = True
        assert bv.count() == 3
        assert bv.get(2) is True
        assert bv.get(3) is True
        assert bv.get(4) is True
        assert bv.get(5) is False

    def test_setitem_slice_with_list(self) -> None:
        """Set slice with list of values."""
        bv = BitVec(8)
        bv[2:5] = [True, False, True]
        assert bv[2] is True
        assert bv[3] is False
        assert bv[4] is True


class TestCount:
    """Test count() (popcount) method."""

    def test_count_empty(self) -> None:
        """Count of empty vector is 0."""
        bv = BitVec(8)
        assert bv.count() == 0

    def test_count_single_bit(self) -> None:
        """Count of single set bit."""
        bv = BitVec(8)
        bv.set(0)
        assert bv.count() == 1

    def test_count_multiple_bits(self) -> None:
        """Count of multiple set bits."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(2)
        bv.set(4)
        assert bv.count() == 3

    def test_count_all_set(self) -> None:
        """Count when all bits are set."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        assert bv.count() == 8

    def test_count_large_vector(self) -> None:
        """Count on large vector."""
        bv = BitVec(1000)
        for i in range(0, 1000, 2):
            bv.set(i)
        assert bv.count() == 500


class TestAccessEdgeCases:
    """Edge cases for bit access."""

    def test_operations_on_zero_size(self) -> None:
        """Operations on zero-size vector."""
        bv = BitVec(0)
        assert bv.count() == 0
        with pytest.raises((IndexError, BitVecError)):
            bv.get(0)

    def test_operations_on_single_bit_vector(self) -> None:
        """Operations on size=1 vector."""
        bv = BitVec(1)
        assert bv.get(0) is False
        bv.set(0)
        assert bv.get(0) is True
        bv.clear(0)
        assert bv.get(0) is False
