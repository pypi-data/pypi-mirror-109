"""The |pydwf.core.dwf_library_subapi| module implements a single class: |AbstractDwfLibrarySubApi|."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydwf.core.dwf_library import DwfLibrary


class AbstractDwfLibrarySubApi:
    """Abstract base class for the sub-API class members of a |DwfLibrary|."""

    def __init__(self, dwf: 'DwfLibrary'):
        self._dwf = dwf

    @property
    def dwf(self):
        """Return the library.
        :meta private:
        """
        return self._dwf

    @property
    def lib(self):
        """Return the |ctypes| library.

        :meta private:
        """
        return self.dwf.lib
