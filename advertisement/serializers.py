from rest_framework import serializers

from advertisement.models import Advertisement, Category


class AdvertisementSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id','author_id','title','main_picture','price','status', 'category']

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['author',]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'