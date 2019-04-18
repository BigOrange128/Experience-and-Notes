import time

user_name = 'didi'
user_passwd = '12345'


commodity = (
    ('肥仔快乐水', 200), ('肥仔快乐面', 90),
    ('肥仔快乐糖', 60), ('肥仔大礼包', 500),
)
user_money = 0
user_commodity = []
while 1:
    print('测试账号：{}\n测试密码：{}\n退出方式：q或Q'.format(user_name, user_passwd))
    in_name = input("欢迎来到肥仔商店, 请输入您的账号！\n")
    if in_name == 'q' or in_name == 'Q':
        print("欢迎下次光临！")
        exit()
    in_passwd = input('输入您的密码!\n')
    if in_passwd == 'q' or in_passwd == 'Q':
        print("欢迎下次光临！")
        exit()
    if in_name != user_name or in_passwd != user_passwd:
        print('用户名或密码错误!\n')
    else:
        while 1:
            try:
                user_money = input('欢迎*{}*登录，请输入您的购物卡金额!\n'.format(user_name))
                user_money = int(user_money)
            except ValueError:
                print('购物卡金额应为数字,请重新输入!')
                continue
            while 1:
                print('---------商品清单----------')
                print('序号      商品名     价格')
                for index, i in enumerate(commodity):
                    print('{}      {}      ￥{}'.format(index, i[0], i[1]))
                print('---------------------------')
                in_shopping = input("请输入您要购买的商品序号!\n")
                if in_shopping == 'q' or in_shopping == 'Q':
                    if user_commodity:
                        print('---------购买清单----------')
                        print('商品名          价格')
                        for i in user_commodity:
                            print('{}       {}'.format(i[0], i[1]))
                        print('---------------------------')
                    print('您的余额为', user_money)
                    print('您即将退出系统！')
                    print("欢迎下次光临！")
                    time.sleep(3)
                    exit()
                else:
                    try:
                        in_shopping = int(in_shopping)
                        if commodity[in_shopping][1] < user_money:
                            print('您已成功购买{}！'.format(commodity[in_shopping][0]))
                            user_money = user_money - commodity[in_shopping][1]
                            user_commodity.append(commodity[in_shopping])
                            print('余额剩余：{}'.format(user_money))
                        else:
                            print('余额不足！')
                    except (ValueError, IndexError) as e:
                        print('输入有误！请重新选择！')
