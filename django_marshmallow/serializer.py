from __future__ import absolute_import
from marshmallow.serializer import Serializer
from marshmallow import fields, utils
from marshmallow.compat import iteritems, OrderedDict

class DjangoModelSerializer(Serializer):

    # There must be some way of doing this which doesn't require
    # directly copying these 3 methods and then only making very
    # minor changes to _update_fields
    def _update_fields(self, obj):
        '''Update fields based on the passed in object.'''
        # if only __init__ param is specified, only return those fields
        if self.only:
            ret = self.__filter_fields(self.only)
            self.__set_field_attrs(ret)
            self.fields = ret
            return self.fields

        if self.opts.fields:
            # Return only fields specified in fields option
            field_names = set(self.opts.fields)
        elif self.opts.additional:
            # Return declared fields + additional fields
            field_names = set(self.declared_fields.keys()) | set(self.opts.additional) | set([field.name for field in obj._meta.fields])
        else:
            field_names = set(self.declared_fields.keys()) | set([field.name for field in obj._meta.fields])

        # If "exclude" option or param is specified, remove those fields
        excludes = set(self.opts.exclude) | set(self.exclude)
        if excludes:
            field_names = field_names - excludes
        ret = self.__filter_fields(field_names)
        # Set parents
        self.__set_field_attrs(ret)
        self.fields = ret
        return self.fields

    def __set_field_attrs(self, fields_dict):
        '''Set the parents of all field objects in fields_dict to self, and
        set the dateformat specified in ``class Meta``, if necessary.
        '''
        for field_name, field_obj in iteritems(fields_dict):
            if not field_obj.parent:
                field_obj.parent = self
            if not field_obj.name:
                field_obj.name = field_name
            if isinstance(field_obj, fields.DateTime):
                if field_obj.dateformat is None:
                    field_obj.dateformat = self.opts.dateformat
        return fields_dict

    def __filter_fields(self, field_names):
        '''Return only those field_name:field_obj pairs specified by
        ``field_names``.

        :param set field_names: Field names to include in the final
        return dictionary.
        :returns: An OrderedDict of field_name:field_obj pairs.
        '''
        # Convert obj to a dict
        obj_marshallable = utils.to_marshallable_type(self.obj,
            field_names=field_names)
        if obj_marshallable and self.many:
            try: # Homogeneous collection
                obj_dict = utils.to_marshallable_type(obj_marshallable[0],
                    field_names=field_names)
            except IndexError: # Nothing to serialize
                return self.declared_fields
        else:
            obj_dict = obj_marshallable
        ret = OrderedDict()
        for key in field_names:
            if key in self.declared_fields:
                ret[key] = self.declared_fields[key]
            else:
                if obj_dict:
                    try:
                        attribute_type = type(obj_dict[key])
                    except KeyError:
                        raise AttributeError(
                            '"{0}" is not a valid field for {1}.'.format(key, self.obj))
                    field_obj = self.TYPE_MAPPING.get(attribute_type, fields.Raw)()
                else: # Object is None
                    field_obj = fields.Raw()
                # map key -> field (default to Raw)
                ret[key] = field_obj
        return ret
