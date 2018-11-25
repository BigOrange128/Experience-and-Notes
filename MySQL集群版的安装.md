# MySQL集群安装及使用

### 实验目的
掌握MySQL集群的安装方法。需要3-5台计算机，来搭建集群。我们使用虚拟机来模拟。
### 实验环境
centos7计算机，mysql-cluster-gpl-7.5.7-linux-glibc2.12-x86_64.tar.gz
### MySQL集群规划
>最少需要三台机器
  
    主机名 IP地址  服务描述
  
    Cluster-1 192.168.1.217 MC管理节点
  
    Cluster-2 192.168.1.105 MC数据服务节点
  
    Cluster-3 192.168.1.94 MC数据服务节点
  
    Cluster-4 192.168.1.96  MC SQL服务节点
  
    Cluster-5 192.168.1.97  MC SQL服务节点
### 配置MySQL Cluster安装环境
>需要在集群中的所有计算机中进行
- 使用命令“rpm -qa | grep mysql”或“yum list installed | grep mysql”检查本机是否已经安装了MySQL软件，若已经安装了MySQL软件，则使用命令“rpm -e --nodeps 软件包名”或“yum -y remove mysql”将已经安装的MySQL软件删除。
- 使用命令“rpm -qa | grep mariadb”或“yum list installed | grep mariadb”检查是否已经安装了MariaDB软件，该数据库软件是CentOS 7.2自带的数据库，有可能与MySQL软件的数据库内核产生冲突，建议在安装MySQL数据库之前将其删除，使用命令“rpm -e --nodeps 软件包名”可以将已经安装的MariaDB软件删除。
- 使用命令“rpm -qa | grep libaio”或“yum list installed | grep libaio”检查本机是否已经安装了libaio软件，MySQL数据库的安装需要依赖于该软件。该软件的安装软件包名称为“libaio-0.3.109-13.el7.x86_64.rpm”,存放于用户家目录的“setups”目录下，该目录为事先自行创建并将实训相关软件包从优盘拷贝至该目录下。若该软件还没有安装，则使用命令“rpm -ivh 软件包路径”进行安装。
- 使用命令“cat /etc/group | grepmysql”检查mysql用户组是否存在，若不存在则使用命令“groupadd mysql”创建mysql用户组。
- 使用命令“cat /etc/passwd | grep mysql”检查mysql用户是否存在，若不存在则使用命令“useradd -r -g mysql mysql”创建mysql用户并加入到mysql用户组中，选项“-r”表示该用户是内部用户，不允许外部登录。若mysql用户存在但不属于mysql用户组，则使用命令“usermod -g mysql”修改mysql用户其所属的用户组为mysql。
- 使用命令“sestatus -v”查看当前系统中SELinux服务的运行状态，若“SELinux status”参数所在行显示为“enabled”则表示为启动状态，需要进行永久关闭。SELinux配置文件位于目录“/etc/selinux”下，配置文件的文件名为“config”,使用命令“vi 配置文件名及路径”修改配置文件，找到配置项“SELINUX”所在行，将其改为以下内容：
SELINUX=disabled
#### 修改完成后使用命令“reboot”重启系统，再次使用命令“sestatus-v”查看当前系统中SELinux服务的运行状态。
### 安装MySQLCluster
- MySQL Cluster软件包
- “mysql-cluster-gpl-7.5.7-linux-glibc2.12-x86_64.tar.gz”存放于用户家目录的“2-mysql”目录下，该目录为事先自行创建并将实训相关软件包从优盘拷贝至该目录下。
- 使用命令“mkdir /mysql”创建用于存放MySQL相关文件的目录，并使用命令“cd /mysql”进入该目录。
- 使用命令“tar -xvzf ~/setups/mysql-cluster-gpl-7.5.7-linux-glibc2.12-x86_64.tar.gz”将软件包解压解包到“mysql”目录下，解压解包出来的目录名称为“mysql-cluster-gpl-7.5.7-linux-glibc2.12-x86_64”。
- 使用命令“cd /usr/local”进入系统的“/usr/local”目录，使用命令“ln -s /mysql/mysql-cluster-gpl-7.5.7-linux-glibc2.12-x86_64 mysql”在该目录下创建一个名为“mysql”的链接指向MySQL Cluster所在的目录。
- 使用命令“cd mysql”进入链接的mysql目录，使用命令“mkdir data”创建存放MySQL数据库数据的目录，并使用命令“chmod 770 data”更改该数据目录的权限设置。
- 使用命令“chown -R mysql .”和“chgrp -R mysql .”更改当前“mysql”目录的所属用户和所属组。
- 配置MySQL相关的环境变量，需要修改系统的配置文件“/etc/profile”，该文件位于用户家目录下，是隐藏文件，使用命令“vi /etc/profile” 对配置文件进行修改，在文件末尾添加以下内容：

      #mysql-cluster environment
      MYSQL_CLUSTER_HOME=/usr/local/mysql
      PATH=$MYSQL_CLUSTER_HOME/bin:$PATH（确保此项输入正确，否则可能会导致所有命令无法使用）
      export MYSQL_CLUSTER_HOME PATH（必须按照前面的定义顺序书写）
