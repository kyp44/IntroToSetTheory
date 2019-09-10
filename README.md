Introduction to Set Theory by Karel Hrbacek and Thomas Jech, 3rd Edition, Revised and Expanded
==============================================================================================

Solutions Manual
----------------

The main solutions manual is `solutions.tex`.
Unfortunately I only started typing up my solutions starting with Chapter 5, having kept them in a handwritten notebook prior to that.
I do intend to eventually go back and start typing up my solutions to the earlier chapters as well to have a more complete manual.
The `python` directory contains some quick and dirty Python scripts that were used to gain insight while working on some of the exercises.
These are not really documented at all and so probably will not be of interest to anyone else.

Other Documents
---------------

When doing exercises it can be useful to see a list of lemmas that have been written as part of the solutions.
Running the `lemmas.py` Python script will build `lemmas_content.tex` that contains these lemmas.
You can then build a lemma list document by compiling `lemmas.tex`, which includes `lemmas_content.tex`.

I have also found it useful to work out more detailed proofs of some of the theorems in the text, for which the text usually provides proofs that gloss over the details.
A document with these proofs can be built by compiling `theorems.tex`.
Many of these more detailed proofs also have their own lemmas, some of which are also used in the solutions manual or vice versa.
Such lemmas resided in their own `.tex` files in the `shared` directory so they can be included in both documents.

Lastly, I have also been keeping a list of errata in the book, which can be compiled from `errata.tex`.

Miscellaneous
-------------

Please submit an issue if you discover any errors in any of the proofs or any typos.

For an up-to-date PDF of the solutions manual, theorems document, errata list, and links to other resources for this text head over to [my website](https://kyp4.dyndns-home.com/set-theory/).
Note that this is still a work in progress.
