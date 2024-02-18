import re
import os
import sys

filename = f"texsongs/{sys.argv[1]}"

accords = ['hm', 'Hm7', 'H/H7', 'H7',
            'Gmaj7', 'Gm7', 'Gm', 'G7', 'G',
            'Fm#', 'F#m', 'f#m', 'Fm7', 'F7', 'F',
            'Em7', 'Em', 'E7', 'E4', 'E',
            'D#', 'Dm', 'D7', 'D4', 'D',
            'C#dim', 'Cmaj7', 'C#7', 'C#m', 'cm#', 'Cm', 'C7', 'C',
            'Bm7' 'Bm/Ab', 'Bm/A', 'Bm',
            'Asus4', 'Am7', 'Am', 'A7sus4', 'A7', 'A']
text = "This is a string with A, C, and Am enclosed in whitespaces."

accord1 = r'([\w\s.,;:!?-])({})([A-Z0-9\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accord2 = r'([\w.,;:!?-])({})([\w\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accordrep = r'\1\\acc{\2}\3'
accord3 = r'({})([\s.,;:!?-])'.format('|'.join(map(re.escape, accords)))
accordrep3 = r'\\acc{\1}\2'
verse = r'(\b\d)\.'
# verserep = r'\\verse'
verserep = r'\\myverse{'
Ref = r'\+ Ref.\n'
Refrep = r'\\Reff'
#refrain = r'([1-9]x)?\s?(Refrain|Refr|Ref. 1|Ref. 2|Ref.|Refr.)[:\.]?\n'
refrain = r'([1-9]x)?\s?(Refrain|Refr|Ref(\.|\s\d)?)\.?:?\s?\n'
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
            f.write("% !TeX root = Liederbuchtest.tex\n")
            # f.write(f"\\title{{{line[:-1]}}} \n")
            f.write("\\begin{finalbox}{\\artist}\n")
            f.write(f"\\titlee{{{line[:-1]}}}\n")
            f.write("\\end{finalbox}\n")
            f.write("\n")
            f.write("\\begin{enumerate}\n")
        else:
            if re.match(verse, line):
                verseflag = True
            if re.match(Refrain, line):
                refflag = True
            # check wether next line is a refrain start or a verse start
            temp1 = re.sub(accord1, accordrep, line)
            temp1 = re.sub(accord2, accordrep, temp1)
            temp1 = re.sub(accord3, accordrep3, temp1)
            temp1 = re.sub(pagenum, pagenumrep, temp1)
            temp1 = re.sub(verse, verserep, temp1)
            temp1 = re.sub(Ref, Refrep, temp1)
            temp1 = re.sub(vorref, vorrefrep, temp1)
            temp1 = re.sub(refrain, refrainrep, temp1)
            temp1 = re.sub(Ref2, Ref2rep, temp1)
            temp1 = re.sub(hash, hashrep, temp1)
            temp1 = re.sub(intro, introrep, temp1)
            temp1 = re.sub(outro, outrorep, temp1)

            # if in refrain mode, make : upright
            if refflag:
                temp1 = re.sub(r'\|\:', r'{\\normalfont|:}', temp1)
                temp1 = re.sub(r'\:\|', r'{\\normalfont:|}', temp1)

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
