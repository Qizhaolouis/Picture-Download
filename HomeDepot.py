
# coding: utf-8

# In[10]:


import os
import requests
import time
from bs4 import BeautifulSoup

class Homedepot_search():
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.sleep_time = 2
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        self.max_page = 7
        self.timeout = 10
        
    def get_homedepot_html_first_page(self, tool):
        url = 'https://www.homedepot.com/b/N-5yc1v/Ntk-semanticsearch/Ntt-{search_term}?NCNI-5'
        response = requests.get(url.format(search_term = tool),headers= self.header, timeout = self.timeout)
        content = response.content
        time.sleep(self.sleep_time)
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    
    def get_homedepot_html(self, tool, page):
        url = 'https://www.homedepot.com/b/N-5yc1v/Ntk-semanticsearch/Ntt-{search_term}?NCNI-5&Nao={number}&Ns=None'
        response = requests.get(url.format(search_term = tool, number = page*24),headers= self.header, timeout = self.timeout)
        content = response.content
        time.sleep(self.sleep_time)
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    
    def get_last_page(self, soup):
        page_numbers = list(map(lambda x: x.text.replace(',',''), soup.findAll('a',{'class':'hd-pagination__link'})))
        page_numbers = [int(number) for number in page_numbers if number != '']
        if len(page_numbers) == 0:
            return 1
        last_page = max(page_numbers)
        return last_page
    
    def get_pic_links(self, soup):
        links = list(map(lambda x: x['src'], soup.findAll('img')))
        links = [link for link in links if ("http" in link and 'jpg' in link)]
        return links
    
    def download_pictures(self, links, tool): 
        folder = self.path + tool
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            print('already downloaded {0}'.format(tool))
            return 0
        for i in range(len(links)):
            Picture_request = requests.get(links[i])
            if Picture_request.status_code == 200:
                with open(folder + "/image" + str(i) + ".jpg", 'wb') as f:
                    f.write(Picture_request.content)
        return folder
    
    def download_from_homedepot(self, tool):
        soup = self.get_homedepot_html_first_page(tool)
        last_page = self.get_last_page(soup)
        links = self.get_pic_links(soup)
        print('Already gotten {0} links'.format(len(links)))
        if last_page == 1:
            self.download_pictures(links)
            print('Finished {0}'.format(tool))
            return None
        if last_page > self.max_page:
            last_page = self.max_page
        for page in range(1,last_page):
            soup = self.get_homedepot_html(tool, page)
            links += self.get_pic_links(soup)
            print('Already gotten {0} links'.format(len(links)))
        self.download_pictures(links, tool)
        print('Finished {0}'.format(tool))
        return None

if __name__ == '__main__':
    homedepot_search = Homedepot_search()
    homedepot_search.download_from_homedepot('hammer')

