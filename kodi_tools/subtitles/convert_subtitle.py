import chardet
import os
import sys


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']


def convert_subtitle(file_path, new_file_path, encoding_from, encoding_to='utf-8'):
    first_line = True
    with open(file_path, 'r', encoding=encoding_from) as fr:
        with open(new_file_path, 'w', encoding=encoding_to) as fw:
            for line in fr:
                line_stripped = line.strip()
                if line_stripped:
                    if line_stripped.isnumeric():
                        if first_line:
                            fw.write(line_stripped + '\n')
                            first_line = False
                        else:
                            fw.write('\n' + line_stripped + '\n')
                    else:
                        fw.write(line_stripped + '\n')


# parse folder
folder_path = sys.argv[1]

print('Processing srt files in folder: ' + folder_path)
for file in os.listdir(folder_path):
    if file.endswith('.srt') and not file.endswith('.new.srt'):
        file_path = os.path.join(folder_path, file)
        file_enc = detect_encoding(file_path)
        print('Converting subtitle: ' + file)
        convert_subtitle(file, file.replace('.srt', '.new.srt'), file_enc)
