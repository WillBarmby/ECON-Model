import csv
from config.paths import PARAMETERS
from params import Params
from typing import cast

ParsedParams = dict[str, str | float]


def read_parameters(file_name: str, skip_header=True) -> ParsedParams:
    params: ParsedParams = {}

    with open(file_name, newline="") as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        reader = csv.reader(f, dialect=dialect)
        f.seek(0)

        if skip_header:
            header = next(reader)

        for row in reader:
            key = row[1].strip()
            raw_value = row[2].strip()

            if not any(row):
                continue
            try:
                value: str | float = float(raw_value)
            except ValueError:
                value = raw_value
            params[key] = value

    return params


def validate_params(parsed: ParsedParams) -> Params:
    required = {
        "c_0",
        "c_1",
        "b_0",
        "b_1",
        "b_2",
        "T",
        "G",
        "x",
        "phi_pi",
        "phi_y",
        "pi_target",
        "m",
        "z",
        "alpha",
        "L",
        "pi_e_0",
    }
    missing = required - set(parsed.keys())
    if missing:
        raise ValueError(f"Missing parameters: {missing}")
    for key in required:
        if not isinstance(parsed[key], float):
            raise TypeError(f"{key} must be float")

    return cast(Params, parsed)


if __name__ == "__main__":
    dict = read_parameters(str(PARAMETERS))
    print(dict)
