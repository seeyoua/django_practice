### 解析器的源码使用和剖析序列化组件的使用
#### 序列化接口设计
    1.1 get
        post11
        put
        delete
        
#### 使用方法
    #view.py（get请求）
        1.1 开始使用序列化类
        1.2 导入模块 （from rest_framwork.serializer import Serializer）
        1.2.1 获取qureyset
                from .models import Book
                orgin_data= Book.objects.all()
        1.3 创键序列化类 serializer.py
            class BookSerializer(serializers.Serializer):
                自定义字段
             多对多关系
             authors = seriliazers.SerializerMethodField()
             def get_authours(self,book_obj):
                   author_list=[]
                   for author in book_obj.authors.all():
                        author_list.append(author)
                   return  author_list
        1.4 开始序列化 views.py (many 为返回多条)
                serializer_data = BookSerilazier(orgin_data,many=1true)
        1.5 获取序列化后的数据，返回给客户端
             from rest_framework import Response
             return Response(serialzier_data.data) 
            
        
        
#### 使用方法(post 方法)
   
    1.1 urls.py 
        from django.conf.urls import url
        from .views import BookViews
        urlpatterns = [
            'books/$',BookViews.as_view()
        ]
    2.1 开始序列化
        - 导入模块
            from rest_framwork import serializers
            from .models import Book
        - 创键序列化类(serializer.Serializer 必须自定create的方法否，并且返回存储对象)
            class BookSerializer(serializers.Serializers):
                #定义字段
                authors = serilizers.SerilzerMethodField()
                #每个get请求放回详细的内容 example 
                ""
                @parmas book_obj 为Bookserilaizers(book_obj,many=True) book_obj = Book.Objects.all() 的对象
                """
                def get_authors(self,book_obj):
                    author_list = []
                    for author in book_obj.authors.all():
                        author_list.append(author.name)
                    return author_list
                重新create方法 其中的publish 是request.data 进行序列化的时候,序列化的字段为publish 大事模型类的和数据库的
                字段为publish_id
                def create(self,validate_data):
                    validate_data['publish_id'] = validate_data.pop('publish')
                    book = Book.objects.create(**validate_data)
                    return book
        -开始序列化
            from rest_framwork import APIview
                #序列化字段
                verifield_data = BookSerializers(request.data)
                verifield_data.is_valid(raise_exception=True)
                book = verified_data.save()
                #多对多关系表的简历
                authors = book.authors.filter(nid__in=request.data['authors'])
                book.authors.add(*authors)

                    
    3.1 Get PUT DELETE
        - PUT 方法
            url.py
                url(r'/books/(\d+)/$',views.BookFilterView.as_view())
            1.获取数据对象
                Book。objects.get(pk=nid)
            2.开始序列化(验证数据)
                book = Book.objects.get(pk=nid)
                verified_data = BookSerializer(data=request.data,instance=book_obj,many=False)
                #如果是继承 serilizers.Serializer 则需要重新update方法
                #instnce  为一个book对象
                def update(self,instance,validate): 
                    instance.publish = validated_data['publish_id']
                    instance.save()         
                #注意,当get请求的时候此处为publish title 当post请求的时候需要pop出publish 跟新models的类型publish_id
            3、验证成功写入数据库
                verifield_data.is_valid(raise_exception=True)
                book = verified_data.save()
                authors = book.authors.filter(nid__in= request.data['authors'])
                book.authors.clear() #清楚数据库已经存在的数据
                book.authors.add(*authors)
            3.返回更新的数据
        
        - Delete 方法
        
  
