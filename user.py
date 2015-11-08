__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'
import event
import names
import random
from constants import UserRoles


from neomodel import (StringProperty, AliasProperty, RelationshipTo, Relationship, ZeroOrOne,
                      FloatProperty, ZeroOrMore, OneOrMore, IntegerProperty, RelationshipFrom)
from neoapi import SerializableStructuredNode, SerializableStructuredRel, DateTimeProperty


class User(SerializableStructuredNode):
    """
    User
    """
    __type__ = 'users'  # => __type__ must be specified and the same as the default for type

    # INFO
    version = '1.0.0'  # => A version is not required but is a good idea
    enums = {'roles': [UserRoles.USER_ROLE, UserRoles.EVENT_CREATOR_ROLE]}

    # ATTRIBUTES -- NOTE: 'type' and 'id' are required for json api specification compliance
    type = StringProperty(default='users')  # => required, unique name for model
    id = StringProperty(default=generate_user_id, unique_index=True)  # => required
    role = StringProperty(default=UserRoles.USER_ROLE)

    # RELATIONSHIPS
    events = RelationshipTo('category.Event', 'GOING_TO', cardinality=OneOrMore,
                              model=SerializableStructuredRel)

    @staticmethod
    def generate_user_id():
        """Creates a fun and quite probably unique user id."""
        return "{fn}-{mn}-{ln}{no}".format(
            fn=names.get_first_name(), mn=names.get_last_name(), ln=names.get_last_name,no=str(random.randint(10, 99))
        )




