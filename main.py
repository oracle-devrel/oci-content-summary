# scrapy scripts
'''
from trending_spider import main as run_trending_spider
from info_spider import main as run_info_spider
'''

import json
from nltk.tokenize import word_tokenize
import re
import yaml
from db_handler import DatabaseHandler

# python scripts
from readme_reader import main as run_readme_reader
from summarize_llm import main as run_summarizer

def count_tokens(data: str = "") -> None:
    print('*******{}*******'.format(len(word_tokenize(data))))
    return len(word_tokenize(data))

def preprocess_string(data: str) -> None:
    processed_str = re.sub(r'[^\x00-\x7f]',r'', data)
    processed_str = re.sub(r'<.*?>',r'', data)
    encoded_str = processed_str.encode("ascii", "ignore")
    string_decode = encoded_str.decode()
    return string_decode

def main():
    # Load database configuration
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Initialize database connection
    db = DatabaseHandler(
        username=config['db_username'],
        password=config['db_password'],
        dsn=config['db_dsn']
    )
    db.connect()

    try:
        readme_list = run_readme_reader()
        print('Obtained {} README records'.format(len(readme_list)))

        iterator = 1
        for x in readme_list:
            new_text = preprocess_string(x)

            if (len(new_text)) < 250:
                print('Skipping iteration as it does not have enough data to summarize')
                iterator += 1
                continue

            print('Text length: {}'.format(len(x)))
            print('Text length: {}'.format(len(new_text)))
            if len(new_text) > 10000:
                new_text = new_text[0:10000]
            else: 
                new_text = new_text
            print('Text length: {}'.format(len(new_text)))
            
            summary = run_summarizer(new_text)
            print(summary)

            # Save to file
            output_file = f'outputs/output_{iterator}.txt'
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(summary)

            # Save to database
            db.insert_summary(
                summary_text=summary,
                daily_position=iterator,
                file_path=output_file
            )
            
            iterator += 1

    finally:
        db.close()

if __name__ == '__main__':
    main()
