# DHCP基于端口配置举例
> 使用华为eNSP模拟器进行操作, 5700交换机
### 需求

企业内部有三个子网。由于网络管理人员较少，计划个区域内计算机地址使用DHCP方式获得。
- 办公区：192.168.10.1/24  vlan10:192.168.10.1
- 生产区：192.168.20.1/24  vlan20:192.168.20.1
- 生活区：192.168.30.1/24  vlan30:192.168.30.1
 
eNSP拓扑图：

![eNSP拓扑图](http://note.youdao.com/noteshare?id=0791439f17ac5e1ffa4d921c802e2ad9)

### 配置命令
    sysname DHCPtest
    vlan batch 10  20  30	 #创建 VLAN
    dhcp enable	 #启用 DHCP 服务
    interface Vlan 10
    ip  address  192.168.10.1  255.255.255.0
    dhcp  select  interface	#设置 DHCP 基于端口配置
    interface Vlan 20
    ip address 192.168.20.1 255.255.255.0
    dhcp select  interface	#设置 DHCP 基于端口配置
    interface Vlan 30
    ip address 192.168.30.1 255.255.255.0
    dhcp  select  interface	#设置 DHCP 基于端口配置
    dhcp  server   excluded-ip-address 192.168.30.201  192.168.30.254  #排除 192.168.20.201 到 192.168.30.254
    dhcp  server  dns-list  8.8.8.8
    #端口1
    interface GigabitEthernet0/0/1 
    port link-type access
    port default vlan 10
    #端口2
    interface GigabitEthernet0/0/2
    port link-type access 
    port default vlan 20
    #端口3
    interface GigabitEthernet0/0/3 
    port link-type access
    port default vlan 30
### 验证
    在PC端使用ipconfig命令查看ip信息是否为分配地址




