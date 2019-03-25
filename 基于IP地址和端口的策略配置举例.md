# 基于IP地址和端口的策略配置
> 使用华为eNSP模拟器进行操作。
### 需求

某企业部署两台业务服务器，其中Server1通过TCP 8888端口对外提供服务，Server2通过UDP 6666端口对外提供服务。需要通过FW进行访问控制，8：00～17：00的上班时间段内禁止IP地址为10.1.1.2、10.2.1.2的两台PC使用这两台服务器对外提供的服务。其他PC在任何时间都可以使用这两台服务器对外提供的服务。

![需求图](http://note.youdao.com/noteshare?id=11cddf2868147b58f52211475978f665)

在eNSP下的拓扑结构为

![eNSP拓扑图](http://note.youdao.com/noteshare?id=f04c4af7f0482c4b1f5e368a9067f482)

### 配置思路

本需求的访问控制涉及到限制源IP、目的IP及端口、时间段。为了好操作，需要提前配置好地址集、服务集和时间段，然后配置安全策略引用这些限制条件。

### 防火墙配置命令：

    配置GigabitEthernet 1/0/1 接口IP地址，将接口加入dmz域。
    <FW> system-view
    [FW] interface GigabitEthernet 1/0/1
    [FW-GigabitEthernet1/0/1] ip address 10.2.0.1 24
    [FW-GigabitEthernet1/0/1] quit
    [FW] firewall zone dmz
    [FW-zone-dmz] add interface GigabitEthernet 1/0/1
    [FW-zone-dmz] quit
    #配置GigabitEthernet 1/0/2接口IP地址，将接口加入trust域。
    [FW] interface GigabitEthernet 1/0/2
    [FW-GigabitEthernet1/0/2] ip address 10.1.1.1 24
    [FW-GigabitEthernet1/0/2] quit
    [FW] firewall zone trust
    [FW-zone-trust] add interface GigabitEthernet 1/0/2
    [FW-zone-trust] quit
    #配置GigabitEthernet 1/0/3接口IP地址，将接口加入trust域。
    [FW] interface GigabitEthernet 1/0/3
    [FW-GigabitEthernet1/0/3] ip address 10.2.1.1 24
    [FW-GigabitEthernet1/0/3] quit
    [FW] firewall zone trust
    [FW-zone-trust] add interface GigabitEthernet 1/0/3
    [FW-zone-trust] quit
    #配置名称为server_deny的地址集，将几个不允许访问服务器的IP地址加入地址集。
    [FW] ip address-set server_deny type object
    [FW-object-address-set-server_deny] address 10.1.1.2 mask 32
    [FW-object-address-set-server_deny] address 10.2.1.2 mask 32
    [FW-object-address-set-server_deny] quit
    #配置名称为time_deny的时间段，指定PC不允许访问服务器的时间。
    [FW] time-range time_deny
    [FW-time-range-time_deny] period-range 08:00:00 to 17:00:00 mon tue wed thu fri sat sun
    [FW-time-range-time_deny] quit
    #分别为Server1和Server2配置自定义服务集server1_port和server2_port，将服务器的非知名端口加入服务集。
    [FW] ip service-set server1_port type object
    [FW-object-service-set-server1_port] service protocol TCP source-port 0 to 65535 destination-port 8888
    [FW-object-service-set-server1_port] quit
    [FW] ip service-set server2_port type object
    [FW-object-service-set-server2_port] service protocol UDP source-port 0 to 65535 destination-port 6666
    [FW-object-service-set-server2_port] quit
    # 限制PC使用Server1对外提供的服务的安全策略
    [FW] security-policy
    [FW-policy-security] rule name policy_sec_deny1
    [FW-policy-security-rule-policy_sec_deny1] source-zone trust
    [FW-policy-security-rule-policy_sec_deny1] destination-zone dmz
    [FW-policy-security-rule-policy_sec_deny1] source-address address-set server_deny
    [FW-policy-security-rule-policy_sec_deny1] destination-address 10.2.0.10 32
    [FW-policy-security-rule-policy_sec_deny1] service server1_port
    [FW-policy-security-rule-policy_sec_deny1] time-range time_deny
    [FW-policy-security-rule-policy_sec_deny1] action deny
    [FW-policy-security-rule-policy_sec_deny1] quit
    # 限制PC使用Server2对外提供的服务的安全策略
    [FW-policy-security] rule name policy_sec_deny2
    [FW-policy-security-rule-policy_sec_deny2] source-zone trust
    [FW-policy-security-rule-policy_sec_deny2] destination-zone dmz
    [FW-policy-security-rule-policy_sec_deny2] source-address address-set server_deny
    [FW-policy-security-rule-policy_sec_deny2] destination-address 10.2.0.11 32
    [FW-policy-security-rule-policy_sec_deny2] service server2_port
    [FW-policy-security-rule-policy_sec_deny2] time-range time_deny
    [FW-policy-security-rule-policy_sec_deny2] action deny
    [FW-policy-security-rule-policy_sec_deny2] quit
    # 允许PC使用Server1对外提供的服务的安全策略
    [FW-policy-security] rule name policy_sec_permit3
    [FW-policy-security-rule-policy_sec_permit3] source-zone trust
    [FW-policy-security-rule-policy_sec_permit3] destination-zone dmz
    [FW-policy-security-rule-policy_sec_permit3] service server1_port
    [FW-policy-security-rule-policy_sec_permit3] action permit
    [FW-policy-security-rule-policy_sec_permit3] quit
    # 允许PC使用Server2对外提供的服务的安全策略
    [FW-policy-security] rule name policy_sec_permit4
    [FW-policy-security-rule-policy_sec_permit4] source-zone trust
    [FW-policy-security-rule-policy_sec_permit4] destination-zone dmz
    [FW-policy-security-rule-policy_sec_permit4] service server2_port
    [FW-policy-security-rule-policy_sec_permit4] action permit
    [FW-policy-security-rule-policy_sec_permit4] quit
    [FW-policy-security] quit
    —-结束
