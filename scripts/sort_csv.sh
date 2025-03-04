(head -n 1 ../output/names_by_year.csv && tail -n +2 ../output/names_by_year.csv | sort -t, -k2 -n) > temp.csv && mv temp.csv ../output/names_by_year.csv
