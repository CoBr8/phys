cd
mkdir tmp
cd tmp
touch tmp.txt
echo -e "fred\njulia\ntom\ncarol\nsam\njason\nnicole" > tmp.txt
mv tmp.txt names.txt
wc -l names.txt
grep -e 'o' -e 'mas' names.txt | wc -l
grep -e 'ol' -e 'om' names.txt | wc -l
grep -v 'o' names.txt | wc -l
cd
du
du /home/user/tmp
cp -rf /home/user/tmp  /home/user/lab/lab1/tmp
rm -rf /home/user/tmp
history -w "history.txt"
