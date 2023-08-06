from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import SanitizedUnicode
from marshmallow.fields import List, Nested


class MultilingualStringPartSchemaV1(StrictKeysMixin):
    """Multilingual string"""

    name = SanitizedUnicode(required=True)
    lang = SanitizedUnicode(required=True)


MultilingualStringSchemaV1 = List(Nested(MultilingualStringPartSchemaV1))

__all__ = ('MultilingualStringSchemaV1',)
