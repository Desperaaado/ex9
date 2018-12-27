import sys
import argparse
import re

def args():
    parser = argparse.ArgumentParser(
        description='Realize sth like "sed" command.'
    )
    parser.add_argument(
        '-expression',
        nargs = '?',
        help = 'Seg by expression.'
    )
    parser.add_argument(
        'content',
        nargs = '?',
        help = 'File name.'
    )
    return parser.parse_args()
    
def deal_expression(expression):
    expr_list = expression.split('/')

    if expr_list[0] == 's' and expr_list[-1] == 'g':
        mode = 'sg'
        result = expr_list[1:3]
    else:
        print('sg function only.(for now)')
        sys.exit(1)
    
    return mode, result

def expression_sg(old_str, new_str, line):
    # replace old_str to new_str (support regular expression.)
    pattern = re.compile(old_str)
    return re.sub(pattern, new_str, line)

def deal_content(content):

    if not content:
        lines = sys.stdin.readlines()
    else:
        lines = open(content).readlines()

    return lines

def cook_lines(lines, cook_book):
    mode, key_list = cook_book

    if mode == 'sg':
        cooked_lines = []

        for line in lines:
            new_line = expression_sg(key_list[0], key_list[1], line)
            cooked_lines.append(new_line)
    else:
        print('sg function only.(for now)')
        sys.exit(1)

    return cooked_lines

def show_content(file):
    if not file:
        content = sys.stdin
        pass
    else:
        with open(file) as f:
            content = f.read()
            print(content)

def the_main():
    # Init
    argv = args()
    expression = argv.expression
    content = argv.content

    # Choose mode
    if expression:
        cook_book = deal_expression(expression)
    else:
        print('expression mode only.(right now)')
        sys.exit(1)
    
    # Content process
    lines = deal_content(content)

    # Do the job
    cooked_lines = cook_lines(lines, cook_book)

    if content:
        with open(content, 'w') as f:
            f.writelines(cooked_lines)
    else:
        print('file mode only.(right now)')
        sys.exit(1)

    # Done!
    show_content(content)

the_main()