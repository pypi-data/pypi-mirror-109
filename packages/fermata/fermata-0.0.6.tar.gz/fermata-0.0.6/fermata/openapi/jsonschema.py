import datetime
import uuid

from jsonschema import Draft7Validator
from jsonschema import validators
try:
    from numpy import ndarray
except ImportError:
    ndarray = list

SUPPORTED_TYPES = {
    None: (str, dict, list, tuple, int, float, bool,
        datetime.datetime, datetime.date, datetime.time, uuid.UUID, ndarray, None),
    'boolean': (bool, ),
    'object': (dict, ),
    'array': (list, set, tuple),
    'number': (float, ),
    'string': (str, datetime.datetime, datetime.date, datetime.time, uuid.UUID),
    'integer': (int),
    }


def extend_with_default(validator_class):
    '''copy from jsonschema docs'''

    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
            validator, properties, instance, schema,
        ):
            yield error

    return validators.extend(
        validator_class, {"properties" : set_defaults},
    )

JSONSchema = extend_with_default(Draft7Validator)


class SchematizeError(ValueError):
    pass


class NullRefResolver:

    def push_scope(self, _):
        pass

    def pop_scope(self):
        pass

    def resolve(self, _):
        raise NotImplementedError('should not be called')

null_ref_resolver = NullRefResolver()


def create(schema):
    return JSONSchema(schema, resolver=null_ref_resolver)


def schematizable(obj, type_name):
    supported_types = SUPPORTED_TYPES.get(type_name)
    return supported_types and isinstance(obj, supported_types)


def schematize(schema, obj, default=None, keys=None):
    if keys is None:
        keys = []
    type_name = schema.get('type', 'object')
    if not schematizable(obj, type_name) and default:
        d = default(obj, type_name)
        if d is not None:
            obj = d
    if 'properties' in schema:
        result = {}
        is_dict = isinstance(obj, dict)
        required_keys = schema.get('required', [])
        for key, sub_schema in schema.get('properties', {}).items():
            _keys = keys + [key]
            required = key in required_keys
            exist = is_dict and key in obj or hasattr(obj, key)
            if not required and not exist:
                continue
            if required and not exist:
                raise SchematizeError(f'key({_keys}) is required')
            try:
                if is_dict:
                    val = obj.get(key)
                else:
                    val = getattr(obj, key)
            except AttributeError:
                raise SchematizeError(f'can\'t get "{obj}" value on key({_keys})')
            result[key] = schematize(sub_schema, val, default, _keys)
        return result
    elif 'items' in schema:
        try:
            return [schematize(schema.get('items', {}), item, default, keys + ['[]']) for item in obj]
        except TypeError:
            raise SchematizeError(f'not iteralbe object "{type(obj)}" on key({keys})')
    else:
        val = obj if obj is not None else schema.get('default', None)
        if val is not None and not schematizable(val, type_name):
            raise SchematizeError(f'not schematizable type: {type(val)} to {type_name} on key({keys})')
        return val
