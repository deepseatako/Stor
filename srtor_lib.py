'''
library.
'''

import os

MP4 = '.mp4'
MKV = '.mkv'
VVT = '.vtt'
SRT = '.srt'
CN_SRT = '.cn.srt'
EN_SRT = '-en.srt'


class _Sufs:
    def __init__(self, load_sufs, save_sufs, output_suf):
        self.load_sufs = load_sufs
        self.save_sufs = save_sufs
        self.output_suf = output_suf


SRT_SUFS = [f'{MP4}{SRT}', EN_SRT, SRT, VVT]
WHISPER_SUFS = _Sufs(load_sufs=[MP4, MKV],
                     save_sufs=SRT_SUFS,
                     output_suf=SRT)
TRANS_SUFS = _Sufs(load_sufs=SRT_SUFS,
                   save_sufs=[CN_SRT],
                   output_suf=CN_SRT)


def is_file_exist(base_name: str, search_sufs: list[str], files: list[str]):
    '''
    if file exist.
    '''
    search_files = [f'{base_name}{suf}' for suf in search_sufs]
    if any(s_file in files for s_file in search_files):
        return True
    return False


def get_file_info(files: list[str], file_name: str, root: str,
                  sufs: _Sufs):
    '''
    get file info.
    '''
    c_load_suf = None
    for load_suf in sufs.load_sufs:
        if file_name.endswith(load_suf):
            c_load_suf = load_suf
            break
    if c_load_suf is None:
        return False, None, None
    if any(file_name.endswith(save_suf) for save_suf in sufs.save_sufs):
        return False, None, None
    base_file_name = file_name[:-len(c_load_suf)]
    output_file_name = f"{base_file_name}{sufs.output_suf}"
    if is_file_exist(base_file_name, sufs.save_sufs, files):
        return False, None, None
    file_path = os.path.join(root, file_name)
    output_path = os.path.join(root, output_file_name)
    return True, file_path, output_path
