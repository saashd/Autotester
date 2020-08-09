import filecmp
import os
import os.path
import re

current_directory = os.path.dirname(os.path.realpath(__file__))


def get_cpp_string():
    cppfiles = []
    parent_directory = os.path.join(current_directory, '..')
    for f in os.listdir(parent_directory):
        if f.endswith(".cpp"):
            cppfiles.append(os.path.join(parent_directory, f))
    main_idx = cppfiles.index(os.path.join(parent_directory, 'main.cpp'))
    cppfiles = [cppfiles[main_idx]] + cppfiles[:main_idx] + cppfiles[
                                                            main_idx + 1:]
    print('[info] Found {} C++ files:'.format(len(cppfiles)))
    for f in cppfiles:
        print(f)

    s = ' '.join(cppfiles)
    return s


def compile(cppfiles):
    exe_name = 'e.exe'
    exe = os.path.join(current_directory, exe_name)
    print('[info] trying to compile...')
    cmd_line = 'g++ -std=c++98 -pedantic -Wall ' + cppfiles + ' -o ' + exe
    print('[compiling] ', cmd_line)
    os.system(cmd_line)
    print('[info] compilation successful')
    return exe_name


def get_tuple_list_of_input_output():
    input = list_of_txt_files('input')
    output = list_of_txt_files('output')
    print('[info] found {} input/output files:'.format(len(input)))
    z = list(zip(input, output))
    for i, o in z:
        print('{} -> {}'.format(i, o))
    return z


def list_of_txt_files(param):
    files = []
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if (f.endswith(".txt"))]:
            if filename.startswith(param):
                files.append(filename)
    files.sort()
    return files


def extract_num_from_str(string):
    return int(re.search(r'\d+', string).group())


def run_test(exe, input_file, output_file):
    number = extract_num_from_str(input_file)
    my_output_file = 'myoutput{}.txt'.format(number)
    cmd_str = exe + ' < ' + input_file + ' > ' + my_output_file
    print('[info] running cmd: {}'.format(cmd_str))
    os.system(cmd_str)
    return filecmp.cmp(my_output_file, output_file)


def main():
    cppfiles = get_cpp_string()
    exe = compile(cppfiles)
    input_output_list = get_tuple_list_of_input_output()
    for i in range(len(input_output_list)):
        res = run_test(exe, *input_output_list[i])
        print('[info] Test {}: {}'
              .format(i + 1, 'PASSED' if res else 'FAILED'))


if __name__ == '__main__':
    main()
