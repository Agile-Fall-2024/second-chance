from rest_framework import serializers

from advertisement.models import Advertisement
from file.serializers import FileSerializer


class AdvertisementSummarySerializer(serializers.ModelSerializer):
    main_picture = FileSerializer(required=True)
    class Meta:
        model = Advertisement
        fields = ['id','author_id','title','main_picture','price','status']

class AdvertisementSerializer(serializers.ModelSerializer):
    main_picture = FileSerializer(required=True)
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['author',]