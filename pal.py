
import sys

def run():

    line = ''
    line_count = 0
    letter_count = 0
    line_max_len = 5
    tot_letter_points = 1000
    tot_pair_points = 10000
    pair_points_cutoff = 10
    file_name = 'words.txt'
    if len(sys.argv) > 1:
        file_name = sys.argv[1]

    # Initialize pairs dict
    pairs = {}
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for letter in letters:
        pairs[letter] = {
            'count':0, 
            'points': 0, 
            'left': {}, 
            'left_sorted': [],
            'left_points': [], 
            'right': {},
            'right_sorted': [],
            'right_points': []
        }


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
            
            print('\n' + letter + ': ' + str(pairs[letter]['points']) + '/' + str(tot_letter_points))

            print('Left: ', end='')
            for point in pairs[letter]['left_points']:
                print(' ' + point[0] + ':' + str(point[1]), end='')
            print()

            print('Right:', end='')
            for point in pairs[letter]['right_points']:
                print(' ' + point[0] + ':' + str(point[1]), end='')
            print()

    
    def sort_pairs_by_count(pairs):
        for letter in pairs:
            pairs[letter]['left_sorted'] = list(sorted(pairs[letter]['left'].items(), key=lambda x:x[1], reverse=True))
            pairs[letter]['right_sorted'] = list(sorted(pairs[letter]['right'].items(), key=lambda x:x[1], reverse=True))


    # Calculate normalized points for letters and pairs independent of sample size
    def score(pairs, letter_count):

        for letter in pairs:
            
            # Calculate the points for the letter itself
            pairs[letter]['points'] = round(pairs[letter]['count'] / letter_count * tot_letter_points)

            # TODO:  create helper to get rid of duped logic
            left_points = []
            for toup in pairs[letter]['left_sorted']:
                pair_points = round(toup[1] / letter_count * tot_pair_points)
                if pair_points >= pair_points_cutoff:
                    left_points.append((toup[0], pair_points))
            pairs[letter]['left_points'] = left_points
                
            right_points = []
            for toup in pairs[letter]['right_sorted']:
                pair_points = round(toup[1] / letter_count * tot_pair_points)
                if pair_points >= pair_points_cutoff:
                    right_points.append((toup[0], pair_points))
            pairs[letter]['right_points'] = right_points
                


    # count the letter pairs in a line, including BOL and EOL as a letter
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
        print(line)

    # sort dicts into lists by count descending
    sort_pairs_by_count(pairs)

    score(pairs, letter_count)

    print('Processed ' + str(line_count) + ' lines and ' + str(letter_count) + ' letters')
    pretty_print(pairs)

    f.close()

run()



