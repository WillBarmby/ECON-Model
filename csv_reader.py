import csv
from config.paths import PARAMETERS


def read_parameters(file_name: str, skip_header=True):
    params_dict = {}
    with open(file_name, newline="") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, dialect=dialect)
        f.seek(0)
        if skip_header:
            header = next(reader)
        for row in reader:
            if not any(row):
                continue
            try:
                params_dict[row[1]] = float(row[2])
            except ValueError:
                params_dict[row[1]] = row[2]
    return params_dict


def read_shocks(file_name: str):
    with open(file_name, newline="") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, dialect=dialect)
        rows = []
        for row in reader:
            if not any(row):
                continue
            rows.append(row)
    return rows


if __name__ == "__main__":
    dict = read_parameters(str(PARAMETERS))
    print(dict)
