import re

infile = "/home/taco/Documents/Liederbuch/build/Liederbuch.toc"
outfile = "/home/taco/Documents/Liederbuch/toc.tex"

pattern = r"{(.*?)}"
pagenum = r"\\textbf\s*{(\d+)"

temp = []

with open(infile) as f:
    content = f.readlines()

for i, line in enumerate(content[1:]):
        matches = re.findall(pattern, line)
        temp.append(matches[1])

print(temp)

letter = ""
with open(outfile, 'w') as f:
    for line in sorted(temp):
        if line[0] is not letter:
            letter = line[0]
            f.write("\\toctitle{" + line[0] + "} \n")
        num = re.findall(pagenum, line)[0]
        f.write("\\hyperlink{page." + num + "}{" + line + "}} \\\\ \n")


