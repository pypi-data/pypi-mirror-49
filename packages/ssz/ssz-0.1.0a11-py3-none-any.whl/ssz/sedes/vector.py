import itertools
from typing import (
    IO,
    Any,
    Iterable,
    Sequence,
    Tuple,
    TypeVar,
)

from eth_utils import (
    to_tuple,
)
from eth_utils.toolz import (
    sliding_window,
)

from ssz.exceptions import (
    SerializationError,
)
from ssz.sedes.base import (
    BaseSedes,
    BasicSedes,
    CompositeSedes,
    TSedes,
)
from ssz.utils import (
    merkleize,
    pack,
    read_exact,
    s_decode_offset,
)

TSerializableElement = TypeVar("TSerializable")
TDeserializedElement = TypeVar("TDeserialized")

TSedesPairs = Tuple[
    Tuple[BaseSedes[TSerializableElement, TDeserializedElement], TSerializableElement],
    ...
]


class Vector(CompositeSedes[Sequence[TSerializableElement], Tuple[TDeserializedElement, ...]]):
    def __init__(self,
                 element_sedes: TSedes,
                 length: int) -> None:
        self.element_sedes = element_sedes
        self.length = length

    def _get_item_sedes_pairs(self, value: Sequence[TSerializableElement]) -> TSedesPairs:
        return tuple(zip(value, itertools.repeat(self.element_sedes)))

    #
    # Size
    #
    @property
    def is_fixed_sized(self) -> bool:
        return self.length == 0 or self.element_sedes.is_fixed_sized

    def get_fixed_size(self) -> int:
        if not self.is_fixed_sized:
            raise ValueError("Tuple is not fixed size.")

        if self.length == 0:
            return 0
        else:
            return self.length * self.element_sedes.get_fixed_size()

    #
    # Serialization
    #
    def _validate_serializable(self, value: Any) -> None:
        if len(value) != self.length:
            raise SerializationError(
                f"Length mismatch.  Cannot serialize value with length "
                f"{len(value)} as {self.length}-tuple"
            )

    #
    # Deserialization
    #
    @to_tuple
    def _deserialize_stream(self, stream: IO[bytes]) -> Iterable[TDeserializedElement]:
        if self.element_sedes.is_fixed_sized:
            element_size = self.element_sedes.get_fixed_size()
            for _ in range(self.length):
                element_data = read_exact(element_size, stream)
                yield self.element_sedes.deserialize(element_data)
        else:
            offsets = tuple(s_decode_offset(stream) for _ in range(self.length))

            for left_offset, right_offset in sliding_window(2, offsets):
                element_length = right_offset - left_offset
                element_data = read_exact(element_length, stream)
                yield self.element_sedes.deserialize(element_data)

            # simply reading to the end of the current stream gives us all of the final element data
            final_element_data = stream.read()
            yield self.element_sedes.deserialize(final_element_data)

    #
    # Tree hashing
    #
    def hash_tree_root(self, value: Sequence[Any]) -> bytes:
        if isinstance(self.element_sedes, BasicSedes):
            serialized_elements = tuple(
                self.element_sedes.serialize(element)
                for element in value
            )
            return merkleize(pack(serialized_elements))
        else:
            element_tree_hashes = tuple(
                self.element_sedes.hash_tree_root(element)
                for element in value
            )
            return merkleize(element_tree_hashes)
