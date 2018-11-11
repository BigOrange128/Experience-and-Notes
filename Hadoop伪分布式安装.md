# Hadoop伪分布式安装与使用


#### 实验目的
掌握Hadoop的伪分布式安装方法。由于不具备集群环境，需要在一台计算机上模拟一个小的集群。
通过本实验在单机上进行Hadoop的伪分布式安装方法。


#### 实验环境
虚拟机CentOS6.5系统,Hadoop-2.6.0。

#### 实验内容
1.使用网页浏览分布式文件系统节点运行情况并查看目录

2.使用jps查看hadoop运行进程

3.在HDFS中创建并练习上传下载文件

#### Hadoop部署安装
1.可以使用scp方法远程拷贝实验安装文件。

2.使用tar命令解压安装包到/usr/local/目录下。

3.进入/usr/local/目录，更改hadoop-2.6.0目录名称为hadoop

#### Hadoop配置

1.openjdk开发包安装
>由于hadoop采用java语言开发，其依赖于java运行环境，因此需要提前安装好java开发包。

(1)使用jps命令查看是否已经安装java开发包，返回command not found说明没有安装。（未安装进入下一步）

(2)修改/etc/yum.repos.d/CentOS-Base.repo文件以更改yum源。
>默认yum下载源的javaopenjdk开发包版本可能过高，与实验所用的hadoop版本不兼容，所以更改yum源。

    示例
    [test]
    name=test
    baseurl=http://****/centos/$releasever/$barsearch/
    enabled=1
    gpgchek=0
    
(3)使用yum list|grep openjdk命令查看yum中名称为openjdk的文件列表。使用yum install命令进行安装。
>本实验安装的是java-1.7.0-openjdk-devel.x86_64版本。

2.环境变量配置

(1)编辑环境变量(vi ~/.bashrc）。

    export JAVA_HOME=/usr
    export PATH=/usr/local/hadoop/bin/:usr/local/hadoop/sbin/:$PATH
    export HADOOP_HOME=/usr/local/hadoop
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/lib/native
    
(2)环境变量生效(source ~/.bashrc)。

(3)使用echo $JAVA_HOME(检验变量值)，java -version命令检验是否设置正确。

(4)使用hadoop version命令查看Hadoop是否可用，成功会显示Hadoop版本信息。

3.Hadoop配置
>Hadoop 的配置文件位于 /usr/local/hadoop/etc/hadoop/ 中，伪分布式需要修改2个配置文件 core-site.xml 和 hdfs-site.xml 。Hadoop的配置文件是 xml 格式，每个配置以声明 property 的 name 和 value 的方式来实现。

(1)修改配置文件 core-site.xml （vi core-site.xml)，修改为下面配置：
    
    <configuration> 
      <property> 
        <name>hadoop.tmp.dir</name> 
        <value>file:/usr/local/hadoop/tmp</value> 
        <description>Abase for other temporary directories.</description> 
      </property> 
      <property> 
        <name>fs.defaultFS</name> 
        <value>hdfs://localhost:9000</value> 
      </property>
    </configuration>
    
(2)修改配置文件 hdfs-site.xml （vi hdfs-site.xml)，修改为下面配置：

    <configuration> 
      <property> 
        <name>dfs.replication</name> 
        <value>1</value> 
      </property> 
      <property> 
        <name>dfs.namenode.name.dir</name> 
        <value>file:/usr/local/hadoop/tmp/dfs/name</value> 
      </property> 
      <property> 
        <name>dfs.datanode.data.dir</name> 
       <value>file:/usr/local/hadoop/tmp/dfs/data</value>
      </property> 
    </configuration>
    
 Hadoop配置文件说明
 >Hadoop 的运行方式是由配置文件决定的（运行 Hadoop 时会读取配置文件），因此如果需要从伪分布式模式切换回非分布式模式，需要删除 core-site.xml 中的配置项。此外，伪分布式虽然只需要配置 fs.defaultFS 和 dfs.replication 就可以运行（官方教程如此），不过若没有配置 hadoop.tmp.dir 参数，则默认使用的临时目录为 /tmp/hadoo-hadoop，而这个目录在重启时有可能被系统清理掉，导致必须重新执行 format 才行。所以我们进行了设置，同时也指定 dfs.namenode.name.dir 和 dfs.datanode.data.dir，否则在接下来的步骤中可能会出错。

