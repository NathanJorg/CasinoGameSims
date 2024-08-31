import pandas as pd
import numpy as np
import os

from pathlib import Path

class WriteToFile:

    @staticmethod
    def write_to_csv(data, filename, headers):
        df = pd.DataFrame(data, columns=headers)
        Path(filename).unlink(missing_ok=True)

        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        df.to_csv(filename, sep='\t', encoding='utf-8', index=False, header=True)

    @staticmethod
    def write_to_file(data, filename, headers):
        df = pd.DataFrame(data, columns=headers)
        df = df.replace(np.nan, '')

        Path(filename).unlink(missing_ok=True)

        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(df.to_string(index=False))  