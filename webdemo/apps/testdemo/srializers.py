""""
author :tomlin
time: 2019-9-09 23:11
email: rain_day01@163.com
conetnt: serialzier study
"""

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.Serializer):
    nid = serializers.CharField(max_length=255,allow_blank=False,required=False)
    title = serializers.CharField(max_length=200)
    publish = serializers.CharField()
    prince = serializers.DecimalField(max_digits=5,decimal_places=2)
    authors = serializers.SerializerMethodField()

    def get_authors(self,book_obj):
        authors_list = []
        for each in book_obj.authors.all():
            authors_list.append(each.name)
        return authors_list

    def create(self, validated_data):
        #数据不复杂的情况下可用这种方式处理，数据复杂时可以做数据校验
        validated_data['publish_id'] = validated_data.pop('publish')
        book = Book.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        instance.publish_id = validated_data['publish']
        instance.save()


        return instance