- 使用命令“source /etc/profile”使新配置的环境变量立即生效。使用命令“echo $MYSQL_HOME”、“echo $PATH”查看新添加和修改的环境变量是否设置成功，以及环境变量的值是否正确。
### 配置管理节点Cluster-1
- 使用命令“cd /usr/local/mysql”进入MySQL Cluster软件所在目录。
- 使用命令“mkdir mysql-cluster”创建存放MySQL Cluster数据的目录，并使用命令“chown -R mysql mysql-cluster”和“chgrp -R mysql mysql-cluster”更改“mysql-cluster”目录的所属用户和所属组。
- 使用命令“mkdir etc”创建用于存放MySQL Cluster管理节点配置文件的目录，并使用命令“cd etc”进入该目录。
- 使用命令“touch config.ini”创建MySQL Cluster管理节点的配置文件，并使用命令“vi config.ini”对配置文件进行修改，在其中添加如下内容：
        
        [NDBD DEFAULT]
        NoOfReplicas=2
        DataMemory=512M
        IndexMemory=32M
        DataDir=/usr/local/mysql/data
        [NDB_MGMD]
        NodeId=1
        HostName=Cluster-1
        [NDBD]
        NodeId=2
        HostName=Cluster-2
        [NDBD]
        NodeId=3
        HostName=Cluster-3
        [MYSQLD]
        NodeId=4
        HostName=Cluster-4
        [MYSQLD]
        NodeId=5
        HostName=Cluster-5
        使用命令“chown -R mysql .”和“chgrp -R mysql .”更改当前“etc”目录的所属用户和所属组。

- 使用命令“ndb_mgmd -f /usr/local/mysql/etc/config.ini--initial”启动MySQL Cluster的管理节点。
#### 首次启动或配置修改之后启动需要添加参数“--initial”，正常启动时不需要添加参数“--initial”。
- 使用命令“ps -ef | grep ndb_mgmd”查看系统进程信息，若存在信息中包含“ndb_mgmd”关键字的进程则表示MySQL Cluster的管理节点启动成功。
- 使用命令“ndb_mgm”可以进入MySQL Cluster管理节点的控制台，在控制台中使用“show”可以查看节点状况，使用命令“exit”可以退出控制台。
### 配置数据服务节点Cluster-2、Cluster-3
- 使用命令“cd /etc”进入系统配置文件所在目录。
- 使用命令“touch my.cnf”创建MySQL Cluster数据服务节点的配置文件，并使用命令“vi my.cnf”对配置文件进行修改，在其中添加如下内容：
        
        [MYSQLD]
        #运行NDB存储引擎
        ndbcluster
        #指定管理节点地址
        ndb-connectstring=Cluster-1
        [MYSQL_CLUSTER]
        ndb-connectstring=Cluster-1

- 使用命令“ndbd--initial”启动数据服务节点。
- 使用命令“ps -ef | grep ndbd”查看系统进程信息，若存在信息中包含“ndbd”关键字的进程则表示MySQL Cluster的数据服务节点启动成功。
- 在管理节点主机上使用命令“ndb_mgm”进入MySQL Cluster管理节点的控制台，在控制台中使用“show”可以查看节点状况，若有相应数据服务节点的连接信息，则表示数据服务节点启动并连接成功。
### 配置SQL服务节点Cluster-4、Cluster-5
- 使用命令“cd /etc”进入系统配置文件所在目录。
- 使用命令“touch my.cnf”创建MySQL Cluster数据服务节点的配置文件，并使用命令“vi my.cnf”对配置文件进行修改，在其中添加如下内容：

        [MYSQLD]
        basedir=/usr/local/mysql
        datadir=/usr/local/mysql/data
        #运行NDB存储引擎
        ndbcluster
        #指定管理节点地址
        ndb-connectstring=Cluster-1
        [MYSQL_CLUSTER]
        ndb-connectstring=Cluster-1
