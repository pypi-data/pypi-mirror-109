from typing import TYPE_CHECKING, Any, Tuple, Union
import numpy

from amulet.api.wrapper import Interface, EntityIDType, EntityCoordType
from amulet.api.chunk import Chunk
from amulet.api.selection import SelectionBox
from amulet.api.data_types import AnyNDArray
from amulet.level.loader import Translators
from amulet.api.block import Block
from .chunk import SpongeSchemChunk

if TYPE_CHECKING:
    from amulet.api.wrapper import Translator
    from PyMCTranslate import TranslationManager


class SpongeSchemInterface(Interface):
    _entity_id_type = EntityIDType.namespace_str_Id
    _entity_coord_type = EntityCoordType.Pos_list_double
    _block_entity_id_type = EntityIDType.namespace_str_Id
    _block_entity_coord_type = EntityCoordType.Pos_array_int

    def is_valid(self, key: Tuple) -> bool:
        return True

    def decode(
        self, cx: int, cz: int, data: SpongeSchemChunk
    ) -> Tuple["Chunk", AnyNDArray]:
        """
        Create an amulet.api.chunk.Chunk object from raw data given by the format
        :param cx: chunk x coordinate
        :param cz: chunk z coordinate
        :param data: Raw chunk data provided by the format.
        :return: Chunk object in version-specific format, along with the block_palette for that chunk.
        """
        palette = numpy.empty(len(data.palette) + 1, dtype=object)
        palette[0] = Block(namespace="minecraft", base_name="air")
        palette[1:] = data.palette[:]

        chunk = Chunk(cx, cz)
        box = data.selection.create_moved_box((cx * 16, 0, cz * 16), subtract=True)
        chunk.blocks[box.slice] = data.blocks + 1
        for b in data.block_entities:
            b = self._decode_block_entity(
                b, self._block_entity_id_type, self._block_entity_coord_type
            )
            if b is not None:
                chunk.block_entities.insert(b)
        for e in data.entities:
            e = self._decode_entity(
                e, self._block_entity_id_type, self._block_entity_coord_type
            )
            if e is not None:
                chunk.entities.append(e)

        return chunk, palette

    def encode(
        self,
        chunk: "Chunk",
        palette: AnyNDArray,
        max_world_version: Tuple[str, Union[int, Tuple[int, int, int]]],
        box: SelectionBox,
    ) -> SpongeSchemChunk:
        """
        Take a version-specific chunk and encode it to raw data for the format to store.
        :param chunk: The already translated version-specfic chunk to encode.
        :param palette: The block_palette the ids in the chunk correspond to.
        :type palette: numpy.ndarray[Block]
        :param max_world_version: The key to use to find the encoder.
        :param box: The volume of the chunk to pack.
        :return: Raw data to be stored by the Format.
        """
        entities = []
        for e in chunk.entities:
            if e.location in box:
                entities.append(
                    self._encode_entity(
                        e, self._entity_id_type, self._entity_coord_type
                    ).value
                )
        block_entities = []
        for e in chunk.block_entities:
            if e.location in box:
                block_entities.append(
                    self._encode_block_entity(
                        e, self._block_entity_id_type, self._block_entity_coord_type
                    ).value
                )

        slices = box.create_moved_box(
            (chunk.cx * 16, 0, chunk.cz * 16), subtract=True
        ).slice

        return SpongeSchemChunk(
            box,
            numpy.asarray(chunk.blocks[slices]),
            palette.copy(),
            block_entities,
            entities,
        )

    def get_translator(
        self,
        max_world_version: Tuple[str, int],
        data: Any = None,
        translation_manager: "TranslationManager" = None,
    ) -> Tuple["Translator", Union[int, Tuple[int, int, int]]]:
        platform, version_number = max_world_version
        if platform != "java":
            raise ValueError("Platform must be java")
        version = translation_manager.get_version(platform, version_number)
        version_number = version.data_version
        return Translators.get((platform, version_number)), version_number
