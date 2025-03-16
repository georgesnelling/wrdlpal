
import sys


def run(file_name:str = 'words.txt', line_max_len:int = 5):

    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    line = ''
    line_count = 0

    letters = 'abcdefghijklmnopqrstuvwxyz'

    # Initialize pairs dict
    pairs = {}
    for letter in letters:
        pairs[letter] = {'count':0, 'left': {}, 'right': {}}


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

    
    def pretty_print(pairs): 

        for letter in pairs:

            if pairs[letter]['count'] == 0:
                continue

            print('\n' + letter + ': ' + str(pairs[letter]['count']))

            print('Left: ')
            for left in pairs[letter]['left']:
                print(left + ': ' + str(pairs[letter]['left'][left]))

            print('Right: ')
            for right in pairs[letter]['right']:
                print(right + ': ' + str(pairs[letter]['right'][right]))


    # count the letter pairs in a line, including BOL and EOL as a letter
    def count_pairs(line:str):

        def increment(c:str, left:str, right:str):

            # increment the letter count
            pairs[c]['count'] += 1

            # create the dict keys if they don't exist and set them to 0
            if left not in pairs[c]['left']:
                pairs[c]['left'][left] = 0 
            if right not in pairs[c]['right']:
                pairs[c]['right'][right] = 0 
            
            # increment the pair counts
            pairs[c]['left'][left] += 1
            pairs[c]['right'][right] += 1


        for i in range(len(line)):

            left = ''
            right = ''
            c = line[i]
            
            if i == 0:
                # beginning of line
                left = '^'  
                right = line[i + 1]

            elif i == len(line) - 1:
                # end of line
                left = line[i - 1]
                right = '^'

            else:
                # somewhere in the middle of line
                left = line[i - 1]
                right = line[i + 1]

            increment(c, left, right)

                
    f = open(file_name, 'r')
    
    # Main loop over each line in file
    while line := f.readline(line_max_len + 2):  # one for the newline, one for over max_len
        line = validate_line(line)
        line_count += 1
        print(line)
        count_pairs(line)

    print('Processed ' + str(line_count) + ' lines')

    pretty_print(pairs)

    f.close()

run()



