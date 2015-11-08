__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'

from neomodel import (StringProperty, AliasProperty, RelationshipTo, RelationshipFrom, Relationship, ZeroOrOne,
                      FloatProperty, ZeroOrMore, OneOrMore)
from neoapi import SerializableStructuredNode, SerializableStructuredRel, DateTimeProperty
import event  # not an unused import
import user


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

    # RELATIONSHIPS
    events = RelationshipFrom('event.Event', 'HAS_CATEGORY', cardinality=ZeroOrMore, model=SerializableStructuredRel)
    users = RelationshipFrom('user.User', 'INTERESTED_IN', cardinality=ZeroOrMore, model=SerializableStructuredRel)


