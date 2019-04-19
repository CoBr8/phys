grep Lysander shakespeare-midsummer-16.txt| wc -l

grep Lysander shakespeare-midsummer-16.txt| grep love | wc -l

grep Lysander shakespeare-midsummer-16.txt| grep love | wc -w

set -- `du -sh shakespeare-midsummer-16.txt`
echo ${1:0:3}

set -- `grep passion ./shakespeare-midsummer-16.txt|grep dear`
echo $6

echo -n $6|wc -m

sed s/"egeus"/"dad"/Ig shakespeare-midsummer-16.txt > midsummer_dad.txt
grep dad midsummer_dad.txt|wc -l
