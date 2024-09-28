from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    fullbody_image = serializers.ImageField()
    clothes_image = serializers.ImageField()