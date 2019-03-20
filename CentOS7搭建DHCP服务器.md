# CentOS7搭建DHCP服务器
> 通过一个小案例掌握DHCP服务器的基本搭建方法。
### 需求分析
    
   - 动态分配的IP地址范围为192.168.1.100-192.168.1.200
   - 子网掩码为255.255.255.0
   - 默认网关地址为192.168.1.254
   - 客户端使用的DNS服务器的IP地址为114.114.114.114
   - 域名为test.com
   - 为指定计算机保留192.168.1.150地址(mac地址为:00:0a:30:bc:00:12)
### 操作步骤
> 如未安装dhcp服务，可以使用yum install dhcp命令进行安装。
#### 修改配置文件
> 安装dhcp服务后，在/usr/share/doc/dhcp*/目录下会有配置文件的样本，可以自行查看。
    
    option domain-name "test.com";
    option domain-name-service 114.114.114.114;
    default-lease-time 600;  #默认租约时间
    max-lease-time 7200;   #最大租约时间
    #设置子网属性
    subnet 192.168.1.0 netmask 255.255.255.0{
    range 192.168.1.100 192.168.1.200;  #地址范围
    option routers 192.168.1.254;   #默认网关
    }
    #设置主机属性
    host special{
    hardware ethernet 00:0a:30:bc:00:12;   #mac
    fixed-address 192.168.1.150;   #保留地址
    }
