'''
recognize the text from video and output to srt file.
'''
import os
import argparse
import whisper
import srtor_lib as lib


def _format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return (
        f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    )


def _get_segment(segment):
    s_id = segment['id'] + 1
    s_start = _format_timestamp(segment['start'])
    s_end = _format_timestamp(segment['end'])
    s_en_text = segment['text'].strip().replace("-->", "->")
    return f"{s_id}\n{s_start} --> {s_end}\n{s_en_text}\n"


def _get_srt_txt(result):
    segments = result['segments']
    txt = ''.join([f'{_get_segment(seg)}\n' for seg in segments])
    return txt


def _recognize_srt(file_path: str, output_path: str):
    model = whisper.load_model('base')
    result = model.transcribe(file_path, fp16=False)
    srt_txt = _get_srt_txt(result)
    with open(output_path, "w", encoding="utf-8") as wf:
        wf.write(srt_txt)


def _recognize_all(path):
    for root, _, files in os.walk(path):
        for file_name in files:
            is_file, file_path, output_path = lib.get_file_info(
                files=files, file_name=file_name, root=root,
                sufs=lib.WHISPER_SUFS)
            if not is_file:
                continue
            print(f'start transcribing "{file_path}".')
            _recognize_srt(file_path, output_path)
            print('done.')
    print('all transcribed.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--folder_path', type=str, required=True)
    args = parser.parse_args()
    _recognize_all(args.folder_path)
