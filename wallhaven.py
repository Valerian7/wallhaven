import requests
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor,as_completed

proxies = {
    "http":"socks5://127.0.0.1:11223",
    "https":"socks5://127.0.0.1:11223"
}
href_list = []
download_link = []
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def func(url):
    resp = requests.get(url,headers=header,proxies=proxies)
    html = etree.HTML(resp.text)
    divs = html.xpath("/html/body/main/div[1]")
    for i in divs:
        href = i.xpath("./section/ul/li/figure/a/@href")
        for new_href in href:
            print("获取子页面：",new_href)
            href_list.append(new_href)
    src_link()
        
        
def src_link():
    for src in href_list:
        src_resp = requests.get(url=src,headers=header,proxies=proxies)
        src_html = etree.HTML(src_resp.text)
        img = src_html.xpath("/html/body/main/section/div[1]/img/@src")
        for img_src in img:
            download_link.append(img_src)
            print("获取壁纸下载链接：",img_src)
    download()
    
def  download():
    for down in download_link:  
        img_download = requests.get(down,headers=header,proxies=proxies)
        img_name = down.split("/")[-1]
        with open("python爬虫学习笔记/wallhaven/imgs/"+img_name,mode="wb") as f:
            f.write(img_download.content)
            print("下载完成：",img_name)
            time.sleep(1)

if __name__ == '__main__':
    for i in range(2,10):
        func(f"https://wallhaven.cc/toplist?page={i}")


'''

    executor = ThreadPoolExecutor(max_workers=50)
    urls = []
    for i in range(2,25):
        url = f"https://wallhaven.cc/toplist?page={i}" 
        urls.append(url)
    for data in executor.map(func,urls):
        print("任务{} 下载完成".format(data))       
    print("全部下载完成")
'''
