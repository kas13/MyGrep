import argparse
import os
import mygrep


def full_message(file_name, result_list):
    for lines in result_list:
        print "\033[1;31m{0} :\x1b[01;37m{1}".format(file_name, lines)

def recur(path, pattern, count_string, ignore_case, number_string, revers_string, recursion):

    files = []
    for child in os.listdir(path):
        files.append(path + '/' + child)
    files_names = []
    for f in files:
        if os.path.isdir(f):
            files_names.extend(recur(f, pattern, count_string, ignore_case, number_string,
                                       revers_string, recursion))
        if os.path.exists(f) and not os.path.isdir(f):
            files_names.append(f)
    return files_names

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="full string match", nargs='*')
    parser.add_argument("-p", help='pattern', dest='pattern')
    parser.add_argument("-o", help="matched piece of string", dest="piece_string")
    parser.add_argument("-w", help='full-word match',  dest="full_match")
    parser.add_argument("-c", help='count string', dest="count", action='store_true')
    parser.add_argument("-i", help='ignore case', dest='ignore', action='store_true')
    parser.add_argument("-n", help='number string', dest='number', action='store_true')
    parser.add_argument("-v", help='only not match', dest='revers', action='store_true')
    parser.add_argument("-r", help='recursion file system', dest='recursion', nargs='*')
    args = parser.parse_args()

    count_string = False
    ignore_case = False
    number_string = False
    revers_string = False
    recursion = False

    pattern = ''
    files = []
    if args.name:
        for name in args.name:
            files.append(name)
    if args.pattern:
        pattern = args.pattern
    if args.piece_string:
        pass
    if args.full_match:
        pass
    if args.count:
        count_string = True
    if args.ignore:
        ignore_case = True
    if args.number:
        number_string = True
    if args.revers:
        revers_string = True
    if args.recursion:
        for arg in args.recursion:
            recursion = True
            res = recur(arg, pattern, count_string, ignore_case, number_string,
                                       revers_string, recursion)
            files = res
    result = mygrep.grep_files(files, pattern, count_string, ignore_case, number_string,
                     revers_string, recursion)
    for complite_string in result:
        print complite_string

if __name__ == '__main__':
    main()