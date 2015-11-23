__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'

from neomodel import (StringProperty, AliasProperty, RelationshipTo, Relationship, ZeroOrOne, One,
                      FloatProperty, ZeroOrMore, OneOrMore, IntegerProperty, RelationshipFrom)
from neoapi import SerializableStructuredNode, SerializableStructuredRel, DateTimeProperty
from uuid import uuid4
import category  # not an unused import statement
import user  # not an unused import statement


class Event(SerializableStructuredNode):
    """
    Event
    """

    __type__ = 'events'  # => __type__ must be specified and the same as the default for type

    # INFO
    version = '1.0.0'  # => A version is not required but is a good idea

    # ATTRIBUTES -- NOTE: 'type' and 'id' are required for json api specification compliance
    type = StringProperty(default='events')  # => required, unique name for model
    id = StringProperty(default=uuid4, unique_index=True)  # => required
    title = StringProperty(required=True)
    description = StringProperty()
    start_time = DateTimeProperty()
    end_time = DateTimeProperty()
    location = StringProperty()
    address = StringProperty()
    lon = FloatProperty()
    lat = FloatProperty()
    link = StringProperty()
    number_going = IntegerProperty(default=0)

    # RELATIONSHIPS
    categories = RelationshipTo('category.Category', 'HAS_CATEGORY', cardinality=OneOrMore,
                              model=SerializableStructuredRel)
    users = RelationshipFrom('user.User', 'GOING_TO', cardinality=ZeroOrMore, model=SerializableStructuredRel)
    owner = RelationshipTo('user.User', 'HAS_OWNER', cardinality=One, model=SerializableStructuredRel)
