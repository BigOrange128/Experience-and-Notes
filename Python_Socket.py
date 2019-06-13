'''
server:
1.创建套接字，绑定套接字到ip与端口
2.开始监听连接
3.进入循环，不断接受客户端的连接请求
4.接受传来的数据，并发送给对方数据
5.传输完毕后，关闭套接字
'''
import socket

server = socket.socket()
server.bind(('127.0.0.1', 1234))
server.listen(5)

while True:
    print('waiting for client...')
    conn, addr = server.accept()
    print("client is coming from {}".format(addr[0]))
    cli_into = conn.recv(1024)

    print("client info:{}".format(cli_into.decode(  )))
    conn.send(cli_into.upper())
server.close()
'''
client:
1.创建套接字，连接远端地址
2.连接后发送数据和接受数据
3.传输完毕后，关闭套接字
'''
import socket

while True:
    client = socket.socket()
    client.connect(('localhost', 1234))
    message = input("您要发送什么消息？(退出请按q)\n")
    if message == 'q':
        print("再见！")
        break
    client.send('{}'.format(message).encode('utf-8'))
    data = client.recv(1024)
    print(data.decode('utf-8'))
client.close()
