import subprocess
import time

start = time.time()
n_runs = 0

while time.time() - start < 3600:
    print(f"run: {n_runs}")
    subprocess.call(["timeout", "60", "python3", "hillclimber.py"])
    n_runs += 1
