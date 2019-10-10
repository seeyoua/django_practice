from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .srializers import BookSerializer
from .models import Book,Author


class BookView(APIView):

    def get(self,request,*args,**kwargs):
        qurey_set = Book.objects.all()
        #开始序列化
        serializer_data = BookSerializer(qurey_set,many=True)
        return Response(serializer_data.data)

    def post(self,request,*args,**kwargs):
        #获取客户端数据
        client_dat = request.data
        #验证数据
        verified_data = BookSerializer(data=client_dat)
        verified_data.is_valid(raise_exception=True)

        book = verified_data.save()
        authors = Author.objects.filter(nid__in=client_dat['authors'])
        book.authors.add(*authors)
        return Response(verified_data.data)


class BookFilterView(APIView):

    def get(self, request, nid):
        book_obj = Book.objects.get(pk=nid)
        serializer_data = BookSerializer(book_obj, many=False)
        return Response(serializer_data.data)

    def put(self, request, nid):
        book_obj = Book.objects.get(pk=nid)
        verified_data = BookSerializer(data=request.data, instance=book_obj, many=False)
        verified_data.is_valid(raise_exception=True)
        book = verified_data.save()
        authors = Author.objects.filter(nid__in=request.data['authors'])
        book.authors.clear()
        book.authors.add(*authors)
        return Response(verified_data.data)

    def delete(self, request, nid):
        Book.objects.get(nid=nid).delete()
        return Response({"messages":"ok"})






