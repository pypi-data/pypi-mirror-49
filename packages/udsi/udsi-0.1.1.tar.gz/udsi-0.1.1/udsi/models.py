"""
udsi.bases
~~~~~~~~~~

This module implements UDSI model classes.
"""

import base64
import dataclasses


@dataclasses.dataclass
class UDSIFile:
    """ Implements the core UDSIFile object. """
    id: str
    name: str

    data: str

    @property
    def asdict(self) -> dict:
        return dataclasses.asdict(self)

    def export(self):
        """ Exports data to original file. """
        with open(self.name, 'wb+') as f:
            dec = base64.b64decode(self.data)
            f.write(dec)
