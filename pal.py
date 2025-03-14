
import sys


def run(file_name:str = 'words.txt', line_max_len:int = 5):

    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    line = ''
    line_count = 0

    # validate idividual lines
    def validate_line(line:str):
        line = line.strip()  #remove trailing newline

        if len(line) > line_max_len:
            raise ValueError ('line ' + str(line_count + 1) + ' beginning with "' +
                    line + '" is too long. Exiting.')

        if not line.isalpha():
            raise ValueError ('line ' + str(line_count + 1) + ' "' +
                    line + '" contains non-alphabetic characters. Exiting.')

        return line.lower()

    f = open(file_name, 'r')
    
    while line := f.readline(line_max_len + 2):  # one for the newline, one for over max_len
        line = validate_line(line)
        line_count += 1
        print(line)

    print('Processed ' + str(line_count) + ' lines')
    f.close()

run()



