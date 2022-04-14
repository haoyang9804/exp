import os
import subprocess
import collect_cov_c
import multiprocessing as mp
from analyze_cov import collect_all


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
    all_line_cov_res_list = {}
    level_list = [0, 1, 2]
    for level in level_list:
        # clear C coverage info
        collect_cov_c.init()
        exccmd(f'rm  .coverage')
        exccmd(f'rm  .coverage.*')  # remove history .coverage
        exccmd(f"rm ./*.gcov")
        all_line_cov_res_list[level] = []
        comGraph_dir = f"/share_container/pycharmProjects/OOPSLA22/coverage-GenGraph/result-cov/nodes_graph/_exp_results-{level}"

        for output in range(50):
            res_path = f"./result-cov/res-node_graph_cov/{level}/{output}"
            res_path_python = os.path.join(res_path, 'python')
            res_path_c = os.path.join(res_path, 'c')
            if not os.path.exists(res_path_python):
                os.makedirs(res_path_python)
            if not os.path.exists(res_path_c):
                os.makedirs(res_path_c)

            script_file = os.path.join(comGraph_dir, f"output{output}.py")
            single_work(script_file)

            # collect python coverage here
            exccmd(f"mv .coverage .coverage.2")
            exccmd(f'coverage combine')
            exccmd(f'coverage json')

            exccmd(f'cp .coverage {res_path_python}/.coverage')
            exccmd(f'mv coverage.json {res_path_python}/coverage.json')

            # collect c/c++ coverage
            collect_cov_c.cov()
            subprocess.run('cp *.gcov {}'.format(res_path_c), shell=True, stdout=subprocess.PIPE)

            #  get_the line coverage number
            all_cov_line = collect_all(res_path)

            all_line_cov_res_list[level].append(all_cov_line)
    print(all_line_cov_res_list)
