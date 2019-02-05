import os

import requests


# 爬取网上的图片、视频、动画等http://xxx.jpg/x.mp4/xxx.mp3
def get_picture(url, root, path):
    try:
        # 文件夹不存在则新建一个
        if not os.path.exists(root):
            os.mkdir(root)
        # 文件不存在则保存，存在则打印‘已存在’
        if not os.path.exists(path):
            r = requests.get(url)
            # with打开一个文件，然后把爬取到的内容（2进制）写进这个文件中，r.content表示返回内容的2进制形式
            with open(path, 'wb') as f:
                # 将返回的二进制图片数据写进文件中
                f.write(r.content)
                f.close()
                print('文件保存成功！')
        else:
            print('文件已经存在！')
    except:
        print('爬取失败')


def main():
    url = "http://img.lanrentuku.com/img/allimg/1609/147479906785.jpg"
    root = "/Users/tang/Pictures/"  # /
    path = root + url.split('/1609/')[-1]
    get_picture(url, root, path)


if __name__ == '__main__':
    main()
