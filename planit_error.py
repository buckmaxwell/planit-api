__author__ = 'Max Buck'
__email__ = 'maxbuckdeveloper@gmail.com'
__version__ = '1.0.0'


class PlanItError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Forbidden(PlanItError):
    DEFAULT_VALUE='forbidden action'
    def __init__(self, value=DEFAULT_VALUE):
        self.value = value
    def __str__(self):
        return repr(self.value)


class WrongUserError(PlanItError):
    DEFAULT_VALUE = 'you cannot perform this action on a user other than yourself'
    def __init__(self, value=DEFAULT_VALUE):
        self.value = value
    def __str__(self):
        return repr(self.value)
