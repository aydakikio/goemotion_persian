import time

from openai import OpenAI
import pandas as panda
from dotenv import load_dotenv
import os

def translate(llm_client: OpenAI, text: str) -> str:
    try:
        response = llm_client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the given text to Persian."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f'Error in translate(): {e}')


def translator() -> int:
    #loading environment variables
    load_dotenv()

    #loadin
    client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=os.getenv('GAP_GPT_API'))

    # Start reading the csv file
    df = panda.read_csv('../data/raw/raw_train.tsv', delimiter='\t')

    for index, row in df.iterrows():
        try:
            print(f'updating row {index}')
            source_text = row[df.columns[0]]
            df.at[index, df.columns[0]] = translate(llm_client=client, text=source_text)

            df.to_csv('../data/translated/translated_train.tsv', sep='\t', index=False)

            time.sleep(30)#sleep for 30 seconds

        except Exception as e:
            raise RuntimeError(f'Error on row {index}: {e}')

    return 0


if __name__ == '__main__':
    translator()