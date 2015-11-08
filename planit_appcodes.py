__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'

from neoapi import http_error_codes

WRONG_USER = '4031', 'you can only perform this action on yourself', http_error_codes.FORBIDDEN
