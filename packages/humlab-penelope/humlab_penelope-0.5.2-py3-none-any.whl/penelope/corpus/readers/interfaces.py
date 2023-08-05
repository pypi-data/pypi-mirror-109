from __future__ import annotations

import abc
import csv
import zipfile
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Set, Union

from penelope.utility import FilenameFieldSpecs

if TYPE_CHECKING:
    from ..document_index import DocumentIndex

TextSource = Union[str, zipfile.ZipFile, List, Any]

FilenameOrCallableOrSequenceFilter = Union[Callable, Sequence[str]]


@dataclass
class TextReaderOpts:
    filename_pattern: str = field(default="*.txt")
    filename_filter: Optional[FilenameOrCallableOrSequenceFilter] = None
    filename_fields: Optional[FilenameFieldSpecs] = None
    index_field: Optional[str] = None
    as_binary: Optional[bool] = False
    sep: Optional[str] = field(default='\t')
    quoting: Optional[int] = csv.QUOTE_NONE
    n_processes: int = 1
    n_chunksize: int = 2

    @property
    def props(self) -> dict:
        return dict(
            filename_pattern=self.filename_pattern,
            filename_filter=self.filename_filter,
            filename_fields=self.filename_fields,
            index_field=self.index_field,
            as_binary=self.as_binary,
            sep=self.sep,
            quoting=self.quoting,
            n_processes=self.n_processes,
            n_chunksize=self.n_chunksize,
        )

    def copy(self, **kwargs) -> TextReaderOpts:
        return TextReaderOpts(**{**self.props, **kwargs})

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


PhraseSubstitutions = Union[Dict[str, List[str]], List[List[str]]]


@dataclass
class ExtractTaggedTokensOpts:

    lemmatize: bool

    target_override: Optional[str] = None

    """ These PoS define the tokens of interest """
    pos_includes: str = ''

    """ These PoS are always removed """
    pos_excludes: str = ''

    """ The PoS define tokens that are replaced with a dummy marker `*` """
    pos_paddings: Optional[str] = None
    pos_replace_marker: str = '*'

    passthrough_tokens: List[str] = field(default_factory=list)
    append_pos: bool = False

    phrases: Optional[PhraseSubstitutions] = None

    to_lowercase: bool = False

    block_tokens: List[str] = field(default_factory=list)

    def get_pos_includes(self) -> Set[str]:
        return set(self.pos_includes.strip('|').split('|')) if self.pos_includes else set()

    def get_pos_excludes(self) -> Set[str]:
        return set(self.pos_excludes.strip('|').split('|')) if self.pos_excludes is not None else set()

    def get_pos_paddings(self) -> Set[str]:
        return set(self.pos_paddings.strip('|').split('|')) if self.pos_paddings is not None else set()

    def get_passthrough_tokens(self) -> Set[str]:
        if self.passthrough_tokens is None:
            return set()
        return set(self.passthrough_tokens)

    def get_block_tokens(self) -> Set[str]:
        if self.block_tokens is None:
            return set()
        return set(self.block_tokens)

    @property
    def props(self):
        return dict(
            lemmatize=self.lemmatize,
            target_override=self.target_override,
            pos_includes=self.pos_includes,
            pos_excludes=self.pos_excludes,
            pos_paddings=self.pos_paddings,
            pos_replace_marker=self.pos_replace_marker,
            passthrough_tokens=list(self.passthrough_tokens or []),
            block_tokens=list(self.block_tokens or []),
            append_pos=self.append_pos,
            phrases=None if self.phrases is None else list(self.phrases),
            to_lowercase=self.to_lowercase,
        )


class ICorpusReader(abc.ABC):
    @property
    @abc.abstractproperty
    def filenames(self) -> List[str]:
        return None

    @property
    @abc.abstractproperty
    def metadata(self) -> List[Dict[str, Any]]:
        return None

    @property
    def document_index(self) -> DocumentIndex:
        return None

    @abc.abstractmethod
    def __next__(self):
        'Return the next item from the iterator. When exhausted, raise StopIteration'
        raise StopIteration

    @abc.abstractmethod
    def __iter__(self) -> "ICorpusReader":
        return self
