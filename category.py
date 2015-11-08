__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'

from neomodel import (StringProperty, AliasProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrOne,
                      FloatProperty, ZeroOrMore, OneOrMore)
from neoapi import SerializableStructuredNode, SerializableStructuredRel, DateTimeProperty
import event  # not an unused import


class Category(SerializableStructuredNode):
    """
    Category
    """

    __type__ = 'categories'  # => __type__ must be specified and the same as the default for type

    # INFO
    version = '1.0.0'  # => A version is not required but is a good idea

    # ATTRIBUTES -- NOTE: 'type' and 'id' are required for json api specification compliance
    type = StringProperty(default='categories')  # => required, unique name for model
    id = StringProperty(required=True, unique_index=True)  # => required
    name = AliasProperty(to=id)

    # RELATIONSHIPS
    events = RelationshipFrom('event.Event', 'HAS_CATEGORY', cardinality=OneOrMore, model=SerializableStructuredRel)

