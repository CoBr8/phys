file_name='shakespeare-midsummer-16.txt'
grep -e 'Lysander' $file_name | wc -l
grep -e 'Lysander' $file_name | grep -e 'love' | wc -l
grep -e 'Lysander' $file_name | grep -e 'love' | wc -w
du -k $file_name | cut -f 1


line=$(grep -e 'passion' $file_name | grep -e 'dear')
set -- $line
echo $6
echo $6 |tr -d '\n'| wc -c 


file_two='midsummer_dad.txt'
sed -e s/"EGEUS"/"dad"/g -e s/"Egeus"/"dad"/g $file_name > $file_two 

grep -e 'dad' $file_two | wc -l 
