import re
import os

filename = "help.tex"

accords = ["A", "A7", "C", "Am", "G", "G7", "F", "D", "D7", "Em", "hm", "H7", "F#m", "D7", "Hm7", "Bm", "Gmaj7", "Bm/A", "Bm/Ab", "C#m", "E"]
text = "This is a string with A, C, and Am enclosed in whitespaces."

accord = r'({})([\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accordrep = r'\\acc{\1}\2'
verse = r'(\b\d)\.'
verserep = r'\\verse'
Ref = r'\+ Ref.\n'
Refrep = r'\\Reff'
refrain = r'(Refrain|Refr\.:|Refrain:)\n'
refrainrep = r'\\refrain '
nl = r'([\w.,:;!?-])(\n)'
nlrep = r'\1 \\\\ \n'
Ref2 = r'Reff'
Ref2rep = r'Reff\n'
pagenum = r'^\d+$\n'
pagenumrep = r''

with open(filename) as f:
    content = f.readlines()

# add extra line at end to prevent index out of range
#content += "\n"

parsed = False

with open(filename, 'w') as f:
    for (i, line) in enumerate(content[:-1]):
        if i == 0:          # parse title
            # check wether file has already been parsed
            if line[0] == "\\":
                parsed = True
                f.write(line)
            else:
                f.write(f"\\title{{{line[:-1]}}} \n")
                f.write("\n")
                f.write("\\begin{enumerate}\n")
        else:
            # check wether next line is a refrain start or a verse start
            temp1 = re.sub(accord, accordrep, line)
            temp1 = re.sub(pagenum, pagenumrep, temp1)
            temp1 = re.sub(verse, verserep, temp1)
            temp1 = re.sub(Ref, Refrep, temp1)
            temp1 = re.sub(refrain, refrainrep, temp1)
            temp1 = re.sub(Ref2, Ref2rep, temp1)
            if not re.match(verse, content[i+1]) and not re.match(refrain, content[i+1]) and line is not content[-2]:
                temp1 = re.sub(nl, nlrep, temp1)
                f.write(temp1)
            else:
                f.write(temp1)
                f.write("\n")
    if not parsed:
        f.write("\\end{enumerate}")


print(content[-2])
