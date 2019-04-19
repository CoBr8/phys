cd ~/mp248-course-notes
find . -type f > ~/mp248/Exams/Final/listing.short
ls -R > ~/mp248/Exams/Final/listing.long
file="../mp248/Exams/Final/listing.short"
file2="../mp248/Exams/Final/listing.long"
grep -e ".ipynb" $file2 | wc -l > ~/mp248/Exams/Final/shell_answer.txt
sed s/".ipynb"/".newsuffix"/g $file2 >~/mp248/Exams/Final/listing.changed
echo Files were created/edited in my final exam directory!
