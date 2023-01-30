from rest_framework import serializers

from base.models import foodlist, foodlike


class foodlistserializer(serializers.ModelSerializer):
    class Meta:
        model = foodlist
        fields = '__all__'


class foodlikeserializer(serializers.ModelSerializer):
    class Meta:
        model = foodlike
        fields = '__all__'
