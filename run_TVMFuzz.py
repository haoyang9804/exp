import subprocess
import os
import time

Max_hours = 5
res_dir = res_dir = f"{Max_hours}h_tvmfuzz"

if not os.path.exists(res_dir):
    os.mkdir(res_dir)
begin_time = time.time()
cnt = 0
while True:
    cnt += 1
    end_time = time.time()
    if end_time - begin_time > Max_hours * 3600:
        break
    subprocess.run(f"python run.py", shell=True, stdout=subprocess.PIPE)
    subprocess.run(f"cp byproduct/program.py {res_dir}/{cnt}.py", shell=True, stdout=subprocess.PIPE)
