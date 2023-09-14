import subprocess
import os
import hashlib
from pprint import pprint
import shutil

"""
Takes file path as an argument, 
gets the SHA256 hash for the contents of the file
returns file_path and hash
"""


def file2hash(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    sha256 = hashlib.sha256()

    sha256.update(data)
    return file_path, sha256.hexdigest()


"""
Stores hash values.
If optional argument baseline is True,
.baseline.txt is overwritten
If optional argument baseline is False(default) 
new filehashs are appended to .baseline.txt
"""


def store_hash(filename, baseline=False, output_file=".baseline.txt"):
    name, hash_value = file2hash(filename)
    if baseline == True:
        with open(output_file, "w") as f:
            f.write("{}|{}\n".format(name, hash_value))
    else:
        with open(output_file, "a") as f:
            f.write("{}|{}\n".format(name, hash_value))

    return


"""
Loads the baseline hashes stored
"""


def load_baseline(baseline=".baseline.txt"):
    with open(baseline, "r") as f:
        data = f.readlines()
    return data


"""
Adds baseline data into a dictionary in key: value pairs
"""


def baseline2dict(data):
    baseline_dictionary = {}
    for line in data:
        if(line=="\n"):
            break
        key = line[:line.index("|")]
        val = line[line.index("|") + 1:line.index("\n")]
        baseline_dictionary.update({key: val})

    #print(baseline_dictionary)
    return baseline_dictionary


def compare_hash(baseline_path=".baseline.txt", current="test.txt"):
    baseline = baseline2dict(load_baseline(baseline_path))
    name, hash_val = file2hash(current)
    return baseline[name] == hash_val


"""
Notifies user of changes
"""
def notify(result):
    if(result):
        print("File integrity confirmed. \n Changes have not been made to the file.")
        return
    print("Warning! A change has been detected")
    return


# print(store_hash("test.txt"))
# pprint(baseline2dict(load_baseline()))

#print(compare_hash())

def main():

    choice = "" #initialize choice variable
    baseline = "" # initialize baseline variable

    print("Welcome to the File Integrity Monitor! \n")
    while(choice != "exit"):
        print("What would you like to do? \n"
              "Enter '1' to collect a new baseline \n"
              "Enter '2' to monitor files with the existing baseline \n"
              "Enter 'exit' to exit the program \n")
        choice = input("Please enter '1', '2', or 'exit': \n")

        if(choice == "1"):
            option = input("Enter the directory path, file path, or '.' if the current directory \n is your target directory")
            option = "test.txt"
            store_hash(option, True)
            print("A baseline has been saved!")

        if(choice == "2"):
            option = input("Enter the directory path, file path, or '.' if the current directory \n is your target directory of the file you'd like to monitor")
            notify(compare_hash())

    print("Have a nice day!")


main()