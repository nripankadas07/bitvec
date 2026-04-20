# BitVec

Compact bit vector with set operations, slicing, and efficient storage for Python developers.

## Installation

From source:
```bash
pip install -e /tmp/bitvec
```

Or from PyPI (once published):
```bash
pip install bitvec
```

## Quick Start

```python
from bitvec import BitVec

# Create a bit vector
bv = BitVec(8)
bv.set(0)
bv.set(3)
bv.set(7)

# Check bits
print(bv.get(3))  # True
print(bv.count())  # 3

# Bitwise operations
bv2 = BitVec(8)
bv2.set(2)
bv2.set(3)
result = bv & bv2  # AND operation
print(result.count())  # 1 (only bit 3 is in both)

# Iterate over set bits
for idx in bv:
    print(idx)  # 0, 3, 7

# Slicing
bits = bv[2:6]  # Get bits 2-5
bv[2:5] = True  # Set bits 2-4

# Convert to bytes
data = bv.to_bytes()
bv_restored = BitVec.from_bytes(data, len(bv))
```

## Features

- **Efficient storage**: Uses one byte per 8 bits
- **Full bitwise operations**: AND, OR, XOR, NOT
- **Flexible creation**: From size, bytes, or iterable of indices
- **Slicing support**: Get/set ranges of bits with Python slicing syntax
- **Iterator protocol**: Iterate over set bit indices
- **Type-safe**: Full type hints for static analysis
- **Tested**: Comprehensive test coverage (80+ tests)

## API Reference

### Construction

```python
BitVec(size: int) -> BitVec
```
Create a zero-initialized bit vector of given size.

```python
BitVec.from_bytes(data: bytes, size: int) -> BitVec
```
Create a bit vector from raw bytes. Raises `ValueError` if data is too small.

```python
BitVec.from_iterable(indices: Iterable[int], size: int) -> BitVec
```
Create a bit vector with specified bit indices set. Raises `IndexError` if any index is out of range.

### Bit Access

```python
get(index: int) -> bool
```
Get the value of bit at index (True=1, False=0).

```python
set(index: int) -> None
```
Set bit at index to 1.

```python
clear(index: int) -> None
```
Clear bit at index (set to 0).

```python
toggle(index: int) -> None
```
Toggle bit at index (flip 0→1 or 1→0).

### Indexing & Slicing

```python
bv[index: int] -> bool
bv[index: int] = value: bool
```
Get/set single bits using bracket notation.

```python
bv[start:stop:step] -> List[bool]
bv[start:stop:step] = value: Union[bool, List[bool]]
```
Get/set ranges of bits with full Python slice support.

### Bitwise Operations

```python
bv1 & bv2 -> BitVec  # AND
bv1 | bv2 -> BitVec  # OR
bv1 ^ bv2 -> BitVec  # XOR
~bv -> BitVec         # NOT (invert)
```

All bitwise operations raise `ValueError` if vector sizes differ (except NOT).

### Query & Analysis

```python
count() -> int
```
Return number of set bits (popcount).

```python
any() -> bool
```
Return True if any bit is set.

```python
all() -> bool
```
Return True if all bits are set (vacuous truth for empty vectors).

```python
none() -> bool
```
Return True if no bits are set.

### Conversion & Iteration

```python
__len__() -> int
```
Return the size of the vector.

```python
__iter__() -> Iterator[int]
```
Iterate over indices of set bits in ascending order.

```python
to_bytes() -> bytes
```
Convert to bytes representation.

```python
__bool__() -> bool
```
Return True if any bit is set (same as `any()`).

```python
__eq__(other: BitVec) -> bool
```
Check equality with another bit vector.

```python
__repr__() -> str
```
Return string representation like "BitVec(size=8, count=3)".

### Exception

```python
BitVecError
```
Raised for various BitVec errors (index out of range, type errors, size mismatches).

## Exceptions

- **IndexError / BitVecError**: Index out of range
- **TypeError / BitVecError**: Non-integer index or wrong value type
- **ValueError / BitVecError**: Size mismatch for bitwise operations or negative size

## Edge Cases Handled

- Empty bit vectors (size=0)
- Non-byte-aligned sizes (e.g., 13 bits)
- Very large vectors (10,000+ bits)
- All bitwise operations on different-sized vectors (raise error)
- Inverted non-aligned vectors (extra bits properly masked)
- Duplicate indices in from_iterable (idempotent)
- Slicing with negative indices and large steps

## Running Tests

```bash
cd /tmp/bitvec
python -m pytest tests/ -v
```

Test coverage:
- **test_construction.py**: 15 tests (creation from various sources)
- **test_access.py**: 18 tests (get, set, clear, toggle, indexing, slicing)
- **test_bitwise.py**: 19 tests (AND, OR, XOR, NOT operations)
- **test_iteration.py**: 20 tests (len, iter, bool, equality, any/all/none)
- **test_edges.py**: 25 tests (edge cases, roundtrips, type checking)

**Total: 97 tests, all passing**

## Performance Notes

- O(1) single-bit access
- O(n) popcount (where n = number of bytes)
- O(n) for bitwise operations (where n = number of bytes)
- O(k) for iteration (where k = number of set bits)
- O(1) memory per bit (1 bit per bit, rounded to byte)

## Implementation Notes

- Uses Python's `bytearray` for efficient storage
- Bits are stored in little-endian order within bytes
- Thread-safe for read-only operations, not thread-safe for concurrent modifications
- Pure Python implementation, no external dependencies

## License

MIT License - see LICENSE file for details.

## Author

Nripanka Das <nripankadas@gmail.com>
