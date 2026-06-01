import time
from openai import OpenAI
import pandas as panda
from dotenv import load_dotenv
import os
import re


def translate(llm_client: OpenAI, texts: list[str]) -> list[str]:
    translations = []
    numbered_texts = "\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))

    try:
        response = llm_client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the given text to Persian. "
                                              "Return ONLY the numbered translations, one per line, "
                                              "with no extra commentary."},
                {"role": "user", "content": numbered_texts}
            ]
        )
        result = response.choices[0].message.content.strip()
        lines = [line.strip() for line in result.split('\n') if line.strip()]

        for line in lines:
            match = re.match(r'^\d+[.):\s]+(.+)$', line)
            translations.append(match.group(1).strip() if match else line)

    except Exception as e:
        raise RuntimeError(f'Error in translate(): {e}')

    return translations


def translator() -> int:
    load_dotenv()
    client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=os.getenv('GAP_GPT_API'))

    df = panda.read_csv('../data/translated/translated_train.tsv', delimiter='\t', header=None)

    BATCH_SIZE = 10
    START_FROM = 7110
    source_col = df.columns[0]

    # Grab all row indices that still need translating
    pending = [i for i in df.index if i > START_FROM]

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch_indices = pending[batch_start : batch_start + BATCH_SIZE]
        texts = [str(df.at[i, source_col]) for i in batch_indices]

        print(f'Translating rows {batch_indices[0]}–{batch_indices[-1]} '
              f'({len(texts)} rows)...')

        try:
            translations = translate(llm_client=client, texts=texts)

            # Write each translation back to the correct row
            for idx, translation in zip(batch_indices, translations):
                df.at[idx, source_col] = translation

            df.to_csv('../data/translated/translated_train.tsv',
                      sep='\t', index=False, header=False)

            time.sleep(1)

        except Exception as e:
            raise RuntimeError(f'Batch starting at row {batch_indices[0]} failed: {e}')

    return 0


if __name__ == '__main__':
    translator()