import requests
import re
from bs4 import BeautifulSoup


# 获得URL对应的页面
def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return "get e"


# 获得股票的信息列表,lst是保存所有股票的列表,stockURL是获得股票列表的URL网站
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, "GB2312")  # 获取东方财富网的html
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find_all('a')  # 通过find_all()获得页面的a标签，a是一个列表
    for i in a:
        try:
            # 异常处理：代码中有很多不是股票链接的a标签的，解析可能出现错误
            href = i.attrs["href"]
            # 以s开头中间是h或z后面是6个数字的正则
            lst.append(re.findall(r'[sh][sz]\d{6}', href)[0])  # 可以找到所有的股票URL
        except:
            continue


# 获得每一只个股的股票信息,lst是保存所有股票的列表;stockURL是获得股票列表的URL网站;股票信息保存的文件路径
def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, "html.parser")
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})
            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                value = valueList[i].text
                infoDict[key] = value
            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'  # 获得股票列表
    stock_info_url = 'https://gupiao.baidu.com/stock/'  # 获取股票信息的链接的主题部分
    output_file = '/Users/tang/Pictures/stock_info.txt'  # 保存的路径
    slist = []  # 股票信息，列表
    getStockList(slist, stock_list_url)  # 获得股票列表
    getStockInfo(slist, stock_info_url, output_file)  # 获得每一只股票信息，保存到本地


if __name__ == '__main__':
    main()