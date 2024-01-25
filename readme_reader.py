import requests
import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)


def main() -> None:

    markdown_list = []
    with open('output.txt', 'r') as file:
        for line in file:
            line = line.rstrip('\n').strip()

            markdown_url = '{}{}{}'.format(
                'https://raw.githubusercontent.com',
                line,
                '/master/README.md'
            ) 
            markdown_list.append(markdown_url)


    #print('Markdown List: {}'.format(markdown_list))
    readme_list = list()
    for x in markdown_list:
        response = requests.get(x)
        #print(response.txt)
        readme_txt = response.text
        readme_list.append(readme_txt)
    # return all TXTs obtained
    return readme_list



if __name__ == '__main__':
    main()
