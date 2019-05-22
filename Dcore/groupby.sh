cat core_sizes_ids* > core_sizes_all.txt
sort -V core_sizes_all.txt > sorted.txt
mv sorted.txt core_sizes_all.txt

cat author_frontiers_ids* > author_frontiers_all.csv
sort -V author_frontiers_all.csv > author_tmp.csv
mv author_tmp.csv author_frontiers_all.csv
awk 'NR==0 { print ; next } { A[$1]=A[$1]","$2 } END { for(X in A) print X,substr(A[X],2) }' author_frontiers_all.csv > author_frontiers_groupby.csv
sort -V author_frontiers_groupby.csv  > sorted_frontier.csv
mv sorted_frontier.csv author_frontiers_groupby.csv

python image.py

sort -V dcore_image.csv > sorted.csv
mv sorted.csv  dcore_image.csv
sed -i '1i group,variable,value' dcore_image.csv

python frontier_names.py
