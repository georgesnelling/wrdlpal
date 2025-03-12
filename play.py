
line_max_len = 5
line_count = 0

# validate idividual lines
def validate(line):
    line = line.strip()  #remove trailing newline
    if len(line) > line_max_len:
        raise ValueError ('line ' + str(line_count + 1) + ' beginning with "' +
                line + '" is too long. Exiting.')
    return line

f = open('words.txt', 'r')
while line := f.readline(line_max_len + 2):
    line = validate(line)
    line_count += 1
    print(line)

print('Processed ' + str(line_count) + ' lines')
f.close()

