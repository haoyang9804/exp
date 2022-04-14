import os
import subprocess
import time


def Red(string):
    return '\033[1;31m' + string + '\033[0m'


def Green(string):
    return '\033[1;32m' + string + '\033[0m'


def generate_compgraph(path):
    begintime = time.time()
    if not os.path.exists(path):
        subprocess.run(f'mkdir -p {path}', shell=True)
    fid = 1
    while True:
        endtime = time.time()
        if endtime - begintime > MAX_HOURS * 3600:
            break
        p = subprocess.run('./compgraph', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(Green(f'p.returncode = {p.returncode}'))
        if p.returncode:
            subprocess.run('mv output.py ' + path + "bug_output" + str(fid) + '.py', shell=True)
            subprocess.run('mv outputdual.py ' + path + "bug_outputdual" + str(fid) + '.py', shell=True)
        else:
            subprocess.run('mv output.py ' + path + "output" + str(fid) + '.py', shell=True)
            subprocess.run('mv outputdual.py ' + path + "outputdual" + str(fid) + '.py', shell=True)
        fid += 1
    print(Red(str(fid) + ' files have been generated in ' + str(MAX_HOURS) + ' hours'))


if __name__ == '__main__':
    MAX_HOURS = 1
    res_path = f"./result-cov/comGraph_{MAX_HOURS}h/"
    generate_compgraph(res_path)