#### Hadoop使用

1.启动HDFS

(1)配置完成后，执行NameNode命令(hdfs namenode -format)进行格式化。
>成功的话，会看到 “successfully formatted” 和 “Exitting with status 0” 的提示，若为 “Exitting with status 1” 则是出错。如果在这一步时提示 Error: JAVA_HOME is not set and could not be found. 的错误，则说明之前设置 JAVA_HOME 环境变量那边就没设置好，请按教程先设置好 JAVA_HOME 变量，否则后面的过程都是进行不下去的。如果已经按照前面教程在.bashrc文件中设置了JAVA_HOME，还是出现 Error: JAVA_HOME is not set and could not be found. 的错误，那么，请到hadoop的安装目录修改配置文件“/usr/local/hadoop/etc/hadoop/hadoop-env.sh”，在里面找到“export JAVA_HOME=${JAVA_HOME}”这行，然后，把它修改成JAVA安装路径的具体地址，比如，“export JAVA_HOME=/usr/lib/jvm/default-java”，然后，再次启动Hadoop。

(2)开启NameNode和DataNode守护进程(start-dfs.sh)。若出现SSH提示，输入yes即可。
>启动时可能会出现如下 WARN 提示：WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform… using builtin-java classes where applicable WARN 提示可以忽略，并不会影响正常使用。

(3)启动完成后，通过jps命令判断是否成功启动。
>若成功启动则会列出如下进程: “NameNode”、”DataNode” 和 “SecondaryNameNode”（如果 SecondaryNameNode 没有启动，请运行 sbin/stop-dfs.sh 关闭进程，然后再次尝试启动尝试）。如果没有 NameNode 或 DataNode ，那就是配置不成功，请仔细检查之前步骤，或通过查看启动日志排查原因。

>文末有相应的解决方案

(4)成功启动后,可以访问Web界面查看NameNode和DataNode信息，还可以查看HDFS中的文件。(http://localhost:50070)

2.使用HDFS，创建目录，上传文件和下载文件。

(1)首先需要在HDFS中创建用户目录(hdfs dfs -mkdir -p /user/hadoop)。
>我们使用的是 root 用户，并且已创建相应的用户目录 /user/root ，因此在命令中就可以使用相对路径如 input，其对应的绝对路径就是 /user/root/input。

(2)创建input文件夹(./bin/hdfs dfs -mkdir -p input)，作为上传文件存放的文件夹。

(3)将./etc/hadoop中的xml文件作为输入文件复制到分布式文件系统中(./bin/hdfs dfs -put ./etc/hadoop/*.xml input)。
>即将/usr/local/hadoop/etc/hadoop复制到分布式文件系统中的/user/root/input中。

(4)查看文件列表(./bin/hdfs dfs -ls input)。

(5)将其中一个hdfs-site文件下载到本地(./bin/hdfs dfs -get hdfs-site.xml ./output)。
>先创建一个output文件夹作为下载文件存放的文件夹(mkdir ./output)。

注意：HDFS有三种shell命令方式：hadoop fs、hadoop dfs、 hdfs dfs。

    hadoop fs适用任何不同的文件系统，如本地文件系统和HDFS文件系统

    hadoop dfs只能适用于HDFS文件系统

    hdfs dfs跟hadoop dfs的命令作用一样，也只能适用于HDFS文件系统
   
#### 实验常见问题

1.namenode无法启动 

解决方案：$bin/hadoop dfsadmin -safemode leave #关闭safe mode 这样，就解决了namenode 无法启动的问题。 我们在使用 hadoop namenode -format 时，才会初始化一个name文件夹，在启动datanode后，才会创建一个data目录，所以我使用的方法是，把/cloud/hadoop-2.2.0/tmp 目录清空，然后重新格式化namenode,再分别启动 hdfs。

2.datanode无法启动

修改/etc/hosts，增加如下内容

127.0.0.1 1502-centos6-38
