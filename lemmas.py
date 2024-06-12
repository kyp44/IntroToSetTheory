#! /usr/bin/env python3
"""
Build lemmas document contents from other tex files.

Run with -h for more information.
"""
from collections import namedtuple
import argparse
import os

# Input directory
idir = "sections" + os.sep

# Output file name
ofname = "lemmas_content.tex"

# Argument parsing
parser = argparse.ArgumentParser(description="Builds lemmas document content from\
section tex files as well as the theorems tex file. Output is written to " + ofname + ".")
args = parser.parse_args()


def get_arg(line, cmd):
    """
    Retuns the argument if the Latex cmd
    is found. Otherwise None is returned.
    """
    lcmd = "\\" + cmd + "{"
    if line.find(lcmd) != 0:
        return None
    j = line.find("}")
    if j < 0:
        return None
    return line[len(lcmd):j]


sargs = ("lem", "cor", "defin", "thrm")
counter_map = {"section": "chapter",
               "subsection": "section"}


def process_file(fpath, ofile, headers=False, shared=None, defined_labels=[]):
    """
    Processes latex file to extract statements

    fpath - Path to .tex file
    ofile - Output file object
    headers - Increment counters for header lines
    shared - Name of shared statement file we are
             reading (None indicates we are not in
             a shared statement)
    defined_labels - LaTeX labels that have already
                     been defined so they are not
                     defined again. This list be be
                     added to.
    """
    # Open up input file for reading
    with open(fpath, "r") as ifile:
        # Whether or not we are in a statement or comment block
        ins = False
        inc = False
        mdef = 0

        # Go through each line in the file
        for line in ifile:
            # We don't care about whitespace at the beginning or end of the line
            sl = line.strip()

            # Are we in a commented out block?
            if inc:
                if sl.find(r"\fi") == 0:
                    inc = False
                continue

            # Are we in a statement block?
            if ins:
                # Pass the line through
                print(sl, file=ofile)

                # Are ending the statement?
                if get_arg(sl, "end") in sargs:
                    # Print a blank line to leave some spaces
                    print("", file=ofile)
                    ins = False
            else:
                # No, only pass through certain lines pertaining to the statements
                earg = get_arg(sl, "exercise")
                iarg = get_arg(sl, "input")
                targ = get_arg(sl, "theorem")
                scarg = get_arg(sl, "setcounter")
                if (sl.find(r"\def") == 0 and sl.find("{") >= 0) or mdef > 0:
                    # Include any macro definitions
                    print(sl, file=ofile)
                    if sl[-1] == "{":
                        # Multiline def
                        mdef += 1
                    elif sl[0] == "}":
                        # End multiline def
                        mdef -= 1
                elif sl.find(r"\iffalse") == 0:
                    # Start of comment block
                    inc = True
                    continue
                elif earg:
                    # Exercise line, set counters
                    e = int(earg)
                    print(r"\setcounter{subsection}{" + str(e-1) +
                          "}\stepcounter{subsection}", file=ofile)
                elif targ:
                    # Theorem line, set counters
                    t = int(targ)
                    print(r"\setcounter{subsection}{" + str(t-1) +
                          "}\stepcounter{subsection}", file=ofile)
                elif iarg and iarg.find("shared") == 0:
                    # Input line for shared satement
                    process_file(iarg + ".tex", ofile,
                                 shared=iarg.split("/")[-1], defined_labels=defined_labels)
                elif get_arg(sl, "begin") in sargs:
                    # We are starting a statement, verify that no content is also on this line
                    if sl[-1] != "}":
                        raise ValueError(
                            "Statement has content on the same line!")

                    add = ""

                    # Add shared tag if applicable
                    if shared:
                        add += "[Shared: " + \
                            shared.replace("_", r"\textunderscore ") + "] "

                    # Determine the label tag (if there is one)
                    lbl = "label"
                    i = sl.find("\\" + lbl)
                    if i >= 0:
                        larg = get_arg(sl[i:], lbl)
                        if larg:
                            add += r"\{" + larg + r"\}"

                        if larg in defined_labels:
                            # Need to strip out the label to prevent compiler warnings,
                            # because it has already been defined before.
                            sl = sl.replace(f"\\{lbl}{{{larg}}}", "")
                        else:
                            defined_labels.append(larg)

                    print(sl + add, file=ofile)

                    ins = True
                elif scarg:
                    # Set counter line
                    print(sl.replace(scarg, counter_map[scarg]), file=ofile)
                elif headers:
                    # Search for counter lines to increment counters
                    for hdr in counter_map.keys():
                        if sl.find("\\" + hdr) == 0:
                            print(
                                r"\stepcounter{" + counter_map[hdr] + "}", file=ofile)


# Section file record
Section = namedtuple("Section", ("chap", "sec", "fname"))

# List of already-defined item labels
defined_labels = []

# Open up output file for writing
with open(ofname, "w") as ofile:
    # Go through files in the current directory
    secs = []
    for fname in sorted(os.listdir(idir)):
        # We only care about certain tex files
        (bname, ext) = os.path.splitext(fname)
        if ext != ".tex":
            continue
        if bname.find("sec_") != 0:
            continue

        secs.append(Section(*(int(s)
                    for s in bname.split("_")[1:]), idir + fname))

    # Sort sections and go through them
    print(r"\section{Solutions}", file=ofile)
    for sec in sorted(secs, key=lambda s: (s.chap, s.sec)):
        print("Processing " + sec.fname + "...")

        # Set counters
        print(r"\setcounter{chapter}{" + str(sec.chap) + "}", file=ofile)
        print(r"\setcounter{section}{" + str(sec.sec) + "}", file=ofile)

        # Process section file
        process_file(sec.fname, ofile, defined_labels=defined_labels)

    # Go through theorems
    print("Processing theorems...")
    print(r"\setcounter{chapter}{0}", file=ofile)
    print(r"\setcounter{section}{1}", file=ofile)
    print(r"\section{Theorems}", file=ofile)
    process_file("theorems.tex", ofile, headers=True,
                 defined_labels=defined_labels)
