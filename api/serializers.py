from mods.models import Mod
from rest_framework import serializers


class ModSerializer(serializers.ModelSerializer):

    simulators = serializers.StringRelatedField(many=True)
    type = serializers.SerializerMethodField('get_type')

    class Meta:
        model = Mod
        fields = [
            'id',
            'title',
            'description',
            'type',
            'simulators',
        ]

    def get_type(self, obj):
        type = obj.type.type
        return type
