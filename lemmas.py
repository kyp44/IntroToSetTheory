#! /usr/bin/env python3
"""
Build lemmas document contents from other tex files.

Run with -h for more information.
"""
import argparse
import os

# Output file name
ofname = "lemmas_content.tex"

parser = argparse.ArgumentParser(description="Builds lemmas document content from\
chapter tex files as well as the theorems document. Output is written to " + ofname + ".")
args = parser.parse_args()

# Open up output file for writing
with open(ofname, "w") as ofile :
    # Go through files in the current directory
    for fname in sorted(os.listdir()) :
        # We only care about certain tex files
        if os.path.splitext(fname)[1].lower() != ".tex" :
            continue
        if fname.find("Ch") != 0 and os.path.splitext(fname)[0] != "theorems" :
            continue

        print("Processing " + fname + "...")

        # Open up input file for reading
        with open(fname, "r") as ifile :
            # Whether or not we are in a statement block
            ins = False

            # Go through each line in the file
            for line in ifile :
                # We don't care about whitespace at the beginning or end of the line
                sl = line.strip()

                # Are we in a statement block?
                if ins :
                    # Pass the line through
                    print(sl, file=ofile)

                    # Are ending the statement?
                    if sl.find(r"\end{statement}") == 0 :
                        # Print a blank line to leave some spaces
                        print("", file=ofile)
                        ins = False
                else :
                    # No, only pass through certain lines pertaining to the statements
                    if sl.find(r"\def") == 0 or sl.find(r"\setcounter{itm}") == 0 :
                        print(sl, file=ofile)
                    elif sl.find(r"\begin{statement}") == 0 :
                        # We are starting a statement, verify that no content is also on this line
                        if sl[-1] != "}" :
                            raise ValueError("Statement has content on the same line!")

                        # Determine the item reference tag (if there is one)
                        rti = sl.find(r"\itm{")
                        if rti < 0 :
                            # There is no reference tag, just pass the line through
                            print(sl, file=ofile)
                        else :
                            # There is a reference tag so extract it
                            rte = sl[rti:].find("}")
                            if rte < 0 :
                                raise ValueError("Item reference has no closing brace!")
                            rtag = sl[rti + 5 : rti + rte]
                            print(sl[:-1] + " \\{" + rtag + "\\}}", file=ofile)

                        ins = True
