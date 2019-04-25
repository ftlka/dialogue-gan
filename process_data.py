import os


DIR_NAME = os.getcwd()
QUERY_TRAIN_FILE = 'gen_data/chitchat.train.query'
ANSWER_TRAIN_FILE = 'gen_data/chitchat.train.answer'
QUERY_TEST_FILE = 'gen_data/chitchat.dev.query'
ANSWER_TEST_FILE = 'gen_data/chitchat.dev.answer'


def load_lines(file_name):
    lines = []
    prev_first_line = ''
    first = True

    with open(file_name, 'r', encoding='utf-8') as f:
        cur_dialog = []
        for line in f:
            if first:
                first = False
                if line == prev_first_line:
                    lines.pop()
                prev_first_line = line

            if line.strip():
                cur_dialog.append(line[1:].strip())
            else:
                first = True
                lines.append(cur_dialog)
                cur_dialog = []
    return lines


def spruce_up_line(line):
    line = line.replace("'", " ' ")
    line = line.replace(".", " . ")
    line = line.replace("!", " !")
    line = line.replace("?", " ?")
    line = line.replace('"','')
    line = line.replace(",",'')
    line = line.replace("-", ' ')
    return ' '.join(line.lower().split())


def write_to_file(lines):
    with open(os.path.join(DIR_NAME, QUERY_TRAIN_FILE), 'w+') as query_train_file,\
            open(os.path.join(DIR_NAME, ANSWER_TRAIN_FILE), 'w+') as answer_train_file,\
            open(os.path.join(DIR_NAME, QUERY_TEST_FILE), 'w+') as query_dev_file,\
            open(os.path.join(DIR_NAME, ANSWER_TEST_FILE), 'w+') as answer_dev_file:
        for dialog in lines:
            # iterating over dialog except for the last phrase
            for i, phrase in zip(range(len(dialog) - 1), dialog):
                first_phrase = spruce_up_line(phrase)
                second_phrase = spruce_up_line(dialog[i + 1])
                if i % 1000 == 0:
                    query_dev_file.write(str(first_phrase) + '\n')
                    answer_dev_file.write(str(second_phrase) + '\n')
                else:
                    query_train_file.write(str(first_phrase) + '\n')
                    answer_train_file.write(str(second_phrase) + '\n')


if __name__ == '__main__':
    lines = load_lines(os.path.join(DIR_NAME, 'subtitles', 'dialogues.txt'))
    write_to_file(lines)
