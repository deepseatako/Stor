import os
import argparse
import asyncio
import pysubs2
from googletrans import Translator
import srtor_lib as lib
from colorama import init, Fore

BATCH_SIZE = 1000  # Set the batch size for translation
MAX_CONCURRENT_FILES = 10  # Maximum number of files to process concurrently


async def translate_bulk(texts):
    """
    Asynchronously translates a list of texts.
    """
    async with Translator() as translator:
        tasks = [translator.translate(text, dest='zh-cn') for text in texts]
        results = await asyncio.gather(*tasks)
        return [result.text for result in results]


async def translate_en2cn(texts):
    """
    Translates multiple English texts into Chinese using async API.
    """
    error_times = 0
    while True:
        try:
            cn_texts = await translate_bulk(texts)
        except Exception as e:  # pylint: disable=W0718
            error_times += 1
            print(f'Error: {e}')
            print('Retrying translation...')
            continue
        break
    return cn_texts


async def translate(file_path, output_path):
    """
    Loads subtitles, translates them in batches asynchronously,
    and saves the translated subtitles.
    """
    subs = pysubs2.load(file_path)

    texts_en = [sub.text for sub in subs]
    translated_texts = []

    for i in range(0, len(texts_en), BATCH_SIZE):
        batch = texts_en[i: i + BATCH_SIZE]
        translated_batch = await translate_en2cn(batch)
        translated_texts.extend(translated_batch)

    for sub, text_cn in zip(subs, translated_texts):
        sub.text = f'{text_cn}\n{sub.text}'

    subs.save(output_path)


async def translate_file(file_path, output_path, semaphore):
    """
    Translates a single file with concurrency control.
    """
    async with semaphore:
        print(f'Start translating "{file_path}".')
        await translate(file_path=file_path, output_path=output_path)
        print(f'{Fore.GREEN}Done translating "{file_path}".')


async def translate_all(folder_path):
    """
    Iterates through all files in the folder and translates subtitles concurrently.
    """
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_FILES)
    tasks = []

    for root, _, files in os.walk(folder_path):
        all_files = files
        for file_name in files:
            is_file, file_path, output_path = lib.get_file_info(
                files=all_files, file_name=file_name, root=root, sufs=lib.TRANS_SUFS
            )
            if not is_file:
                continue

            tasks.append(translate_file(file_path, output_path, semaphore))

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    init(autoreset=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--folder_path', type=str, required=True)
    args = parser.parse_args()

    asyncio.run(translate_all(args.folder_path))
