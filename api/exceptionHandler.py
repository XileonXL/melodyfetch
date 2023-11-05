# -*- coding: utf-8 -*-

class NotFoundError(Exception):
    pass

class InvalidParameterError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class ConflictError(Exception):
    pass

class NoIndexError(Exception):
    pass

class DuplicateError(Exception):
    pass
