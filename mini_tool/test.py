from decimal import * #导入小数位数控制模块

def password(a,b,x,y):

    #设定小数位数为y位

    getcontext().prec = y

    #通过Decimal()来计算长浮点数

    m = Decimal(a) / Decimal(b)

    #把结果转换成为字符串格式

    m = str(m)

    #定义一个空列表

    list = []

    #定义结果的连字符

    s = ''

    #判定：如果结果的位数不够，补足零

    if len(m) < y + x + 2:

        #定义内容为0的空列表

        o = []

        #需要添加多少个0,需要添加至少y个零，因为假设第2位到第5位，若除数结果为2.0，添加5个0，才能取到最终结果个0

        for i in range(y):

            #把0添加到o列表中

            o.append('0')

        #把m转换为列表

        m = [i for i in m]

        #两个列表相加

        m.extend(o)

    #取列表中的小数点后x位到y位的数字

    for i in range(x + 1, y + 2):

        if m[i]:

            list.append(m[i])

    #输出列表，用jion函数

    print s.join(list)





password(1,2,2,5)

