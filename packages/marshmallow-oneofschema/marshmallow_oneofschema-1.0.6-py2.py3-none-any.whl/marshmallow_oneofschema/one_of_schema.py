from marshmallow import Schema, MarshalResult, UnmarshalResult, ValidationError


class OneOfSchema(Schema):
    """
    This is a special kind of schema that actually multiplexes other schemas
    based on object type. When serializing values, it uses get_obj_type() method
    to get object type name. Then it uses `type_schemas` name-to-Schema mapping
    to get schema for that particular object type, serializes object using that
    schema and adds an extra "type" field with name of object type.
    Deserialization is reverse.

    Example:

        class Foo(object):
            def __init__(self, foo):
                self.foo = foo

        class Bar(object):
            def __init__(self, bar):
                self.bar = bar

        class FooSchema(marshmallow.Schema):
            foo = marshmallow.fields.String(required=True)

            @marshmallow.post_load
            def make_foo(self, data):
                return Foo(**data)

        class BarSchema(marshmallow.Schema):
            bar = marshmallow.fields.Integer(required=True)

            @marshmallow.post_load
            def make_bar(self, data):
                return Bar(**data)

        class MyUberSchema(marshmallow.OneOfSchema):
            type_schemas = {
                'foo': FooSchema,
                'bar': BarSchema,
            }

            def get_obj_type(self, obj):
                if isinstance(obj, Foo):
                    return 'foo'
                elif isinstance(obj, Bar):
                    return 'bar'
                else:
                    raise Exception('Unknown object type: %s' % repr(obj))

        MyUberSchema().dump([Foo(foo='hello'), Bar(bar=123)], many=True).data
        # => [{'type': 'foo', 'foo': 'hello'}, {'type': 'bar', 'bar': 123}]

    You can control type field name added to serialized object representation by
    setting `type_field` class property.
    """
    type_field = 'type'
    type_field_remove = True
    type_schemas = []

    def get_obj_type(self, obj):
        """Returns name of object schema"""
        return obj.__class__.__name__

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        many = self.many if many is None else bool(many)
        if not many:
            result = self._dump(obj, update_fields, **kwargs)
        else:
            result_data = []
            result_errors = {}

            for idx, o in enumerate(obj):
                result = self._dump(o, update_fields, **kwargs)
                result_data.append(result.data)
                if result.errors:
                    result_errors[idx] = result.errors

            result = MarshalResult(result_data, result_errors)

        if result.errors and self.strict:
            raise ValidationError(result.errors)

        return result

    def _dump(self, obj, update_fields=True, **kwargs):
        obj_type = self.get_obj_type(obj)
        if not obj_type:
            return MarshalResult(None, {
                '_schema': 'Unknown object class: %s' % obj.__class__.__name__
            })

        type_schema = self.type_schemas.get(obj_type)
        if not type_schema:
            return MarshalResult(None, {
                '_schema': 'Unsupported object type: %s' % obj_type
            })

        schema = (type_schema if isinstance(type_schema, Schema)
                  else type_schema())

        schema.context.update(getattr(self, 'context', {}))

        result = schema.dump(
            obj, many=False, update_fields=update_fields, **kwargs
        )
        if result.data:
            result.data[self.type_field] = obj_type
        return result

    def load(self, data, many=None, partial=None):
        many = self.many if many is None else bool(many)
        if partial is None:
            partial = self.partial

        if not many:
            result = self._load(data, partial=partial)
        else:
            result_data = []
            result_errors = {}

            for idx, item in enumerate(data):
                result = self._load(item, partial=partial)
                result_data.append(result.data)
                if result.errors:
                    result_errors[idx] = result.errors

            result = UnmarshalResult(result_data, result_errors)

        if result.errors and self.strict:
            raise ValidationError(result.errors)

        return result

    def _load(self, data, partial=None):
        if not isinstance(data, dict):
            return UnmarshalResult({}, {'_schema': 'Invalid data type: %s' % data})

        data = dict(data)

        data_type = data.get(self.type_field)
        if self.type_field in data and self.type_field_remove:
            data.pop(self.type_field)

        if not data_type:
            return UnmarshalResult({}, {
                self.type_field: ['Missing data for required field.']
            })

        try:
            type_schema = self.type_schemas.get(data_type)
        except TypeError:
            # data_type could be unhashable
            return UnmarshalResult({}, {
                self.type_field: ['Invalid value: %s' % data_type]
            })
        if not type_schema:
            return UnmarshalResult({}, {
                self.type_field: ['Unsupported value: %s' % data_type],
            })

        schema = (type_schema if isinstance(type_schema, Schema)
                  else type_schema())

        schema.context.update(getattr(self, 'context', {}))

        return schema.load(data, many=False, partial=partial)

    def validate(self, data, many=None, partial=None):
        try:
            return self.load(data, many=many, partial=partial).errors
        except ValidationError as ve:
            return ve.messages
