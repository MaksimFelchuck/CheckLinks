from bs4 import BeautifulSoup
import urllib.request

def Get_links(url):
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser')
    static_files = []
    links = []
    
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    static_files.append('dlya_oshibki')   
    for link in soup.find_all('link', href=True):
        links.append(link['href'])
       
    for link in soup.find_all('img', src=True):
        static_files.append(link['src'])
        
    for link in soup.find_all('script', src=True):
        static_files.append(link['src'])
    
    Check(url, links, static_files)
    

def Check(url, links, static_files):
    for link in links:
        try:
            resp = urllib.request.urlopen(url)
            print(link + '  -Успешно')
        except:
            print(link+ '   -404 File not found')
            
    for link in static_files:
        try:
            resp = urllib.request.urlopen(url+link)
            print(link + '  -Успешно')
        except:
            print(link+ '   -404 File not found')
    
if '__main__':
    url = input('Введите ссылку на сайт: ')
    links = Get_links(url)
    
    
