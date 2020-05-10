# Intro to Mathematical Cryptography
This repo (while currently only a work-in-progress) contains notes and sketches of algorithms highlighted in the book [_An Introduction to Mathematical Cryptography_ (Hoffstein et al., 2014)](https://www.springer.com/gp/book/9781441926746), as well as (attempted) solutions to exercises.

Files are grouped in folders `chap1`, `chap2`, etc., by the chapter that sparked their creation. Exercise files, named `exercise.py` should all be executable, and output answers or relevant information for each exercise in the following format:
```
$ python3 chap1/exercises.py
============================= Exercises chapter 1 ==============================
-------------------------------- Exercise 1.1. ---------------------------------
a)
A page of history is worth a volume of logic.
LALRP ZQSTD EZCJT DHZCE SLGZW FXPZQ WZRTN 
apage ofhis toryi swort havol umeof logic 

b)
AOLYL HYLUV ZLJYL AZILA ALYAO HUAOL ZLJYL AZAOH ALCLY FIVKF 
NBLZZ LZ
there areno secre tsbet terth anthe secre tstha tever ybody 
guess es

c)
XJHRF TNZHM ZGAHI UETXZ JNBWN UTRHE POMDN BJMAU GORFA OIZOC 
C
whena ngryc ountt enbef oreyo uspea kifve ryang ryanh undre 
d

-------------------------------- Exercise 1.2. ---------------------------------
a)
ithin kthat ishal lneve rseea billb oardl ovely asatr ee

b)
lovei snotl ovewh ichal tersw henit alter ation finds 

c)
inbai tinga mouse trapw ithch eesea lways leave roomf orthe 
mouse 

...
```

It has been a goal to include useful type-hints in the signatures all functions and methods, no matter how small or inconsequential. To check for typing consistency, make sure to have [MyPy](https://github.com/python/mypy) installed and run
```
$ mypy *.py
```

All files are (hopefully) also formatted nicely using [Black](https://github.com/psf/black).
