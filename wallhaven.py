import requests
from lxml import etree
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from tqdm import tqdm
import tqdm


proxies = {
    "http":"socks5://127.0.0.1:11223",
    "https":"socks5://127.0.0.1:11223"
}

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
            href_list.append(new_href)
          
        
def src_link():
    print("子页面总数",len(href_list)) 
    for src in href_list:
        src_resp = requests.get(url=src,headers=header,proxies=proxies)
        src_html = etree.HTML(src_resp.text)
        img = src_html.xpath("/html/body/main/section/div[1]/img/@src")
        for img_src in img:
            download_link.append(img_src)
    time.sleep(1)
    return
    
def  download():
    print("壁纸总数",len(download_link))
    for down in download_link:
        img_download = requests.get(down,headers=header,proxies=proxies,stream=True)
        img_name = down.split("/")[-1]
        pbar=tqdm.tqdm(unit='B',unit_scale=True,desc=img_name)
        with open("imgs/"+img_name,mode="wb") as f:
            for chunk in img_download.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(1024)
            pbar.close()   
            print("下载完成：",img_name)
            time.sleep(1)
        

if __name__ == '__main__':

    for i in range(1,3):
        func(url=f"https://wallhaven.cc/toplist?page={i}")
    with ThreadPoolExecutor(20) as t: 
        t.submit(src_link())
        t.submit(download()) 
    print("全部下载完成")
          
