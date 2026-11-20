import pandas as pd
from pandas import DataFrame, Timedelta

def number_input(min,max,in_str) -> int:
    while(1):
        try:
            i = int(input(in_str))
            if min <= i <= max:
                return i
            else:
                print(f"Zahl muss zwischen {min} und {max} sein")
            
        except KeyboardInterrupt:
            raise
        except:
            print("Eingabe muss eine Zahl sein!")



def filter_gaps(df:DataFrame, max_gap:Timedelta):
    # Identify where the time difference exceeds max_gap
    df = df.sort_values('date')
    time_diff = df['date'].diff()
    gap_mask = time_diff > max_gap

    # Create gap rows with NaNs
    gap_rows = pd.DataFrame({'date': df.loc[gap_mask, 'date'] - pd.Timedelta(seconds=1)})

    # Concatenate, sort by date, and reset index
    df = pd.concat([df, gap_rows]).sort_values('date').reset_index(drop=True)
    return df
