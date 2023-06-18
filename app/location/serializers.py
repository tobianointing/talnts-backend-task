from rest_framework import serializers


class SuggestionSerializer(serializers.Serializer):
    name = serializers.CharField()
    latitute = serializers.FloatField()
    longitute = serializers.FloatField()
    score = serializers.FloatField()
