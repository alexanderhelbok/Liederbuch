import os

def get_files_by_file_size(dirname, reverse=False):
    """ Return list of file paths in directory sorted by file size """

    # Get list of files
    filepaths = []
    for basename in os.listdir(dirname):
        if basename[-4:] == ".tex":
            filepaths.append(basename)

    # Re-populate list with filename, size tuples
    for i in range(len(filepaths)):
        filepaths[i] = (filepaths[i], os.path.getsize(os.path.join(dirname, filepaths[i])))

    # Sort list by file size
    # If reverse=True sort from largest to smallest
    # If reverse=False sort from smallest to largest
    filepaths.sort(key=lambda filename: filename[1], reverse=reverse)

    # Re-populate list with just filenames
    for i in range(len(filepaths)):
        filepaths[i] = filepaths[i][0]

    return filepaths

lst = get_files_by_file_size("/home/taco/Documents/Liederbuch/texsongs")
print(lst)

with open("loader.tex", 'w') as f:
    for song in lst:
        f.write("% !TeX root = Liederbuchtest.tex\n")
        f.write("\myinput[]{" + song[:-4] + "}\n")
        f.write("\clearpage")
