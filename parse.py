import re
import os

filename = "texsongs/Irgendwie, Irgendwo, Irgendwann"

accords = ['A', 'Asus4', 'A7', 'A7sus4', 'Am', 'Bm', 'Bm/A', 'Bm/Ab', 'C', 'C#m', 'D', 'D7', 'D7', 'Dm', 'E', 'Em', 'F', 'F#m', 'G', 'G7', 'Gmaj7', 'H7', 'Hm7', 'hm']
text = "This is a string with A, C, and Am enclosed in whitespaces."

accord = r'({})([A-Z\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accordrep = r'\\acc{\1}\2'
verse = r'(\b\d)\.'
# verserep = r'\\verse'
verserep = r'\\myverse{'
Ref = r'\+ Ref.\n'
Refrep = r'\\Reff'
refrain = r'([1-9]x)?\s?(Refrain|Refr|Ref. 1|Ref. 2)[:\.]?\n'
# refrainrep = r'\\refrain[\1]{Refrain:} '
refrainrep = r'\\myrefrain[\1]{Refrain:}{ '
vorref = r'Vor-Ref[:\.]?\n'
# vorrefrep = r'\\refrain{Vor-Ref:} '
vorrefrep = r'\\myrefrain{Vor-Ref:}{ '
nl = r'([\w.,:;!?-«»\}])(\n)'
nlrep = r'\1 \\\\ \n'
Ref2 = r'Reff'
Ref2rep = r'Reff\n'
pagenum = r'^\d+$\n'
pagenumrep = r'\n'
hash = r'#'
hashrep = r'\\faHashtag '
intro = r'Intro:\n'
introrep = r'\\intro '
outro = r'(Outro|Bridge):?\n'
# outrorep = r'\\refrain{\1:} '
outrorep = r'\\myrefrain{\1:}{ '

Refrain = f"({refrain}|{vorref}|{intro}|{outro})"

with open(filename + ".txt") as f:
    content = f.readlines()

verseflag = False
refflag = False
# pre parse
# for line in content:
#     if line[0:2] == "1.":
#         enumenv = True
#         break

# add extra line at end to prevent index out of range
content += "\n"

with open(filename + ".tex", 'w') as f:
    for (i, line) in enumerate(content[:-1]):
        if i == 0:          # parse title
            f.write(f"\\title{{{line[:-1]}}} \n")
            f.write("\n")
            f.write("\\begin{enumerate}\n")
        else:
            if re.match(verse, line):
                verseflag = True
            if re.match(Refrain, line):
                refflag = True
            # check wether next line is a refrain start or a verse start
            temp1 = re.sub(accord, accordrep, line)
            temp1 = re.sub(pagenum, pagenumrep, temp1)
            temp1 = re.sub(verse, verserep, temp1)
            temp1 = re.sub(Ref, Refrep, temp1)
            temp1 = re.sub(vorref, vorrefrep, temp1)
            temp1 = re.sub(refrain, refrainrep, temp1)
            temp1 = re.sub(Ref2, Ref2rep, temp1)
            temp1 = re.sub(hash, hashrep, temp1)
            temp1 = re.sub(intro, introrep, temp1)
            temp1 = re.sub(outro, outrorep, temp1)
            if not re.match(verse, content[i+1]) and not re.match(Refrain, content[i+1]) and not re.match(pagenum, content[i+1]) and line is not content[-2]:
                temp1 = re.sub(nl, nlrep, temp1)
                f.write(temp1)
            else:
                if verseflag:
                    temp1 = re.sub('\n', ' }\n', temp1)
                    verseflag = False
                elif refflag:
                    temp1 = re.sub('\n', ' }\n', temp1)
                    refflag = False
                f.write(temp1)
                f.write("\n")
    f.write("\\end{enumerate}")
f.close()

accspace = r'-\s*\\acc\{([^}]*)\}\s*-'
accspacerep = r'-\\acc{\1}-'

# reopen file to clear some things up
with open(filename + ".tex") as g:
    content = g.readlines()

content += "\n"

with open(filename + ".tex", 'w') as f:
    for (i, line) in enumerate(content[:-1]):
        if not (line == "\n" and content[i+1] == "\n"):
            temp1 = re.sub(accspace, accspacerep, line)
            f.write(temp1)

#print(content[-2])
