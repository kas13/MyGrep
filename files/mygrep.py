import re
import os
import sys
import string
RED = '\033[1;31m'
WHITE = '\x1b[01;37m'
BLUE = '\033[96m'


def make_red(pattern, string):
    string = str(string)
    result = []
    for s in string.split():
        if s in pattern:
            result.append(RED+s)
        else:
            result.append(RED+s)
    result = " ".join(result)
    print result


def make_normal_word(file):
    with open(file, 'r') as f:
        lines = f.read().split('\n')
        lines = str(lines)
        all_word = re.findall(r'\w+', lines)
        return all_word

def numbering_strings(path, line, count=0, numbers_string=False, ignore_case=False):

    if ignore_case is True:
        if numbers_string is True:
            return ("{0}{1} : {2}{3} : {4}{5}".format(RED, path, BLUE, count,
                                                         WHITE, line))
        else:
            return "{0}{1} : {2}{3}".format(RED, path, WHITE, line)

    else:
        if numbers_string is True:
            return ("{0}{1} : {2}{3} : {4}{5}".format(RED, path, BLUE, count,
                                                         WHITE, line))
        else:
            return "{0}{1} : {2}{3}".format(RED, path, WHITE, line)


def full_complete(path, pattern, ignore_case=False, numbers_string=False,
                  revers_string=False):
    result_list = []
    try:
        count_list = []
        count = 0
        with open(path, 'r') as file:
            text = file.readlines()

        if ignore_case is True:
            gen_count_list = (search_index(text, pattern, revers_string))
            for count in gen_count_list:
                count_list.append(count)

        if count_list.__len__() == 0:
            if ignore_case is True:
                return result_list
            r = re.compile(pattern)
            for line in text:
                count += 1
                match = r.search(line)
                if match and revers_string is False:
                    new_string = numbering_strings(path, line, count, numbers_string,
                                                            ignore_case)
                    result_list.append(new_string)
                if revers_string is True and not match:
                    new_string = numbering_strings(path, line, count, numbers_string,
                                                            ignore_case)
                    result_list.append(new_string)

                # for word in words:
                #     match = r.search(word)
                #     if match and flag and revers_string is False:
                #         new_string = numbering_strings(path, line, count, numbers_string,
                #                                        ignore_case)
                #         result_list.append(new_string)
                #         flag = False
                #     if flag and revers_string is True and not match:
                #         new_string = numbering_strings(path, line, count, numbers_string,
                #                                        ignore_case)
                #         result_list.append(new_string)
                #         flag = False
        else:
            count = 0
            for line in text:
                count += 1
                for index in count_list:
                    if count == index:
                        new_string = numbering_strings(path, line, count, numbers_string,
                                                           ignore_case)
                        result_list.append(new_string)
        return result_list
    except:
        return result_list


def piece_of_string(pattern, file):
    result_list = []
    try:
        all_word = make_normal_word(file)
        all_word = "".join(all_word)
        result_list = re.findall(pattern, all_word)
        return result_list
    except:
        return result_list


def only_pattern(pattern, file):
    result_list = []
    all_word = make_normal_word(file)
    for word in all_word:
        if word == pattern:
            result_list.append(word)
    return result_list


def full_match(pattern, file):
    result_list = []
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                flag = True
                words_line = line.split(' ')
                for word in words_line:
                    m = re.match(pattern, word)
                    if m and flag is True:
                        if m.end() == word.__len__():
                            result_list.append(line)
                            flag = False
        return result_list
    except:
        return result_list


def search_index(lines, pattern, revers_string=False):
    pattern = str(pattern)
    temp_pattern = pattern.lower()
    count = 0
    for line in lines:
        count += 1
        temp_line = str(line).lower()
        res = re.search(temp_pattern, temp_line)
        if revers_string is False:
            if res:
                yield count
        if revers_string is True:
            if not res:
                yield count


def search_count_string(path, pattern, count_list, revers_string=False):
    with open(path, 'r') as file:
        text = file.readlines()

        if count_list.__len__() != 0:
            return "{0} {1} : {2} {3}".format(RED, path, WHITE, count_list.__len__())

        count = 0
        for line in text:
            line = "".join(line)
            if re.search(pattern, line) and revers_string is False:
                count += 1
            if revers_string is True and not re.search(pattern, line):
                count += 1
        return "{0} {1} : {2} {3}".format(RED, path, WHITE, count)


def recursive_crawling_files(path, pattern, count_string, ignore_case, number_string, revers_string, recursion):

    files = [path + "/" + child for child in os.listdir(path)]
    files_names = []
    for f in files:
        if os.path.isdir(f):
            result = recursive_crawling_files(f, pattern, count_string, ignore_case, number_string,
                                              revers_string, recursion)
        if os.path.exists(f):
            files_names.append(f)
    result = grep_files(files_names, pattern, count_string, ignore_case, number_string,
                                   revers_string, recursion)
    return result


def grep_files(paths, pattern, count_string=False, ignore_case=False,
               number_string=False, revers_string=False, recursion=False):
    result_string = []
    try:
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as file:
                    text = file.readlines()
                    count_list = []
                if ignore_case is True:
                    gen_count_list = (search_index(text, pattern, revers_string))
                    for count in gen_count_list:
                        count_list.append(count)

                if count_string is True:
                    string = search_count_string(path, pattern, count_list, revers_string)
                    result_string.append(string)

                if count_string is False:
                    r_list = full_complete(path, pattern, ignore_case, number_string,
                                           revers_string)

                    for r in r_list:
                        result_string.append(r)
        return result_string
        # if recursion is True:
        #     ff = []
        #     files = [paths + "/" + child for child in os.listdir(paths)]
        #     for f in files:
        #         if os.path.isdir(f):
        #             recursion = True
        #             return grep_files(f, pattern, count_string, ignore_case, number_string,
        #                   revers_string, recursion)
        #         if os.path.exists(f) and not os.path.isdir(f):
        #             ff.append(f)
        #     recursion = False
        #     return grep_files(ff, pattern, count_string, ignore_case, number_string,
        #                revers_string, recursion)
        #    # return result_string
        #     #print paths

    except:
        return result_string