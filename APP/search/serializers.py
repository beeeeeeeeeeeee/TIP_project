from rest_framework import serializers
from app01.models import Piano

# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piano
        fields = ['pid', 'brand', 'model', 'sub_model', 'colour', 'type']