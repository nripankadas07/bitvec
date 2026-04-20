"""BitVec: compact bit vector implementation."""
from typing import Iterable, Iterator, overload, Union, List
from bitvec.errors import BitVecError


class BitVec:
    """Compact bit vector with set operations and slicing.

    A zero-initialized bit vector supporting efficient bit access,
    bitwise operations, and iteration over set bit indices.
    """

    __slots__ = ('_data', '_size')

    def __init__(self, size: int) -> None:
        """Create a zero-initialized bit vector.

        Args:
            size: Number of bits (must be >= 0)

        Raises:
            ValueError: If size < 0
        """
        if size < 0:
            raise ValueError(f"size must be non-negative, got {size}")
        self._size = size
        byte_count = (size + 7) // 8
        self._data = bytearray(byte_count)

    @classmethod
    def from_bytes(cls, data: bytes, size: int) -> 'BitVec':
        """Create from raw bytes.

        Args:
            data: Byte data
            size: Number of bits to use

        Returns:
            BitVec with bits from data

        Raises:
            ValueError: If data is too small for size
        """
        required_bytes = (size + 7) // 8
        if len(data) < required_bytes:
            raise ValueError(
                f"need {required_bytes} bytes for size {size}, got {len(data)}"
            )
        bv = cls(size)
        for i in range(required_bytes):
            bv._data[i] = data[i]
        # Mask off extra bits beyond size in the last byte
        if size % 8 != 0:
            last_byte_idx = required_bytes - 1
            mask = (1 << (size % 8)) - 1
            bv._data[last_byte_idx] &= mask
        return bv

    @classmethod
    def from_iterable(cls, indices: Iterable[int], size: int) -> 'BitVec':
        """Create from iterable of bit indices.

        Args:
            indices: Iterable of indices to set
            size: Size of vector

        Returns:
            BitVec with specified bits set

        Raises:
            IndexError: If any index is out of range
        """
        bv = cls(size)
        for idx in indices:
            if not isinstance(idx, int):
                raise TypeError(f"index must be int, got {type(idx).__name__}")
            if idx < 0 or idx >= size:
                raise IndexError(f"index {idx} out of range for size {size}")
            bv.set(idx)
        return bv

    def get(self, index: int) -> bool:
        """Get bit at index.

        Args:
            index: Bit index

        Returns:
            True if bit is set, False otherwise

        Raises:
            IndexError: If index out of range
            TypeError: If index is not an integer
        """
        if not isinstance(index, int):
            raise TypeError(f"index must be int, got {type(index).__name__}")
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")
        byte_idx = index // 8
        bit_idx = index % 8
        return bool((self._data[byte_idx] >> bit_idx) & 1)

    def set(self, index: int) -> None:
        """Set bit at index to 1.

        Args:
            index: Bit index

        Raises:
            IndexError: If index out of range
            TypeError: If index is not an integer
        """
        if not isinstance(index, int):
            raise TypeError(f"index must be int, got {type(index).__name__}")
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")
        byte_idx = index // 8
        bit_idx = index % 8
        self._data[byte_idx] |= (1 << bit_idx)

    def clear(self, index: int) -> None:
        """Clear bit at index (set to 0).

        Args:
            index: Bit index

        Raises:
            IndexError: If index out of range
            TypeError: If index is not an integer
        """
        if not isinstance(index, int):
            raise TypeError(f"index must be int, got {type(index).__name__}")
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")
        byte_idx = index // 8
        bit_idx = index % 8
        self._data[byte_idx] &= ~(1 << bit_idx)

    def toggle(self, index: int) -> None:
        """Toggle bit at index (flip 0->1 or 1->0).

        Args:
            index: Bit index

        Raises:
            IndexError: If index out of range
            TypeError: If index is not an integer
        """
        if not isinstance(index, int):
            raise TypeError(f"index must be int, got {type(index).__name__}")
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")
        byte_idx = index // 8
        bit_idx = index % 8
        self._data[byte_idx] ^= (1 << bit_idx)

    def count(self) -> int:
        """Count set bits (popcount).

        Returns:
            Number of bits set to 1
        """
        total = 0
        for byte_val in self._data:
            total += bin(byte_val).count('1')
        return total

    def __len__(self) -> int:
        """Return size of vector."""
        return self._size

    @overload
    def __getitem__(self, index: int) -> bool:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[bool]:
        ...

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[bool, List[bool]]:
        """Get bit(s) by index or slice.

        Args:
            index: Integer index or slice

        Returns:
            Boolean for single index, list of booleans for slice

        Raises:
            IndexError: If index out of range
            TypeError: If index is not int or slice
        """
        if isinstance(index, int):
            return self.get(index)
        elif isinstance(index, slice):
            start, stop, step = index.indices(self._size)
            result = []
            for i in range(start, stop, step):
                result.append(self.get(i))
            return result
        else:
            raise TypeError(
                f"indices must be integers or slices, not {type(index).__name__}"
            )

    @overload
    def __setitem__(self, index: int, value: bool) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Union[bool, List[bool]]) -> None:
        ...

    def __setitem__(
        self, index: Union[int, slice], value: Union[bool, List[bool]]
    ) -> None:
        """Set bit(s) by index or slice.

        Args:
            index: Integer index or slice
            value: Boolean or list of booleans for slice

        Raises:
            IndexError: If index out of range
            ValueError: If slice and value size mismatch
        """
        if isinstance(index, int):
            self._setitem_single(index, value)
        elif isinstance(index, slice):
            self._setitem_slice(index, value)
        else:
            raise TypeError(
                f"indices must be integers or slices, not {type(index).__name__}"
            )

    def _setitem_single(
        self, index: int, value: Union[bool, List[bool]]
    ) -> None:
        """Set single bit at index.

        Raises:
            TypeError: If value is not bool
        """
        if isinstance(value, bool):
            if value:
                self.set(index)
            else:
                self.clear(index)
        else:
            raise TypeError(f"expected bool, got {type(value).__name__}")

    def _setitem_slice(
        self, slc: slice, value: Union[bool, List[bool]]
    ) -> None:
        """Set multiple bits via slice."""
        start, stop, step = slc.indices(self._size)
        indices = list(range(start, stop, step))
        if isinstance(value, bool):
            for i in indices:
                (self.set(i) if value else self.clear(i))
        elif isinstance(value, (list, tuple)):
            if len(value) != len(indices):
                raise ValueError(
                    f"slice: expected {len(indices)} values, got {len(value)}"
                )
            for i, v in zip(indices, value):
                (self.set(i) if v else self.clear(i))
        else:
            raise TypeError(f"expected bool or iterable, got {type(value)}")

    def __and__(self, other: 'BitVec') -> 'BitVec':
        """Bitwise AND.

        Args:
            other: BitVec to AND with

        Returns:
            New BitVec with AND result

        Raises:
            ValueError: If sizes differ
        """
        if self._size != other._size:
            raise ValueError(
                f"cannot AND vectors of different sizes: {self._size} vs "
                f"{other._size}"
            )
        result = BitVec(self._size)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] & other._data[i]
        return result

    def __or__(self, other: 'BitVec') -> 'BitVec':
        """Bitwise OR.

        Args:
            other: BitVec to OR with

        Returns:
            New BitVec with OR result

        Raises:
            ValueError: If sizes differ
        """
        if self._size != other._size:
            raise ValueError(
                f"cannot OR vectors of different sizes: {self._size} vs "
                f"{other._size}"
            )
        result = BitVec(self._size)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] | other._data[i]
        return result

    def __xor__(self, other: 'BitVec') -> 'BitVec':
        """Bitwise XOR.

        Args:
            other: BitVec to XOR with

        Returns:
            New BitVec with XOR result

        Raises:
            ValueError: If sizes differ
        """
        if self._size != other._size:
            raise ValueError(
                f"cannot XOR vectors of different sizes: {self._size} vs "
                f"{other._size}"
            )
        result = BitVec(self._size)
        for i in range(len(self._data)):
            result._data[i] = self._data[i] ^ other._data[i]
        return result

    def __invert__(self) -> 'BitVec':
        """Bitwise NOT (invert all bits).

        Returns:
            New BitVec with inverted bits
        """
        result = BitVec(self._size)
        for i in range(len(self._data)):
            result._data[i] = ~self._data[i] & 0xFF

        if self._size % 8 != 0:
            last_byte_idx = len(self._data) - 1
            mask = (1 << (self._size % 8)) - 1
            result._data[last_byte_idx] &= mask

        return result

    def __iter__(self) -> Iterator[int]:
        """Iterate over set bit indices in ascending order.

        Yields:
            Indices of bits that are set to 1
        """
        for i in range(self._size):
            if self.get(i):
                yield i

    def __eq__(self, other: object) -> bool:
        """Check equality with another BitVec.

        Args:
            other: Object to compare with

        Returns:
            True if same size and same bits, False otherwise
        """
        if not isinstance(other, BitVec):
            return False
        if self._size != other._size:
            return False
        return self._data == other._data

    def __bool__(self) -> bool:
        """Check if any bit is set.

        Returns:
            True if any bit is set, False if all unset
        """
        return self.count() > 0

    def __repr__(self) -> str:
        """Return string representation.

        Returns:
            String like "BitVec(size=8, count=3)"
        """
        return f"BitVec(size={self._size}, count={self.count()})"

    def to_bytes(self) -> bytes:
        """Convert to bytes.

        Returns:
            Bytes representation of bit vector
        """
        return bytes(self._data)

    def any(self) -> bool:
        """Check if any bit is set.

        Returns:
            True if at least one bit is set
        """
        return self.count() > 0

    def all(self) -> bool:
        """Check if all bits are set.

        Returns:
            True if all bits are 1, False otherwise.
            For zero-size vector, returns True (vacuous truth).
        """
        if self._size == 0:
            return True
        return self.count() == self._size

    def none(self) -> bool:
        """Check if no bits are set.

        Returns:
            True if all bits are 0
        """
        return self.count() == 0
