from collections import OrderedDict
from operator import itemgetter

from rest_framework import serializers


class DynamicNonNullSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed. Also ensure that null field are not
    included in the response.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(filter(itemgetter(1), ret.items()))
        return ret
