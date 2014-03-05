from marshmallow.serializers import Serializer
from marshmallow.compat import with_metaclass

# something like this.  Totally untested.
# Make sure obj._meta.fields is actually correct
# Make sure obj._meta.fields does not have reverse relationships for now
class DjangoModelSerializer(Serializer):
    def __init__(self, obj=None, extra=None, only=None,
                 exclude=None, prefix='', strict=False, many=False,
                 context=None):

        if not self.Meta.fields:
            self.Meta.fields = obj._meta.fields

        super(DjangoModelSerializer, self).__init__(obj=None, extra=None, only=None,
                                                    exclude=None, prefix='', strict=False,
                                                    many=False, context=None)
