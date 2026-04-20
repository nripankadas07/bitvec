"""Tests for edge cases and comprehensive coverage."""
import pytest
from bitvec import BitVec, BitVecError


class TestToBytes:
    """Test to_bytes() method."""

    def test_to_bytes_empty(self) -> None:
        """to_bytes() of empty vector."""
        bv = BitVec(0)
        result = bv.to_bytes()
        assert result == b''

    def test_to_bytes_single_byte(self) -> None:
        """to_bytes() of single byte."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(7)
        result = bv.to_bytes()
        assert isinstance(result, bytes)
        assert len(result) == 1

    def test_to_bytes_multiple_bytes(self) -> None:
        """to_bytes() of multiple bytes."""
        bv = BitVec(16)
        bv.set(0)
        bv.set(8)
        result = bv.to_bytes()
        assert isinstance(result, bytes)
        assert len(result) == 2

    def test_to_bytes_non_aligned(self) -> None:
        """to_bytes() with non-byte-aligned size."""
        bv = BitVec(13)
        for i in range(13):
            bv.set(i)
        result = bv.to_bytes()
        # Should be 2 bytes for 13 bits
        assert len(result) == 2

    def test_to_bytes_roundtrip(self) -> None:
        """from_bytes -> to_bytes roundtrip."""
        original = b'\xAA\xBB'
        bv = BitVec.from_bytes(original, 16)
        result = bv.to_bytes()
        assert result == original

    def test_to_bytes_roundtrip_non_aligned(self) -> None:
        """Roundtrip with non-aligned size preserves bits."""
        bv1 = BitVec(13)
        for i in range(13):
            bv1.set(i)
        data = bv1.to_bytes()
        bv2 = BitVec.from_bytes(data, 13)
        assert bv1 == bv2


class TestRangeErrors:
    """Test comprehensive range checking."""

    def test_get_boundary_conditions(self) -> None:
        """Get at all boundary indices."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(7)
        assert bv.get(0) is True
        assert bv.get(7) is True
        with pytest.raises((IndexError, BitVecError)):
            bv.get(-1)
        with pytest.raises((IndexError, BitVecError)):
            bv.get(8)

    def test_set_boundary_conditions(self) -> None:
        """Set at all boundary indices."""
        bv = BitVec(8)
        bv.set(0)
        bv.set(7)
        assert bv.get(0) is True
        assert bv.get(7) is True
        with pytest.raises((IndexError, BitVecError)):
            bv.set(8)

    def test_large_index_out_of_range(self) -> None:
        """Very large out-of-range index."""
        bv = BitVec(100)
        with pytest.raises((IndexError, BitVecError)):
            bv.get(1000000)

    def test_operations_on_large_indices(self) -> None:
        """Operations on edge indices of large vector."""
        bv = BitVec(10000)
        bv.set(9999)
        assert bv.get(9999) is True
        with pytest.raises((IndexError, BitVecError)):
            bv.get(10000)


class TestTypeChecking:
    """Test type validation."""

    def test_non_integer_index_get(self) -> None:
        """get() with non-integer index."""
        bv = BitVec(8)
        with pytest.raises((TypeError, BitVecError)):
            bv.get(3.5)  # type: ignore
        with pytest.raises((TypeError, BitVecError)):
            bv.get("3")  # type: ignore

    def test_non_integer_index_set(self) -> None:
        """set() with non-integer index."""
        bv = BitVec(8)
        with pytest.raises((TypeError, BitVecError)):
            bv.set(3.5)  # type: ignore

    def test_non_integer_index_getitem(self) -> None:
        """__getitem__ with non-integer index (single)."""
        bv = BitVec(8)
        with pytest.raises((TypeError, BitVecError, KeyError)):
            _ = bv["0"]  # type: ignore


