## Django搭建博客总结
> 对个人博客网站搭建所学到的知识进行一个梳理和记录。

### Django介绍
Django是一个开放源代码的Web应用框架，由Python写成。基于MVC的框架模式。
但Django更关注于MTV模式(因为控制器接受用户输入的部分由框架自行处理)。
- 模型M
  > 通过models.py文件定义数据库的模型。
    
      对象关系映射 (ORM,object-relational mapping)：可以以Python类形式定义你的数据模型，ORM将模型与关系数据库连接起来，
      你将得到一个非常容易使用的数据库API，同时你也可以在Django中使用原始的SQL语句。
- 视图V
  > 通过views.py文件定义视图文件。
    
      视图是模板和模型的桥梁。通过定义它决定从数据库中取得什么样的数据，然后将取到的数据传递给模板。
- 模板T
  > 在项目的根目录新建templates文件夹存放模板文件。

      模板可以理解为前端，通过定义把收到的数据放置到页面的相应位置，构成一个完整的页面。
### Django运行逻辑
- 用户发起请求链接，Django查看urls中定义各种格式的url，找到符合格式的url调用其相应的视图方法。
- 视图方法受到调用，执行相应的代码段，并将相应的数据传递给模板。
- 模板接受到数据后按照定义的前端格式，将不同的数据放到合适的位置，将渲染好的页面给视图。视图构造http响应给用户。
### Django框架常用命令

    命令                              功能
    django-admin startproject ***     创建一个名为***的django项目
    python manage.py startapp ***     创建一个应用(创建好的app要添加至settings里的INSTALLED_APPS中)
    python manage.py makemigrations   创建数据库文件（与行代码顺序执行）
    python manage.py migrate          数据库迁移
    python manage.py createsuperuser  创建超级用户
    python manage.py shell            进入Python命令交互栏
    python manage.py runserver        启动Django服务
### 定义url

    from django.urls import path, include
    
    #引入当前目录下的视图文件
    from . import views
    #path函数用于定义一个url 
    path('contact/', views.Contact, name = 'contact'), #当链接为***/contact/时，调用绑定的Contact方法，name后为别名。  
    #当视图中定义的为类而不是方法时，需要用as_view()方法
    path('post/<int:pk>/', views.PostDetailView.as_view(), name = 'detail'),
    
    #include一般在项目的urls文件中使用，用于将单个应用中的url包含到项目中
    path('', include('blog.urls')),#将blog应用的urls包含进项目
    
### 定义模板

#### 模板变量
> 用{{***}}包裹，用于接收视图函数传递过来的变量。
    
    {{ title }}
    {{ post.pk }}
#### 模板标签
> 用{%***%}包裹，类似于函数。使用前应先引入{%load ***%}
 
- static   

      #引入模块
      {%load staticfiles%}
      #替换路径
      <link rel="stylesheet" href="{% static 'blog/css/pace.css' %}">#static标签会渲染为settings文件中定义的静态文件路径
- for
        
      #开始循环
      {% for post in post_list %}
      <article class="post post-{{ post.pk }}">
      ...
      </article>
      #若post_list为空
      {% empty %}
      <div class="no-post">暂时还没有发布的文章！</div>
      #结束循环
      {% endfor %}
       
### 定义视图
 
- render
  > 结合一个给定的模板和一个给定的上下文字典, 并返回一个渲染后的HttpResponse对象。    
    
      from django.shortcuts import render
      
      return render(request, 'blog/index.html', context={'post_list': post_list})
-  模型管理器 objects
   > 提供一系列从数据库中取数据方法
       
       #获取数据库中的所有Post，按创建时间逆序排列
       Post.objects.all().order_by('-created_time')# - 号表示逆序，all方法返回一个 QuerySet（类似于列表）
   
### 定义模型
> 一个类相当于一个表

    from django.db import models
    
    class Post(models.Model):
        #字符型，最大长度70
        title = models.CharField(max_length=70)
        #存储大段文本
        body = models.TextField()
        #时间类型
        created_time = models.DateTimeField()
        #blank表示可以为空
        excerpt = models.CharField(max_length=200, blank=True)
        #一篇文章只能对应一个分类，但是一个分类下可以有多篇文章
        #分类和文章为一对多关系
        category = models.ForeignKey(Category)
        #一篇文章可以有多个标签，同一个标签下也可能有多篇文章
        #多对多关系
        tags = models.ManyToManyField(Tag, blank=True)
