import pandas as pd
import numpy as np

def get_random_df():
    data = np.random.randn(4,3)
    df = pd.DataFrame(data, columns=["col1", "col2", "col3"])
    return df
