# project1.py
#
# ICS 32 Fall 2025
# Project #1: File System Explorer
#
# NAME: Joseph Li
# EMAIL: josel35@uci.edu
# STUDENT ID: 73817120
#
# High-level Design:
"""
lists: the commands are parsed as tuples and passed through various functions depending on the content of the list
    for example:
    if the command is ls, it will strip the 0th index (ls) and pass the rest of the tuple to the ls function to be sorted
uses for loops for each case to be evaluated, throws an error if there is an illegal statement

"""
import pathlib
from distutils.util import split_quoted
#

from pathlib import Path

# These string constants are provided to avoid typo errors for the man command.
# Each constant holds one line of text.
# These can be concatenated to create the correct man directions.
# Note: uncomment and move the constants into your function for creating the directions.

GENERIC1 = "The File System Explorer supports this command in the following format/s:\n"
GENERIC2 = "[COMMAND]\n"
GENERIC3 = "[COMMAND] [INPUT]\n"
GENERIC4 = "[COMMAND] [-OPTIONS] [INPUT]\n"
GENERIC5 = "[COMMAND] [-OPTIONS] [INPUT] [OPTION_INPUT]\n"
GENERIC6 = "The [INPUT] corresponds to the [COMMAND].\n"
GENERIC7 = "The [OPTIONAL_INPUT] corresponds to [-OPTIONS].\n"
LS_DIR = "ls is a command that lists the contents of a directory. [INPUT] is the path.\n"
LS_DIR2 = "ls options include -r, -f, -s, -e, -g and -l.\n"
LS_DIR3 = "-r = recursive, -f file only, -s match specific file name, -e match specific extension.\n"
LS_DIR4 = "-g and -l prints only files with size greater (g) or less (l) than [OPTION_INPUT].\n"
CAT_DIR = "cat is a command that prints the contents of a file. [INPUT] is the file path.\n"
CAT_DIR2 = "cat options include -f and -d.\n"
CAT_DIR3 = "-f = prints the first line only, -d duplicates the file into filename.dup.\n"
MAN_DIR = "man is a command that prints the directions for the command. [INPUT] is the command.\n"
Q_DIR = "q is a command that quits the file system explorer.\n"



def ls(input_list: list) -> list:
    print(input_list)
    def obtain_contents(path:Path) -> tuple:
        """obtains files and directories of parameter and returns them in a tuple of sorted lists, first one is files
        and seconds one is directory"""
        file_list = []
        directory_list = []
        for i in path.iterdir():
            if i.is_file():
                file_list.append(i)
            else:
                directory_list.append(i)
        file_list.sort()
        directory_list.sort()
        return file_list, directory_list
    try:
        #check if there is -OPTIONS
        if input_list[0][0] == '-':
            options = input_list[0][1:]
            file_path = Path(input_list[1])
            file_list, directory_list = obtain_contents(file_path)
            recursive_list = []
            error_counter = 0
            #execute -e option:
            if 'e' in options:
                error_counter += 1
                EXT_match = input_list[2]
                for i, d in enumerate(file_list[:]):
                    if d.suffix[1:] != EXT_match:
                        print(d.suffix)
                        file_list.remove(d)
            #execute -g option:
            if 'g' in options:
                error_counter += 1
                SIZE_match = eval(input_list[2])
                for i, d in enumerate(file_list):
                    if d.stat().st_size <= SIZE_match:
                        file_list.pop(i)
            #execute -g option:
            if 'l' in options:
                error_counter += 1
                SIZE_match = eval(input_list[2])
                for i, d in enumerate(file_list):
                    if d.stat().st_size >= SIZE_match:
                        file_list.pop(i)
            if 'r' in options:
                for i in directory_list:
                    recursive_input_list = [input_list[0], str(i)] + input_list[2:] #forgiving slicing...
                    recursive_list += ls(recursive_input_list)
            #execute -s option
            if 's' in options:
                error_counter += 1
                filename_match = input_list[2]
                for i, d in enumerate(file_list[:]): #copies list
                    if filename_match not in d.name:
                        file_list.remove(d)
                directory_list = []
            if error_counter > 1:
                raise TypeError
            if 'f' in options:
                directory_list = []
            return file_list + directory_list + recursive_list
        #no options:
        else:
            file_path = Path(input_list[0])
            file_list, directory_list = obtain_contents(file_path)


            return file_list + directory_list
    except (TypeError, IndexError, NameError):
        return ["ERROR: Invalid Format.\n"]
    except FileNotFoundError:
        return ["ERROR: Invalid Path.\n"]


def cat(input_list: list) -> str:
    try:
        return_value = ''
        if input_list[0][0] == '-':
            file_path = Path(input_list[1])
            f = file_path.open()
            if ('f' in input_list[0]) and ('d' in input_list[0]):
                raise TypeError
            if 'f' in input_list[0]:
                return_value += f.readline()
            if 'd' in input_list[0]:
                write_file = Path(str(file_path) + ".dup").open('w')
                for line in f:
                    write_file.write(line)
                    #return_value += line
                write_file.flush()
                write_file.close()
        else:
            file_path = Path(input_list[0])
            f = file_path.open()
            for line in f:
                return_value += line
        f.close()
        return return_value
    except (TypeError, IndexError):
        print("test invalid format")
        return "ERROR: Invalid Format.\n"
    except FileNotFoundError:
        return "ERROR: Invalid Path.\n"
def man(input_list: list) -> str:
    if input_list[0] == 'man':
        return GENERIC1 + GENERIC3 + MAN_DIR
    if input_list[0] == 'q':
        return GENERIC1 + GENERIC2 + Q_DIR
    if input_list[0] == 'cat':
        return GENERIC1 + GENERIC3 + GENERIC4 + GENERIC6 + CAT_DIR + CAT_DIR2 + CAT_DIR3
    if input_list[0] == 'ls':
        return GENERIC1 + GENERIC3 + GENERIC4 + GENERIC5 + GENERIC6 + GENERIC7 + LS_DIR + LS_DIR2 + LS_DIR3 + LS_DIR4
    else:
        return "ERROR: Invalid Command.\n"



def parse_command(user_input):
    """ parse user input into a line, use the tuple to navigate through different commands, removes the first
    line of line once a command is found"""
    return_value = ''
    input_list = user_input.split()
    user_command = input_list
    if user_command[0] == 'q':
        return_value = "quit"
    elif user_command[0] == 'ls':
        input_list = input_list[1:]
        for i in ls(input_list):
            return_value += str(i) + "\n"
    elif user_command[0] == 'cat':
        return_value = cat(input_list[1:])
    elif user_command[0] == 'man':
        return_value = man(input_list[1:])
    else:
        return_value = "ERROR: Invalid Command.\n"
    return return_value

def main() -> None:
    while True:
        user_input = input()
        value = parse_command(user_input)
        if value == "quit":
            exit()
        else:
            print(value, end="")

if __name__ == '__main__':
    main()