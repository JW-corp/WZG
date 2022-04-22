#!/bin/basj


flist=`ls -1 cards_SR_2016/*.txt`


combineCards.py $flist >& combine_data.txt

