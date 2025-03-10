import requests
from bs4 import BeautifulSoup

def simple_crawler(url):
    """
    一個簡單的爬蟲函數

    Args:
        url (str): 要爬取的網頁網址

    Returns:
        str: 解析後的網頁內容
    """

    # 發送請求，獲取網頁內容
    response = requests.get(url)
    response.encoding = 'utf-8'  # 設定編碼，避免亂碼

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取所需內容 (這裡以提取所有標題為例)
    titles = soup.find_all('title')
    for title in titles:
        print(title.text)

    return soup

if __name__ == '__main__':
    url = 'https://www.bbc.com'  # 替換成你要爬取的網址
    simple_crawler(url)