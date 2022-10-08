import os
import sys
import re
import datetime


def rename(di, fi):
    date_str = str(datetime.date.today())
    old_name = os.path.join(di, fi)
    new_name = os.path.join(di, date_str+" "+fi)
    os.rename(old_name, new_name)


if __name__ == "__main__":
    directory = os.path.dirname(sys.argv[0])

    for file in os.listdir(directory):  # skip python files
        filename = os.fsdecode(file)
        if filename.endswith(".py") or filename.endswith(".pyw") or filename.endswith(".exe"):
            continue
        if re.search("^\d{4}-\d\d-\d\d", filename):  # already contains date in front
            continue
        elif "." in filename:
            rename(directory, filename)
