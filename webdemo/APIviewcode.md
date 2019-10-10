###django drf 源码解读 和 CBV
    DRF 请求流程和源码剖析(其中flask中的flask-rest也是类似)
       1.本质上drf 就是django的一个app
       2.drf 封装了很多的功能其中包括
           2.1 解析组件
           2.2 序列化组件
           2.3 认证组件
           2.4 权限组件
           2.5 视图组件

###View 解读（cbv 方式dispach方法位于base.py）
      
    from django.conf.urls import url
    from . import views
    urlpatterns = [
           url(r"books/$",views.CursorView.as_viwes()),
      ]
      
####url 绑定视图      
    def as_view(cls, **initkwargs):
        """
        cls 为CursorView 视图类
        """
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            """
            实例化CursorView视图类,
            """
            self = cls(**initkwargs)
            """
            查看cursorview视图中的方法
            """
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            #查找dispatch方法 
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        #返回一个视图
        return view
    #注意：
        dispatch（）来处客户端发过来的请求1.首先查找CusorView 中的dispatch方法
        如果不存在继续查找父类，其中cbv方式中的dispach方法位于父类的View中
        
        
####dispach 方法
    
      def dispatch(self, request, *args, **kwargs):
          """
           查找request中的请求方式[get,post,put],其中的hander 为获得
           请求方式
          """
          if request.method.lower() in self.http_method_names:
              handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
          else:
              handler = self.http_method_not_allowed
          """
          通过获得请求方式去调用视图
          """
          return handler(request, *args, **kwargs）
      
### APIview 的使用方式
    #url.py
    from django.conf.urls import url
    from views import CursorsView
    urlpatterns = [
           url(r"books/$",views.CursorView.as_viwes()),
    ] 
    
    #views.py
    from rest_framwork.views import APIview
    class  CursorsView(APIview):
    
        def get(self,request,*args,**kwargs)
                pass
        
        def post(self,*args,**kwargs):
            pass
         ....
###APIview 的请求流程
        1、 启动django：python manage.py runserver ip:port
        2、加载settings：
            2.1 加载models.py
            2.2 加载 views.py
            2.3 加载 urls.py
                2.3.1 re_path(r'curors/$'，CursorsView.as_view()),开始执行as_view()方法
                2.3.2 urls.py url和视图函数之间建立绑定关系
     
        3. 等待用户请求
        4、接收用户请求:127.0.0.1:8000
        5.开始查找url和视图间的绑定关系，根据用户的请求url找到对应的视图函数
        6、开始执行视图view(request)
        7、开始执行dispatch 方法
        8、将请求结果返回给视图
      
#### drf 中的apiview继承了view 并且重写了as_view()方法
    """
        views 中的as_view() 方法
    """
    @classonlymethod
    def as_view(cls, **initkwargs):
        def view(request, *args, **kwargs):
            #cls 实例化CursorView
            self = cls(**initkwargs)
            #把原生的request的请求复制给CursorView的实例化对象
            self.request = request
            #为request中请求是否带有参数即url的请求参数
            self.args = args
            self.kwargs = kwargs
            #view视图的返回结过就是dispatch的返回结果,即response的相应
            return self.dispatch(request, *args, **kwargs)
        view.view_class = cls
        view.view_initkwargs = initkwargs

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view
        
    """
    APIView 中的 as_view() 类方法 继承views 中的as_view()
    """
    @classmethod
    def as_view(cls, **initkwargs):
       
       """
       cls 为view.py 中自己创键的视图类
       """
        if isinstance(getattr(cls, 'queryset', None), models.query.QuerySet):
            def force_evaluation():
                raise RuntimeError(
                    'Do not evaluate the `.queryset` attribute directly, '
                    'as the result will be cached and reused between requests. '
                    'Use `.all()` or call `.get_queryset()` instead.'
                )
            cls.queryset._fetch_all = force_evaluation
        #继承viws 中的as_view()方法 最主要的是继承了dispach方法
        view = super(APIView, cls).as_view(**initkwargs)
        #cls 为CursorsView 
        view.cls = cls
        view.initkwargs = initkwargs
        
        # all other authentication is CSRF 的装饰器返回是视图
        return csrf_exempt(view)
        
#### drf 中封装了view中请求的dispatch方法（注解：首先去CursorView中查找==>>在去APIview中查找）

     def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        ""
            重新封装request请求,self 为视图类(初始化request)
        """
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response
        
        
#### drf 中的initialize_request 重新封装
     def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        parser_context = self.get_parser_context(request)
        #Request 为drf自己封装的request
        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )
        
##### drf APIview 的request的data的请求流程
                1、 启动django：python manage.py runserver ip:port
        2、加载settings：
            2.1 加载models.py
            2.2 加载 views.py
            2.3 加载 urls.py
                2.3.1 re_path(r'curors/$'，CursorsView.as_view()),开始执行as_view()方法
                2.3.2 urls.py url和视图函数之间建立绑定关系
     
        3. 等待用户请求
        4、接收用户请求（post）:127.0.0.1:8000
        5.开始self.post()
            5.1 request.data 触发解析器操作
        6、开始执行视图view(request)
        7、开始执行dispatch 方法
        8、将请求结果返回给视图
    


##### drf 封装的 Request 类
    class Request(object):

    """"
    @parmas request 为原始的request
    @params  parsers 为get_parsers() 的返回值
    @params authenticators 为 get_authenticators() 方法的返回参数
        
    """
    def __init__(self, request, parsers=None, authenticators=None,
                 negotiator=None, parser_context=None):
        assert isinstance(request, HttpRequest), (
            'The `request` argument must be an instance of '
            '`django.http.HttpRequest`, not `{}.{}`.'
            .format(request.__class__.__module__, request.__class__.__name__)
        )

        self._request = request
        self.parsers = parsers or ()  #self.get_parsers() 的执行结果
        self.authenticators = authenticators or ()
        self.negotiator = negotiator or self._default_negotiator()
        self.parser_context = parser_context
        self._data = Empty
        self._files = Empty
        self._full_data = Empty  #为空
        self._content_type = Empty
        self._stream = Empty

        if self.parser_context is None:
            self.parser_context = {}
        self.parser_context['request'] = self
        self.parser_context['encoding'] = request.encoding or settings.DEFAULT_CHARSET

        force_user = getattr(request, '_force_auth_user', None)
        force_token = getattr(request, '_force_auth_token', None)
        if force_user is not None or force_token is not None:
            forced_auth = ForcedAuthentication(force_user, force_token)
            self.authenticators = (forced_auth,)
        
        
    [ _hasattr 不是request对象而是一个全局变量
        def _hasattr(obj, name):
            return not getattr(obj, name) is Empty
    ]
    
        def _load_data_and_files(self):
            if not _hasattr(self, '_data'):
                #开始执行self.parse() 方法
                self._data, self._files = self._parse()
            if self._files:
                self._full_data = self._data.copy()
                self._full_data.update(self._files)
            else:
                self._full_data = self._data
                
            if is_form_media_type(self.content_type):
                self._request._post = self.POST
                self._request._files = self.FILES
    #request.data 出发解析器 slef 为request对象
    @property
    def data(self):
        if not _hasattr(self, '_full_data'):
            self._load_data_and_files()
        return self._full_data
    
### drf 执行Request类中的_parse()方法 返回解析解析请求的结果
    class CursorsView(APIview):
        def post(self,request,*args,**kwargs):
            parse_data = request.data
            
     
    #源码类Request的 _parse():
    def _parse(self):
        #为application/json 为请求方式
        media_type = self.content_type
        try:
            stream = self.stream   #WSGIrequest cursors/POST
        except RawPostDataException:
            if not hasattr(self._request, '_post'):
                raise
            if self._supports_form_parsing():
                return (self._request.POST, self._request.FILES)
            stream = None

        if stream is None or media_type is None:
            if media_type and is_form_media_type(media_type):
                empty_data = QueryDict('', encoding=self._request._encoding)
            else:
                empty_data = {}
            empty_files = MultiValueDict()
            return (empty_data, empty_files)
        #sel.parse 为实例化request的传递的参数 self.parse = self.get_parssers() 的返回接结果 在 apiview中查找
        parser = self.negotiator.select_parser(self, self.parsers)

        if not parser:
            raise exceptions.UnsupportedMediaType(media_type)

        try:
            parsed = parser.parse(stream, media_type, self.parser_context)
        except Exception:

            self._data = QueryDict('', encoding=self._request._encoding)
            self._files = MultiValueDict()
            self._full_data = self._data
            raise

        # Parser classes may return the raw data, or a
        # DataAndFiles object.  Unpack the result as required.
        try:
            return (parsed.data, parsed.files)
        except AttributeError:
            empty_files = MultiValueDict()
            return (parsed, empty_files)

 
 
 
       