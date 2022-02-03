# csvfilter

Python script for filtering / reducing file size of CSV files.

## Usage

See help:
```sh
python filter_csv.py --help
```

Sample every 100 rows:
```sh
python3 filter_csv.py original.csv --filter /100 > new.csv
```

Sample every every 100 rows by column hash value (columns with same id will be included):
```sh
python3 filter_csv.py original.csv --filter id/100 > new.csv
```

Filter rows by column value (column "state" is "maryland"):
```sh
python3 filter_csv.py original.csv --filter state=maryland > new.csv
```

Filter every 100 rows buy column vlaue (column "state" is "maryland")
```sh
python3 filter_csv.py original.csv --filter /100 --filter state=maryland > new.csv
```
