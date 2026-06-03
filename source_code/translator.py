import time
from openai import OpenAI
import pandas as panda
from dotenv import load_dotenv
import os
import re


MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds between retries


def translate(llm_client: OpenAI, texts: list[str]) -> list[str]:
    translations = []
    numbered_texts = "\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))

    try:
        response = llm_client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the given text to Persian. "
                                              "Return ONLY the numbered translations, one per line, "
                                              "with no extra commentary."
                                              "if you can't translate that return I can't translate."},
                {"role": "user", "content": numbered_texts}
            ]
        )

        # Gemini can return None content on filtered/blocked responses
        content = response.choices[0].message.content
        if content is None:
            finish_reason = response.choices[0].finish_reason
            raise RuntimeError(f'API returned None content (finish_reason={finish_reason!r})')

        result = content.strip()
        lines = [line.strip() for line in result.split('\n') if line.strip()]

        for line in lines:
            match = re.match(r'^\d+[.):\s]+(.+)$', line)
            translations.append(match.group(1).strip() if match else line)

    except RuntimeError:
        raise  # already formatted, pass it up
    except Exception as e:
        raise RuntimeError(f'Error in translate(): {e}')

    return translations


def translator() -> int:
    load_dotenv()
    client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=os.getenv('GAP_GPT_API'))

    df = panda.read_csv('../data/translated/translated_train.tsv', delimiter='\t', header=None)

    BATCH_SIZE = 10
    START_FROM = 43027
    source_col = df.columns[0]

    pending = [i for i in df.index if i > START_FROM]

    for batch_start in range(0, len(pending), BATCH_SIZE):
        batch_indices = pending[batch_start : batch_start + BATCH_SIZE]
        texts = [str(df.at[i, source_col]) for i in batch_indices]

        print(f'Translating rows {batch_indices[0]}–{batch_indices[-1]} '
              f'({len(texts)} rows)...')

        last_error = None
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                translations = translate(llm_client=client, texts=texts)

                for idx, translation in zip(batch_indices, translations):
                    df.at[idx, source_col] = translation

                df.to_csv('../data/translated/translated_train.tsv',
                          sep='\t', index=False, header=False)

                time.sleep(1)
                last_error = None
                break  # success, move to next batch

            except Exception as e:
                last_error = e
                print(f'  Attempt {attempt}/{MAX_RETRIES} failed: {e}')
                if attempt < MAX_RETRIES:
                    print(f'  Retrying in {RETRY_DELAY}s...')
                    time.sleep(RETRY_DELAY)

        if last_error is not None:
            # Write original texts back as a placeholder so the row isn't blank,
            # then continue rather than crashing the whole run
            print(f'  Skipping rows {batch_indices[0]}–{batch_indices[-1]} after {MAX_RETRIES} failed attempts.')
            print(f'  Rows left untouched. Log: {last_error}')
            # Optionally: write to a skip log
            with open('../data/translated/skipped_batches.log', 'a') as log:
                log.write(f'rows {batch_indices[0]}-{batch_indices[-1]}: {last_error}\n')

    return 0


if __name__ == '__main__':
    translator()