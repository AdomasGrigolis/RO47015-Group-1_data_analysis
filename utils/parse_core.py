import os, json, sys
import pandas as pd

def parse_data(data_dir=os.path.join(os.getcwd(), 'data')):
    data_directory=os.path.join(data_dir, 'json_logs')
    records = []
    for fname in os.listdir(data_directory):
        if 'trial' in fname.lower():
            continue
        if fname.endswith('.json'):
            fpath = os.path.join(data_directory, fname)
            with open(fpath, 'r') as f:
                data = json.load(f)
                round_data = data.get('round_data', {})
                t_val = round_data.get('t')
                mse_val = round_data.get('mse')
                record = {
                    'participantID': str(round_data.get('id', '')),
                    'condition': str(round_data.get('mode', '')),
                    'time': float(t_val) if t_val is not None else float('nan'),
                    'error': float(mse_val) if mse_val is not None else float('nan')
                }
                records.append(record)
    df_long = pd.DataFrame(records, columns=['participantID', 'condition', 'time', 'error'])
    return df_long

if __name__ == "__main__":
    df_long = parse_data()
    print(df_long.head())