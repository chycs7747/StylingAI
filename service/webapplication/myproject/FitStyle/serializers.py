from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    top_photos = serializers.ListField(
        child=serializers.ImageField(), 
        required=False
    )
    bottom_photos = serializers.ListField(
        child=serializers.ImageField(), 
        required=False
    )
