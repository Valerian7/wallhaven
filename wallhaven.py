import requests
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
import tqdm

proxies = {
    "http":"socks5://127.0.0.1:11223",
    "https":"socks5://127.0.0.1:11223"
}
requests.adapters.DEFAULT_RETRIES = 5
header = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

href_list = []
download_link = []

def func(url):
    resp = requests.get(url,headers=header,proxies=proxies)
    html = etree.HTML(resp.text)
    divs = html.xpath("/html/body/main/div[1]")
    for i in divs:
        href = i.xpath("./section/ul/li/figure/a/@href")
        for new_href in href:
#            print("获取子页面：",new_href)
            href_list.append(new_href)
    time.sleep(1)
          
        
def src_link(src):
    s = requests.session()
    s.keep_alive = False
    src_resp = s.get(url=src,headers=header,proxies=proxies)
    src_html = etree.HTML(src_resp.text)
    img = src_html.xpath("/html/body/main/section/div[1]/img/@src")
    for img_src in img:
        download_link.append(img_src)
#            print("获取壁纸下载链接：",img_src)
    time.sleep(1)
      
    
def  download(down): 
    img_download = requests.get(down,headers=header,proxies=proxies,stream=True)
    img_name = down.split("/")[-1]
    pbar = tqdm.tqdm(unit='B',unit_scale=True,desc="正在下载："+img_name)
    with open("python爬虫学习笔记/wallhaven/imgs/"+img_name,mode="wb") as f:
        for chunk in img_download.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    f.close
    time.sleep(1)


if __name__ == '__main__':
#    for i in range(2,10):
#        func(f"https://wallhaven.cc/toplist?page={i}")
    print("正在爬取子页面...")
    for i in range(5,7):
        func(url=f"https://wallhaven.cc/toplist?page={i}")
    with ThreadPoolExecutor(20) as t: 
        print("子页面总数",len(href_list))
        print("正在爬取壁纸下载链接...") 
        for srclink in href_list:
            t.submit(src_link(src=srclink))
    with ThreadPoolExecutor(20) as m:
        print("壁纸总数",len(download_link))
        print("正在下载壁纸...")
        for down in download_link:
            m.submit(download,down)     
    print("全部下载完成")
