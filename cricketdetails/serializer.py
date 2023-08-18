from rest_framework import serializers
from .models import CricketMatchDetails

class CricketMatchDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CricketMatchDetails
        fields = '__all__'