from bs4 import BeautifulSoup
import urllib.request
import traceback
import sys
def Start(url, link, depth, is_link):

    if link == '':
        links, static_files = Get_links(url)
        print('Проверка - ' + url + '\n --------------------')
        Check(url, links, static_files, depth-1, is_link)
        print('\n --------------------')
    else:
        print('Проверка - ' + link + '\n --------------------')
        links, static_files = Get_links(url+link)
        Check(url, links, static_files, depth-1, is_link)
        print('\n --------------------')
        
def Get_links(url):
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser')
    static_files = []
    links = []
    
    
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    static_files.append('dlya_oshibki')   
    for link in soup.find_all('link', href=True):
        static_files.append(link['href'])
       
    for link in soup.find_all('img', src=True):
        static_files.append(link['src'])
        
    for link in soup.find_all('script', src=True):
        static_files.append(link['src'])
    
    return links, static_files;
    

def Check(url,links, static_files, depth, is_link):
    print('(STATIC):')       
    for link in static_files:
        try:
            if ('https://' in link) or ('.com' in link):
                resp = urllib.request.urlopen(link)
            else:
                resp = urllib.request.urlopen(url + link)
            print(link + '(Успешно)')     
        

        except Exception as err:
            print(link+ " (Ошибка - {0})".format(err))
    
    print('(LINKS):')
    for link in links:
        try:
            if '.html' in link:
                resp = urllib.request.urlopen(url + link)
            else:
                resp = urllib.request.urlopen(link)
            print(link + '(Успешно)')
            
            
            if depth != 0 and ('.html' in link):
                Start(url, link, depth, is_link)
            if depth != 0 and is_link =='-e' and ('.html' not in link):
      
                Start(link, '', depth, is_link)

        except Exception as err:
            print(link+ " (Ошибка - {0})".format(err))
            


    
if '__main__':
    try:

        par = ['-e','-i']


        if int(sys.argv[2])>0 and (sys.argv[3] in par):
            Start(sys.argv[1],'', int(sys.argv[2]), sys.argv[3])
        elif int(sys.argv[2])<1:
            print('Глубина должна быть > 0')
        else:
            print('''Введите: 
                  -e, проверить внешние и внутренние ссылки
                  -i, только внутренние
                  ''')

    except Exception as err:
        print(" (Ошибка - {0})".format(err))
        print('Не правельно введены параметры \n (ссылка на сайт) (глубина проверки > 0) (выбор проверки внешних и внутренних ссылок)')

        
    
    
