
import sys

def run():

    line = ''
    line_count = 0
    letter_count = 0
    line_max_len = 5
    tot_letter_points = 1000
    tot_pair_points = 10000
    pair_points_cutoff = 8
    letters = 'abcdefghijklmnopqrstuvwxyz'
    consonants = 'bcdfghjklmnpqrstvwxz'
    file_name = 'words.txt'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    # Initialize pairs dict
    pairs = {}
    for letter in letters:
        pairs[letter] = {
            'count':0, 
            'points': 0, 
            'left': {}, 
            'left_points': [], 
            'cleft_points': [],
            'right': {},
            'right_points': [],
            'cright_points': []
        }


    # Untility debugger
    def inspect(pairs):
        print('INSPECT PAIRS')
        for letter in pairs:
            print('\n' + letter)
            for k in pairs[letter]:
                print(k,pairs[letter][k])


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

    
    # Print Human-Readable Summary Output as Text
    def pretty_print(pairs): 

        print('WordlePal')
        print('Letter Points:', tot_letter_points)
        print('Pair Points:', tot_pair_points)
        print('Points Cutoff:', pair_points_cutoff)
        print('Words Processed:', line_count)
        print('Letters Processed:', letter_count)

        for letter in pairs:

            # Skip empty letters
            if pairs[letter]['count'] == 0:
                continue
            
            # Print the top-level letter and its points
            print('\n' + letter + ':', (pairs[letter]['points']))

            # Print the left and right pairs and their points
            print_lines = [
                {'title': 'cLeft: ', 'data': 'cleft_points'}, 
                {'title': 'cRight:', 'data': 'cright_points'},
                {'title': 'Left:  ', 'data': 'left_points'},
                {'title': 'Right: ', 'data': 'right_points'}
                ]

            # Print each output line formatted, skipping empty lines
            for line in print_lines: 
                if len(pairs[letter][line['data']]) == 0:
                    continue
                print(line['title'], end='')
                for pair_letter in pairs[letter][line['data']]:
                    print(' ' + pair_letter[0] + ':' + str(pair_letter[1]), end='')
                print()

    
    # Calculate normalized points for letters and pairs independent of sample size
    def score(pairs, letter_count):

        for letter in pairs:
            
            # Calculate the points for the letter itself
            pairs[letter]['points'] = round(pairs[letter]['count'] / letter_count * tot_letter_points)

            print_out= [{'side': 'left', 'target': 'cleft_points', 'consonants_only': True},
                {'side': 'right', 'target': 'cright_points', 'consonants_only': True},
                {'side': 'left', 'target': 'left_points', 'consonants_only': False},
                {'side': 'right', 'target': 'right_points', 'consonants_only': False}]

            for out in print_out:
                pair_points = 0
                for pair_let in pairs[letter][out['side']]:

                    # skip consonants only output for vowels as top-level letters
                    if letter not in consonants and out['consonants_only']:
                        continue

                    # skip consonants only output for vowels as pair letters
                    if pair_let not in consonants and out['consonants_only']:
                        continue

                    pair_points = round(pairs[letter][out['side']][pair_let] / letter_count * tot_pair_points)
                    if pair_points >= pair_points_cutoff:
                        pairs[letter][out['target']].append((pair_let, pair_points))

            # sort printout arays by pair count descending
            for out in print_out:
                pairs[letter][out['target']].sort(key=lambda x: x[1], reverse=True)


    # count the letter pairs in a line, including begin-of-line and end-of-line as letters
    def count_pairs(line:str):

        def increment(c:str, left:str, right:str):

            # increment this particular letter count
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
        letter_count += len(line)
        count_pairs(line)
        # print(line)

    score(pairs, letter_count)

    # inspect(pairs)
    pretty_print(pairs)

    f.close()

run()
