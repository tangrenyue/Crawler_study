import requests


def get_amazon(url):
    try:
        header = {'user-agent': 'Mozilla/5.0'}  # 定制请求头
        r = requests.get(url, headers=header, timeout=30)
        r.raise_for_status()  # 不是200则http_error
        r.encoding = r.apparent_encoding
        print(r.request.headers)  # 请求头
        print(r.headers)  # 响应头
        # print(r.content.decode('utf-8')) content返回的是字节，需要解码
        return r.text[:1000]
        # text返回的是unicode的字符串，可能会出现乱码情况
    except:
        return "爬取失败"


def main():
    url = "https://www.amazon.cn/dp/B06Y653D2Q"
    print(get_amazon(url))


if __name__ == "__main__":
    main()


'''
{'user-agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
{'Server': 'Server', 'Content-Type': 'text/html;charset=UTF-8'}
'''
