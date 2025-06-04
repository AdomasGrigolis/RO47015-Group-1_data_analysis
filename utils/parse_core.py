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
    df_long = attach_trial_id(data_dir, df_long)
    return df_long

def attach_trial_id(data_dir, df_long):
    order_path = os.path.join(data_dir, 'other', 'order.xlsx')
    order_df = pd.read_excel(order_path, skiprows=1)

    # Ensure participantID is zero-padded strings in both dataframes
    order_df['participantID'] = order_df['participantID'].apply(lambda x: str(x).zfill(2))
    df_long['participantID'] = df_long['participantID'].apply(lambda x: str(x).zfill(2))

    # Build mapping: participantID -> {mode: trial_number}
    order_map = {}
    for _, row in order_df.iterrows():
        pid = str(row['participantID'])
        mode_to_trial = {}
        for i, cond_col in enumerate(['condA', 'condB', 'condC'], 1):
            val = row[cond_col]
            if pd.notna(val):
                mode_to_trial[str(int(val))] = i
        order_map[pid] = mode_to_trial

    trial_id_list = []
    for idx, row in df_long.iterrows():
        pid = str(row['participantID'])
        try:
            cond = str(int(float(row['condition'])))
        except Exception:
            cond = str(row['condition'])
        trial_id = order_map.get(pid, {}).get(cond, None)
        trial_id_list.append(trial_id)
    df_long['trialID'] = pd.Series(trial_id_list, dtype="Int64")
    
    # Warn about missing participants
    data_pids = set(df_long['participantID'])
    order_pids = set(order_map.keys())
    missing_in_order = data_pids - order_pids
    if missing_in_order:
        print(f"Warning: These participantIDs are in your data but not in the order file: {sorted(missing_in_order)}")
    extra_in_order = order_pids - data_pids
    if extra_in_order:
        print(f"Note: These participantIDs are in the order file but not in your data: {sorted(extra_in_order)}")

    return df_long

if __name__ == "__main__":
    df_long = parse_data()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df_long)