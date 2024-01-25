import scrapy

def build_link(i):
    '''
    Build the XPath for the link based on the index.
    
    Args:
        i (int): Index of the article.
    
    Returns:
        str: XPath for the link.
    '''
    return '/html/body/div[1]/div[4]/main/div[3]/div/div[2]/article[{}]/h2/a/@href'.format(i)


class GithubTrendingSpider(scrapy.Spider):
    '''
    Spider to crawl GitHub trending page and extract links.
    '''
    name = 'github_trending'
    start_urls = ['https://github.com/trending']

    # by default, GitHub will give us 25 results in the trending tab.
    def parse(self, response):
        '''
        Parse the response and extract the links.
        
        Args:
            response (scrapy.http.Response): The response received from the request.
        '''
        link_list = list()
        for x in range(1, 26):
        
            link = response.xpath(build_link(x)).getall()
        
            yield {
                'link': link
            }

            link_list.append(link[0])
        
        print(link_list)
        
        with open('output.txt', 'w') as file:
            # trick to avoid the last iteration to write \n in our output file.
            for x in range(len(link_list)):
                if x+1 != len(link_list): # checking if we are in the last iteration
                    file.write(link_list[x] + '\n')
                else: # if we are, just write the link with no newline at the end.
                    file.write(link_list[x])

