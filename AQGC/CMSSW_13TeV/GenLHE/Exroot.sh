#!/bin/bash



outdir=condorOut


if [ ! -d $outdir/roots ]; then mkdir -p $outdir/roots; fi

#flist=`ls -1 $outdir`
flist=$@

for f in $flist
do
f_base=`basename $f`

echo $f_base
outname=`echo ${f_base} | awk -F '.' '{print $1}'`
/x5/cms/jwkim/MG5_aMC_v2_7_3/ExRootAnalysis/ExRootLHEFConverter $outdir/$f_base  $outdir/roots/${outname}.root
done





