import os
import json
import re

# This script checks the integrity of JSON files in a specified directory.

def check_json_data_integrity(data_dir):
    json_dir = os.path.join(data_dir, 'json_logs')
    pattern = re.compile(r'(\d+)_([0-2])_.*\.json$')
    issues_found = False
    participant_files = {}

    for fname in os.listdir(json_dir):
        if not fname.endswith('.json'):
            continue
        match = pattern.match(fname)
        if not match:
            print(f"Filename format issue: {fname}")
            issues_found = True
            continue
        file_pid, file_mode = match.group(1), match.group(2)
        participant_files.setdefault(file_pid, set()).add(file_mode)
        fpath = os.path.join(json_dir, fname)
        with open(fpath, 'r') as f:
            try:
                data = json.load(f)
                round_data = data.get('round_data', {})
                rd_pid = str(round_data.get('id', ''))
                rd_mode = str(round_data.get('mode', ''))
                t_val = round_data.get('t', None)
                mse_val = round_data.get('mse', None)

                if file_pid != rd_pid or file_mode != str(rd_mode):
                    print(f"ID/mode mismatch in {fname}: filename ({file_pid}, {file_mode}) vs round_data ({rd_pid}, {rd_mode})")
                    issues_found = True
                if t_val is None:
                    print(f"Missing 't' in round_data for {fname}")
                    issues_found = True
                if mse_val is None:
                    print(f"Missing 'mse' in round_data for {fname}")
                    issues_found = True
            except Exception as e:
                print(f"Error reading {fname}: {e}")
                issues_found = True

    all_modes = {'0', '1', '2'}
    valid_participants = 0
    for pid, modes in participant_files.items():
        missing = all_modes - modes
        extra = modes - all_modes
        if len(modes) == 3 and not missing and not extra:
            valid_participants += 1
        else:
            print(f"Participant {pid} has files for modes: {sorted(modes)}")
            if missing:
                print(f"  Missing modes: {sorted(missing)}")
            if extra:
                print(f"  Extra/invalid modes: {sorted(extra)}")
            issues_found = True

    if not issues_found:
        print("All JSON files passed integrity checks.")
    print(f"Number of valid participants with all 3 modes: {valid_participants}")
    return valid_participants

if __name__ == "__main__":
    data_directory = "./data"
    check_json_data_integrity(data_directory)