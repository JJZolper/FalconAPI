import json

result = [line.rstrip() for line in open('journals.txt')]

outputfile = open('output.txt', 'w')
json.dump(result, outputfile)
outputfile.close()






