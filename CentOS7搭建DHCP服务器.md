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
#### 启动服务
    
    使用dhcpd -t命令可以检验配置文件语法错误
    
    使用service dhcpd start命令启动DHCP服务
#### 客户端获取地址
    
    Linux：
        vim /etc/sysconfig/network-scripts/ifcfg-***  #修改配置文件
        BOOTPROTO=dhcp
        ONBOOT=yes
        :wq    #保存退出
        service network restart #重启网络服务
        dhclient -r  #释放ip地址
        dhclient     #获取ip地址
    Windows:
        win+R弹出运行窗口，输入CMD    #进入cmd
        ipconfig /release #释放ip地址
        ipconfig /renew   #获取ip地址
 #### DHCP服务器相关文件  
    
    日志文件(包括请求及响应信息等)：/var/log/messages
    租约信息(ip地址和其他信息)：/var/lib/dhcpd/dhcpd/dhcpd/leases
    
 #### DHCP工作过程
 > 图片来自度娘，侵权请告知
 
 ![DHCP工作过程图](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1553094818771&di=108ed3a651ac68f9f5efa17260b0d463&imgtype=0&src=http%3A%2F%2Ffile.elecfans.com%2Fweb1%2FM00%2F46%2F7A%2Fo4YBAFqeXpaAYNC_AAA3y3CNuN8311.jpg)
    
    首先客户端广播一个DHCPDISCOVER数据包，向网络上任一DHCP服务器请求IP租用
    DHCP服务器向客户端回应一个DHCPOFFER广播包，提供一个IP地址
    客户端选择第一个收到的DHCPOFFER包，并广播一个DHCPREQUEST包，表示已经接受了一个IP
    DHCP服务器向客户端返回一个DHCPACK，表示已经接受客户端的选择
 
    
  