- 使用命令“mysqld --initialize --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data”对MySQL数据库的安装进行初始化，执行该命令后会有一些提示信息，特别注意最后一行的“[Note]”相关信息，信息内容如下：信息末尾的“XXXXXXXXXXXXXX”是安装程序随机生成的初始密码，在首次以root用户登录数据库时需要使用，一定要记下。
        
        [Note] A temporary password is generated for root@localhost: XXXXXXXXXXXXXX
- 使用命令“cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysql”可以将MySQL加入到系统的可控制启动服务目录内，并将服务名命名为“mysql”。
- 使用命令“chkconfig --add mysql”和“chkconfig --level 2345 mysql on”可以将MySQL服务配置为开机自动启动。
- 使用命令“service mysql start”启动SQL服务节点。
- 使用命令“ps -ef | grep mysql”查看系统进程信息，若存在信息中包含“mysql”关键字的进程则表示MySQL Cluster的数据服务节点启动成功。
- 在管理节点主机上使用命令“ndb_mgm”进入MySQL Cluster管理节点的控制台，在控制台中使用“show”可以查看节点状况，若有相应SQL服务节点的连接信息，则表示SQL服务节点启动并连接成功。
- 使用命令“mysql -u root -p”登录MySQL数据库，会提示输入密码，该密码为之前进行安装初始化时所显示的初始密码，正确输入密码成功登录MySQL数据库之后会进入MySQL的控制台。
  - 在MySQL控制台使用命令“SET PASSWORD=PASSWORD('1');”重新设置数据库的“root”用户的登录密码，其中“****”部分为自定义的新密码。
  - 在MySQL控制台使用命令“USE mysql;”切换到“mysql”数据库。
  - 在MySQL控制台使用命令“UPDATE user SET host='%' WHERE user='root';”修改数据库的root用户所接收请求来源的范围。
  - 在MySQL控制台使用命令“FLUSHPRIVILEGE;”刷新数据库的权限信息使新配置的权限生效。
  - 在MySQL控制台使用命令“exit”可以退出MySQL控制台返回到系统命令行界面。
  - 使用命令“firewall-cmd --zone=public --add-port=3306/tcp --permanent”添加系统防火墙的端口策略，对外开启MySQL所使用的端口“3306”；
  - 使用命令“firewall-cmd -reload”重启系统防火墙服务，使新添加的端口策略生效。
### 验证
- 在任意一台SQL服务节点主机上使用命令“mysql -u root -p”登录到MySQL数据库，会提示输入密码，正确输入密码成功登录MySQL数据库之后会进入MySQL的控制台。
- 在MySQL控制台使用命令“CREATE DATABSE test;”创建数据库“test”。
- 在任意一台其它SQL服务节点主机上使用命令“mysql -u root -p”登录到MySQL数据库，会提示输入密码，正确输入密码成功登录MySQL数据库之后会进入MySQL的控制台。
#### 可以使用命令“ssh 目标主机名或IP地址”远程登录到集群中其它SQL服务节点主机进行操作，完成所有操作后使用命令“logout”退出当前登录。
- 在MySQL控制台使用命令“SHOW DATABSES;”显示数据库列表，若存在名为“test”的数据库，则表示集群同步数据成功。
### 常见问题
- 无法启动节点
  - 修改hosts文件，添加IP和主机名的对应关系。(vi /etc/hosts)
    
        例如
        192.168.1.1  Cluster-1
        192.168.1.2  Cluster-2
  - 修改network文件，修改主机名。(vi /etc/sysconfig/network)
    
        NTEWORKING=yes
        HOSTNAME=Cluster-1
- 无法连接至管理节点
  - 优先检查配置，确保配置文件没有出错。
  - 关闭防火墙。(systemctl stop firewalld.service)
