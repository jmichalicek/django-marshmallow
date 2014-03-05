django-marshmallow
==================

Django specific serializers based on [Marshmallow][1].
This allows Marshmallow to be used for serializing Django models to JSON
with a few shortcuts that you find in Django specific REST framework serializers.

Currently planned:
* DjangoModelSerializer to automatically default to serializing all of the model's fields
* PaginatedDjangoModelSerializer which takes a Django paginator object and works like Django Rest Framework PaginatedSerializer

[1]: https://github.com/sloria/marshmallow
