import os
import subprocess
import collect_cov_c
import multiprocessing as mp


def exccmd(com):
    print(f"run commend: {com}")
    res = []
    p = os.popen(com, 'r')
    lines = p.readlines()  # return a list, but each item end with '\n'
    for line in lines:
        res.append(line.strip())
    return res


def single_work(script_path):
    if not os.path.exists(script_path):
        assert False, f"file path {script_path} is not exist!"
    cmd_str = f"coverage run -p {script_path}"
    exccmd(cmd_str)
    print("finish ", script_path)


if __name__ == '__main__':
    # clear C coverage info
    collect_cov_c.init()
    exccmd(f'rm  .coverage')
    exccmd(f'rm  .coverage.*')  # remove history .coverage
    exccmd(f"rm ./*.gcov")
    # comGraph_dir = "./result-cov/5min_comGraph"
    # res_path = './result-cov/res-comGraph-cov2'
    comGraph_dir = "/workplace/software/tvm/tvm/tests/python/relay"
    res_path = "./result-cov/unit-test"

    # comGraph_dir = "result-cov/5h_tvmfuzz"
    # res_path = './result-cov/res-tvmFuzz_cov'
    cnt = 1
    res_path_python = os.path.join(res_path, 'python')
    res_path_c = os.path.join(res_path, 'c')
    if not os.path.exists(res_path_python):
        os.makedirs(res_path_python)
    if not os.path.exists(res_path_c):
        os.makedirs(res_path_c)

    all_task_list = []
    for comGraph in os.listdir(comGraph_dir):
        if not comGraph.endswith(".py"):
            continue

        comGraph_path = os.path.join(comGraph_dir, comGraph)
        all_task_list.append(comGraph_path)
    print("length of the task is ", len(all_task_list))

    core_num = 2
    for i in range(0, len(all_task_list) + core_num, core_num):
        p_list = []
        for j in range(0, core_num, 1):
            this_cnt = i + j
            if this_cnt >= len(all_task_list):
                break
            p1 = mp.Process(target=single_work, args=(all_task_list[this_cnt],))
            p_list.append(p1)
            p1.start()
        for p in p_list:
            p.join()

    # collect python coverage here
    exccmd(f'coverage combine')
    exccmd(f'coverage json')

    exccmd(f'cp .coverage {res_path_python}/.coverage')
    exccmd(f'mv coverage.json {res_path_python}/coverage.json')

    # collect c/c++ coverage
    collect_cov_c.cov()
    subprocess.run('mv *.gcov {}'.format(res_path_c), shell=True, stdout=subprocess.PIPE)
