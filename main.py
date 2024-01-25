# scrapy scripts
'''
from trending_spider import main as run_trending_spider
from info_spider import main as run_info_spider
'''

import json
from nltk.tokenize import word_tokenize
import re

# python scripts
from readme_reader import main as run_readme_reader
from summarize_llm import main as run_summarizer

def count_tokens(data: str = "") -> None:
    print('*******{}*******'.format(len(word_tokenize(data))))
    return len(word_tokenize(data))



def preprocess_string(data: str) -> None:
    #processed_str = data.decode('utf8').encode('ascii', errors='ignore')
    processed_str = re.sub(r'[^\x00-\x7f]',r'', data)
    processed_str = re.sub(r'<.*?>',r'', data)
    encoded_str = processed_str.encode("ascii", "ignore")
    string_decode = encoded_str.decode()
    return string_decode

#
#The listed limit is 4096 for input + output. Meaning, you need to save some token space for  the LLM to output a response.
#https://docs.oracle.com/en-us/iaas/Content/generative-ai/limitations.htm

def main():
    readme_list = run_readme_reader()
    print('Obtained {} README records'.format(len(readme_list)))

    iterator = 1
    for x in readme_list:
        new_text = preprocess_string(x)

        '''with open('local_file.txt', 'w') as file:
            file.write(new_text)
        file.close()'''

        if (len(new_text)) < 250:
            print('Skipping iteration as it does not have enough data to summarize')
            iterator += 1
            continue

        print('Text length: {}'.format(len(x)))
        print('Text length: {}'.format(len(new_text)))
        if len(new_text) > 10000:
            new_text = new_text[0:10000]
        else: new_text = new_text
        print('Text length: {}'.format(len(new_text)))
        summary = run_summarizer(new_text)
        print(json.loads(str(summary))['summary'])

        with open('outputs/output_{}.txt'.format(iterator), 'w') as file:
            file.write(json.loads(str(summary))['summary'])
        file.close()
        
        iterator += 1


if __name__ == '__main__':
    main()
