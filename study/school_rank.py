import requests
from bs4 import BeautifulSoup
import bs4


# 获取html页面
def get_HTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"


# 将html页面放到list列表中
def fill_UnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    # 查找tbody标签然后，下行遍历，只遍历儿子节点（tr）。tr标签是行，这里是一所大学的信息。
    for tr in soup.find("tbody").children:
        # tbody的儿子节点可能有tr标签和字符串类型（字符串类型也是节点），这里所有信息都在tr标签中，这里需要过滤掉非标签类型的信息
        # 这里需要import bs4，检测循环遍历tr的类型，若不是bs4库定义的标签类型则过滤掉
        if isinstance(tr, bs4.element.Tag):
            # 对tr标签中的td标签做查询，存为列表类型tds = tr.find_all("td")
            tds = tr('td')  # find_all()的简写
            # 将排名、大学名称、大学排分加进列表
            ulist.append([tds[0].string, tds[1].string, tds[3].string])


def print_UnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    # 大学信息打印，格式和表头一致
    print(tplt.format("排名", "学校名称", "总分", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))


def main():
    # 将大学信息放进uinfo列表中
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    # 调用3个步骤对应的函数,将URL转换为html
    html = get_HTMLText(url)
    fill_UnivList(uinfo, html)
    print_UnivList(uinfo, 20)  # 这里选取20所学校信息


if __name__ == '__main__':
    main()

