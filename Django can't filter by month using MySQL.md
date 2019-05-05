# Django使用MySQL无法按月份过滤问题

使用filter方法按月份过滤数据时，查不到结果。

### 问题原因

当开启USE_TZ(USE_TZ = True)时表示使用UTC模式，也就协调世界时。它的原理是在存入数据库时
存入的不是本地时间而是世界统一时间，当我们前端渲染时再按对应的时区进行改变。所有我们指定
了时区为上海(TIME_ZONE = 'Asia/Shanghai')。这样的好处时当我们处理后台时间时，不需要
考虑后台时间，一系列的转换都交给Django完成。

问题就出在这里，我们的mysql不认识上海这个时区，所以时区转换失败了。

### 解决方法
最直接的可以不使用UTC，直接指定USE_TZ = False。

如果想使用看下面两种方式。
#### Linux
执行命令：

    mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql

#### Windows
- 下载时区文件

     https://dev.mysql.com/downloads/timezones.html
     
     ![MySQL时区文件下载选择](https://s2.ax1x.com/2019/05/05/E02Xlt.png)
         
    根据MySQL版本情况选择适合自己的时区文件。一般都会选择POSIX协议的。
    
    这里我的版本是MySQL8.0.12加Win10。
- 恢复时区数据

    将解压出的时区sql文件移动至mysql文件夹内(mysql-8.0.12-winx64\Data\mysql)。

    执行：
    
        #恢复数据库
        mysql -u username -p password mysql < timezone_posix.sql
        #登录数据库
        mysql -u root -p
        #设置时区
        set global time_zone = 'Asia/Shanghai';
        set session time_zone = 'Asia/Shanghai';
        #验证设置
        select @@global.time_zone,@@session.time_zone;
    
    显示如下:
    
    ![MySQL导入时区命令行](https://s2.ax1x.com/2019/05/05/E02j6P.png)

### 参考文章

- [Django使用MySQL后端日期不能按月过滤的问题及解决方案](https://chowyi.com/Django%E4%BD%BF%E7%94%A8MySQL%E5%90%8E%E7%AB%AF%E6%97%A5%E6%9C%9F%E4%B8%8D%E8%83%BD%E6%8C%89%E6%9C%88%E8%BF%87%E6%BB%A4%E7%9A%84%E9%97%AE%E9%A2%98%E5%8F%8A%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88/)
