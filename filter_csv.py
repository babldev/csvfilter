import argparse
import csv
import re
import sys
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional


class Filter:
    def include_row(self, row: Dict[str, str], row_number: int) -> bool:
        raise NotImplementedError


@dataclass
class ColumnHashFilter(Filter):
    column: str
    filter_every: int

    def include_row(self, row: Dict[str, str], row_number: int) -> bool:
        result = hash(row[self.column]) % self.filter_every
        return result == 0


@dataclass
class ColumnValueFilter(Filter):
    column: str
    value: str

    def include_row(self, row: Dict[str, str], row_number: int) -> bool:
        return row[self.column] == self.value


@dataclass
class RowFilter(Filter):
    filter_every: int

    def include_row(self, row: Dict[str, str], row_number: int) -> bool:
        return row_number % self.filter_every == 0


# Filter format:    --filter column=value/filter_every
#
# Example:          --filter id/100
#                   Filters for 1 in 100 id values
#
#                   --filter state=md
#                   Filters for column "state" being value "md"
#
#                   --filter /100
#                   Filters every 100 rows

COLUMN_HASH_FILTER = re.compile(r"(?P<column>.+)/(?P<filter_every>\d+)")
COLUMN_VALUE_FILTER = re.compile(r"(?P<column>.+)=(?P<value>.+)")
ROW_FILTER = re.compile(r"/(?P<filter_every>\d+)")


def parse_filter(input_str: str) -> Optional[Filter]:
    match = COLUMN_HASH_FILTER.match(input_str)
    if match:
        return ColumnHashFilter(
            column=match.group("column"), filter_every=int(match.group("filter_every"))
        )
    match = COLUMN_VALUE_FILTER.match(input_str)
    if match:
        return ColumnValueFilter(
            column=match.group("column"), value=match.group("value")
        )
    match = ROW_FILTER.match(input_str)
    if match:
        return RowFilter(filter_every=int(match.group("filter_every")))
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter a data CSV")
    parser.add_argument("input_file", help="input CSV file")
    parser.add_argument(
        "-f", "--filter", dest="filters", action="append", help="column=value/filter"
    )
    args = parser.parse_args()

    filters: List[Filter] = []
    for filter_str in args.filters:
        parsed_filter = parse_filter(filter_str)
        if parsed_filter:
            filters.append(parsed_filter)

    with open(args.input_file, "r") as f:
        csv_reader = csv.DictReader(f)
        header_written = False
        row_i = 0
        for row in csv_reader:

            if not header_written and csv_reader.fieldnames:
                # One row must be read first
                writer = csv.DictWriter(sys.stdout, fieldnames=csv_reader.fieldnames)
                writer.writeheader()
                header_written = True

            include_row = True

            for row_filter in filters:
                if not row_filter.include_row(row=row, row_number=row_i):
                    include_row = False
                    break

            if not include_row:
                continue

            writer.writerow(row)


if __name__ == "__main__":
    main()