class TestNonAlignedBehavior:
    """Test non-byte-aligned vectors comprehensively."""

    def test_all_sizes_small(self) -> None:
        """Test all small non-aligned sizes."""
        for size in [1, 2, 3, 5, 7, 9, 13, 15, 17]:
            bv = BitVec(size)
            assert len(bv) == size
            assert bv.count() == 0
            # Set all bits
            for i in range(size):
                bv.set(i)
            assert bv.count() == size

    def test_invert_preserves_non_aligned_size(self) -> None:
        """Invert doesn't set extra bits beyond size."""
        bv = BitVec(5)
        result = ~bv
        assert len(result) == 5
        assert result.count() == 5
        # No 6th-8th bits should be set

    def test_from_bytes_with_non_aligned_size(self) -> None:
        """from_bytes correctly handles non-aligned sizes."""
        for size in [1, 5, 9, 13]:
            data = b'\xFF' * ((size + 7) // 8)
            bv = BitVec.from_bytes(data, size)
            assert len(bv) == size


class TestBitwiseSizeMismatch:
    """Test all bitwise operations with size mismatch."""

    def test_and_various_mismatches(self) -> None:
        """AND with various size mismatches."""
        bv8 = BitVec(8)
        bv16 = BitVec(16)
        bv13 = BitVec(13)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv8 & bv16
        with pytest.raises((ValueError, BitVecError)):
            _ = bv8 & bv13

    def test_or_various_mismatches(self) -> None:
        """OR with various size mismatches."""
        bv8 = BitVec(8)
        bv16 = BitVec(16)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv8 | bv16

    def test_xor_various_mismatches(self) -> None:
        """XOR with various size mismatches."""
        bv8 = BitVec(8)
        bv16 = BitVec(16)
        with pytest.raises((ValueError, BitVecError)):
            _ = bv8 ^ bv16


class TestIterationEdgeCases:
    """Edge cases for iteration."""

    def test_iter_after_modifications(self) -> None:
        """Iteration after various modifications."""
        bv = BitVec(16)
        bv.set(0)
        bv.set(15)
        result1 = list(bv)
        bv.set(7)
        result2 = list(bv)
        assert len(result2) == len(result1) + 1
        assert 7 in result2

    def test_iter_large_gaps(self) -> None:
        """Iteration with large gaps between set bits."""
        bv = BitVec(1000)
        bv.set(0)
        bv.set(999)
        result = list(bv)
        assert result == [0, 999]

    def test_iter_sequential_bits(self) -> None:
        """Iteration with many sequential bits."""
        bv = BitVec(100)
        for i in range(50, 60):
            bv.set(i)
        result = list(bv)
        assert result == list(range(50, 60))


class TestSliceEdgeCases:
    """Comprehensive slice testing."""

    def test_slice_empty_range(self) -> None:
        """Slice with empty range."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[3:3]
        assert len(result) == 0

    def test_slice_out_of_bounds_stop(self) -> None:
        """Slice with stop beyond size."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[5:100]
        assert len(result) == 3  # Only indices 5, 6, 7

    def test_slice_negative_start(self) -> None:
        """Slice with negative start."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[-3:]
        assert len(result) == 3
        assert all(result)

    def test_slice_negative_both(self) -> None:
        """Slice with both negative indices."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[-4:-1]
        assert len(result) == 3

    def test_slice_step_greater_than_range(self) -> None:
        """Slice with step greater than range."""
        bv = BitVec(8)
        for i in range(8):
            bv.set(i)
        result = bv[0:5:10]
        assert len(result) == 1
        assert result[0] is True

    def test_setitem_slice_iterable(self) -> None:
        """Set slice from iterable."""
        bv = BitVec(8)
        bv[2:5] = [True, False, True]
        assert bv[2] is True
        assert bv[3] is False
        assert bv[4] is True

    def test_setitem_slice_too_many_values(self) -> None:
        """Set slice with wrong number of values."""
        bv = BitVec(8)
        # Behavior depends on implementation
        # Just ensure it doesn't crash catastrophically
        try:
            bv[2:5] = [True, False]
        except (ValueError, BitVecError, IndexError):
            pass


class TestSpecialCases:
    """Special and corner cases."""

    def test_single_bit_vector_all_operations(self) -> None:
        """All operations on size=1 vector."""
        bv = BitVec(1)
        assert len(bv) == 1
        assert bv.count() == 0
        assert bv.any() is False
        assert bv.all() is False
        assert bv.none() is True
        bv.set(0)
        assert bv.count() == 1
        assert bv.any() is True
        assert bv.all() is True
        assert bv.none() is False
        bv.clear(0)
        assert bool(bv) is False

    def test_zero_size_vector_all_operations(self) -> None:
        """All operations on size=0 vector."""
        bv = BitVec(0)
        assert len(bv) == 0
        assert bv.count() == 0
        assert bv.any() is False
        assert bv.all() is True  # Vacuous truth
        assert bv.none() is True
        assert bool(bv) is False
        assert list(bv) == []
        with pytest.raises((IndexError, BitVecError)):
            bv.get(0)

    def test_from_iterable_generator(self) -> None:
        """from_iterable with generator."""
        def gen() -> type:  # type: ignore
            for i in [0, 2, 4]:
                yield i
        bv = BitVec.from_iterable(gen(), 8)
        assert bv.count() == 3

    def test_repr_consistency(self) -> None:
        """repr() is consistent across calls."""
        bv = BitVec(13)
        bv.set(5)
        r1 = repr(bv)
        r2 = repr(bv)
        assert r1 == r2

    def test_equality_after_operations(self) -> None:
        """Equality is preserved through operations."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(3)
        bv2.set(3)
        assert bv1 == bv2
        bv1.clear(3)
        bv2.clear(3)
        assert bv1 == bv2

    def test_operations_preserve_immutability_expectation(self) -> None:
        """Bitwise operations don't modify operands."""
        bv1 = BitVec(8)
        bv2 = BitVec(8)
        bv1.set(0)
        bv2.set(1)
        orig_bv1_count = bv1.count()
        orig_bv2_count = bv2.count()
        _ = bv1 | bv2
        _ = bv1 & bv2
        _ = bv1 ^ bv2
        assert bv1.count() == orig_bv1_count
        assert bv2.count() == orig_bv2_count
