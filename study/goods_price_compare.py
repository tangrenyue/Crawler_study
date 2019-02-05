# 现在要登录才能爬商品info，借鉴思路

import requests
import re
import time


# 获取html页面
def get_HTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # "utf-8" 可以节约时间
        return r.text
    except:
        return "error"


# 对获取的每一个页面进行解析,ilt是结果的列表类型
def parse_page(ilt, html):
    try:
        # "view_price":"149.00" 反斜杠\表示引入双引号，获取价格信息保存到plt中
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        # "raw_title":"2017春季新款双肩包女韩版时尚pu背包流苏子母包百搭学院风书包"
        # *?是最小匹配
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        # 获取了商品的价格和信息，下面对这两个信息关联起来，保存到我们要输出的变量中
        # plt\tlt列表长度一样，元素位置一一对应的，同一个位置的元素是同一个商品的
        for i in range(len(plt)):
            # 字符串分割获取商品的价格，eval()函数能够将字符串的最外层的双引号或单引号去掉
            price = eval(plt[i].split(':')[1])
            # 获得商品名称
            title = eval(tlt[i].split(":")[1])
            # 将信息需要输出的列表中
            ilt.append([price, title])
    except:
        print("parse error")


# 将解析后的信息输出
def print_goods_price_compare(ilt):
    # 先设计一个打印模板tplt，希望打印什么格式,
    # {}定义槽函数，{:4}第一个位置长度为4，中间8，最后是16
    tplt = "{:4}\t{:8}\t{:16}"
    # 打印输出信息的表头
    print(tplt.format("序号", "价格", "商品名称"))
    # 定义一个输出信息计数器,商品序号
    count = 0
    # 对所有的信息进行输出显示
    for g in ilt:
        count += 1
        # 序号，价格，名称
        print(tplt.format(count, g[0], g[1]))


# 定义主函数，记录整个程序运行的过程
def main():
    start_time = time.time()
    # 搜索关键词goods
    goods = "书包"
    # 设定向下一页爬取的深度，爬取页数depth
    depth = 3
    # 爬取的URL
    start_url = "https://s.taobao.com/search?q=" + goods
    # 定义变量infoList 表示输出结果
    infoList = []
    # 因为每一个页面URL不同，需要对每一个页面进行单独访问和处理
    for i in range(depth):
        try:
            # 使用try多获取页面进行异常判断，如果某页面解析出问题，可以跳过该页面，往下继续，不会造成出现解析错误，程序停止
            # 对每一个页面的URL链接进行设计,因为淘宝每个页面显示44个商品
            url = start_url + '&s=' + str(44 * i)
            html = get_HTMLText(url)  # 获取页面内容
            parse_page(infoList, html)  # 对获取的页面进行处理
        except:
            # continue语句只是结束本次循环，而不会终止循环的执行。break语句则是终止整个循环过程
            continue
    # 将获取的页面信息输出
    print_goods_price_compare(infoList)
    end_time = time.time()
    print(end_time - start_time)


if __name__ == '__main__':
    main()


