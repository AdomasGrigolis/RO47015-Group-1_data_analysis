import os
import json
import random
from datetime import datetime

# The purpose of this script is to generate fake JSON data
# for demonstration or testing purposes.

def generate_fake_json_files(
    out_dir,
    n_participants=5,
    n_modes=3,
    n_files_per_participant=1
):
    os.makedirs(out_dir, exist_ok=True)
    for pid in range(1, n_participants + 1):
        participant_id = f"{pid:02d}"
        for mode in range(n_modes):
            for _ in range(n_files_per_participant):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
                filename = f"{participant_id}_{mode}_{timestamp}.json"
                data = {
                    "round_data": {
                        "id": participant_id,
                        "mode": mode,
                        "t": round(random.uniform(100, 200), 6),
                        "mse": round(random.uniform(500, 1500), 6)
                    }
                }
                with open(os.path.join(out_dir, filename), "w") as f:
                    json.dump(data, f)

if __name__ == "__main__":
    output_dir = os.path.join(os.getcwd(), "data", "json_logs")
    generate_fake_json_files(output_dir, n_participants=10, n_modes=3, n_files_per_participant=1)