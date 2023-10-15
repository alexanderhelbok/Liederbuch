import re
import locale

locale.setlocale(locale.LC_ALL, 'de_AT.UTF-8')

infile = "/home/taco/Documents/Liederbuch/build/Liederbuchtest.toc"
outfile = "/home/taco/Documents/Liederbuch/toc.tex"

pattern = r"{(.*?)}"
pagenum = r"\\textbf\s*{(\d+)"

temp = []

with open(infile) as f:
    content = f.readlines()

for i, line in enumerate(content[1:]):
        matches = re.findall(pattern, line)
        temp.append(matches[1])

#print(temp)

letter = ""
digitflag = False
with open(outfile, 'w') as f:
    for line in sorted(temp, key=locale.strxfrm):
        if line[0].isdigit():
            if not digitflag:
                f.write("\\toctitle{\faHashtag} \n")
            num = re.findall(pagenum, line)[0]
            f.write("\\hyperlink{page." + num + "}{" + line + "}} \\\\ \n")
        else:
            if line[0] is not letter:
                letter = line[0]
                f.write("\\toctitle{" + line[0] + "} \n")
            num = re.findall(pagenum, line)[0]
            f.write("\\hyperlink{page." + num + "}{" + line + "}} \\\\ \n")


