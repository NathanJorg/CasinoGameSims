from pathlib import Path

import os
import pandas as pd

def write_to_file(data, filename):
    df = pd.DataFrame(data)
    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
  
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(df.to_string(index=False))

def write_to_csv(data, filename):
    df = pd.DataFrame(data)
    Path(filename).unlink(missing_ok=True)

    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    df.to_csv(filename, sep='\t', encoding='utf-8', index=False, header=True)


def main():
    pass


if __name__ == "__main__":
    main()