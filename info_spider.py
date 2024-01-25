import scrapy
import requests
import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

class GithubInfoSpider(scrapy.Spider):
    '''
    Spider to crawl GitHub trending page and extract links.
    '''
    name = 'github_info'

    link_list = []
    with open('output.txt', 'r') as file:
        for line in file:
            link_list.append('https://github.com'+line.rstrip('\n'))

    start_urls = link_list

    def parse(self, response):
        description_list = list()
        about = '/html/body/div[1]/div[4]/div/main/turbo-frame/div/div/div/div[2]/div[2]/div/div[1]/div/div/p'


        '''
        Parse the response and extract the links.
        
        Args:
            response (scrapy.http.Response): The response received from the request.
        '''
   
        description = response.xpath(about).getall()

        try:
            description[0]
        except IndexError as e:
            return


        description = remove_tags(description[0].rstrip())
        description = re.sub(r"[\n\t]*", "", description).strip()
        yield {
            'description': description
        }
        description_list.append(description)
        
        print(description_list)

        response = requests.get(readme_uri)

        print(response.text)
    


