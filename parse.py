import re
import os

filename = "texsongs/wonderwall"

accords = ['A', 'A7', 'A7sus4', 'Am', 'Bm', 'Bm/A', 'Bm/Ab', 'C', 'C#m', 'D', 'D7', 'D7', 'Dm', 'E', 'Em', 'F', 'F#m', 'G', 'G7', 'Gmaj7', 'H7', 'Hm7', 'hm']
text = "This is a string with A, C, and Am enclosed in whitespaces."

accord = r'({})([A-Z\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accordrep = r'\\acc{\1}\2'
verse = r'(\b\d)\.'
verserep = r'\\verse'
Ref = r'\+ Ref.\n'
Refrep = r'\\Reff'
refrain = r'(Refrain|Refr\.:|Refrain:|Ref\. 1:|Ref\. 2:)\n'
refrainrep = r'\\refrain{Refrain:} '
nl = r'([\w.,:;!?-])(\n)'
nlrep = r'\1 \\\\ \n'
Ref2 = r'Reff'
Ref2rep = r'Reff\n'
pagenum = r'^\d+$\n'
pagenumrep = r'\n'
hash = r'#'
hashrep = r'\\faHashtag '
intro = r'(Intro:|Outro:)\n'
introrep = r'\\refrain{\1} '

with open(filename + ".txt") as f:
    content = f.readlines()

# add extra line at end to prevent index out of range
content += "\n"

parsed = False

with open(filename + ".tex", 'w') as f:
    for (i, line) in enumerate(content[:-1]):
        if i == 0:          # parse title
            # check wether file has already been parsed by looking for \title{...}
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
            temp1 = re.sub(hash, hashrep, temp1)
            temp1 = re.sub(intro, introrep, temp1)
            if not re.match(verse, content[i+1]) and not re.match(refrain, content[i+1]) and line is not content[-2]:
                temp1 = re.sub(nl, nlrep, temp1)
                f.write(temp1)
            else:
                f.write(temp1)
                f.write("\n")
    if not parsed:
        f.write("\\end{enumerate}")
f.close()

accspace = r'-\s*\\acc\{([^}]*)\}\s*-'
accspacerep = r'-\\acc{\1}-'

# reopen file to clear some things up
with open(filename + ".tex") as g:
    content = g.readlines()

with open(filename + ".tex", 'w') as f:
    for (i, line) in enumerate(content):
        temp1 = temp1 = re.sub(accspace, accspacerep, line)
        f.write(temp1)

#print(content[-2])
