def dict_serializer(obj, fields):
    """Serializes given object into a dictionary.


    Use this to serialize any Python object. The method doesn't not catch
    AttributeError exception.
    """
    _obj = {}
    for field in fields:
        _obj[field] = getattr(obj, field)
    return _obj
