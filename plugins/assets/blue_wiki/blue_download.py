import os
import re
import requests

def download_images(url, save_path):
    # 发送请求获取网页内容
    response = requests.get(url,proxies={"http": "http://127.0.0.1:7890","https": "http://127.0.0.1:7890"})
    print("############")
    if response.status_code != 200:
        print("无法获取网页内容")
        return
    print(response.text)
    # 使用正则表达式匹配图片链接
    img_links = re.findall(r'([0-9]+\.png)', response.text)

    # 下载图片
    for img_link in img_links:
        img_url = f"{url}/{img_link}"
        img_save_path = os.path.join(save_path, img_link)

        # 下载图片
        response_img = requests.get(img_url)
        if response_img.status_code == 200:
            with open(img_save_path, 'wb') as f:
                f.write(response_img.content)
            print(f"已下载图片：{img_link}")
        else:
            print(f"无法下载图片：{img_link}")

print("**********")


website_url = "https://ba.gamekee.com/155086.html"
save_directory = "D:\\bot\\awesomebot\\awesomebot\\plugins\\assets\\blue_wiki"

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

download_images(website_url, save_directory)
