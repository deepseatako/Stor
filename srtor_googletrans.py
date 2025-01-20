'''
translate all file under the folder.
'''
import os
import argparse
import pysrt
from googletrans import Translator
from tqdm import tqdm
from httpcore._exceptions import TimeoutException, ConnectError
import srtor_lib as lib


class _Translator:
    def _translate_en2cn(self, en_txt: str):
        translator = Translator()
        while True:
            try:
                cn_txt = translator.translate(
                    en_txt, src='en', dest='zh-cn').text
            except IndexError:
                en_txt = en_txt.replace('.', '. ')
                cn_txt = translator.translate(
                    en_txt, src='en', dest='zh-cn').text
                cn_txt = cn_txt.replace('。', '.')
            except (TimeoutException, ConnectError):
                self._pbar.write('error. try to translate again.')
                continue
            break
        return cn_txt

    def translate(self):
        '''
        output str file.
        '''
        subs = pysrt.open(self._file_path)
        self._pbar = tqdm(total=len(subs), ncols=0)
        srt_file = ''
        for sub in subs:
            text_en = sub.text
            text_cn = self._translate_en2cn(text_en)
            sub.text = f'{text_cn}\n{text_en}'
            srt_file += f'{str(sub)}\n'
            self._pbar.update(1)
        self._pbar.close()
        with open(self._output_path, "w", encoding="utf-8") as wf:
            wf.write(srt_file)

    def __init__(self, file_path: str, output_path: str):
        self._pbar = None
        self._file_path = file_path
        self._output_path = output_path


def _translate_all(folder_path):
    for root, _, files in os.walk(folder_path):
        all_files = files
        for file_name in files:
            is_file, file_path, output_path = lib.get_file_info(
                files=all_files, file_name=file_name, root=root,
                sufs=lib.TRANS_SUFS)
            if not is_file:
                continue
            print(f'start translating "{file_path}".')
            _Translator(file_path=file_path,
                        output_path=output_path).translate()
            all_files.append(os.path.basename(output_path))
            print('done.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--folder_path', type=str, required=True)
    args = parser.parse_args()
    _translate_all(args.folder_path)
