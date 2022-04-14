#-*- coding : utf-8-*-
import os
import json


def get_package_name(gcovfilepath):
    short_file_name = gcovfilepath[len("#workplace#software#tvm#tvm"):]
    if "relay" in short_file_name:
        this_package_name = "relay"
    elif "tir" in short_file_name:
        this_package_name = "tir"
    elif "topi" in short_file_name:
        this_package_name = "topi"
    elif "te" in short_file_name:
        this_package_name = "te"

    elif "auto_scheduler" in short_file_name:
        this_package_name = "auto_scheduler"
    elif "autotvm" in short_file_name:
        this_package_name = "autotvm"
    # elif "meta_schedule" in short_file_name:
    #     this_package_name = "meta_schedule"
    elif "contrib" in short_file_name:
        this_package_name = "contrib"
    elif "runtime" in short_file_name:
        this_package_name = "runtime"
    elif "target" in short_file_name:
        this_package_name = "target"
    elif "ir" in short_file_name:
        this_package_name = "ir"
    elif "arith" in short_file_name:
        this_package_name = "arith"
    else:
        this_package_name = "other"
        # print(short_file_name)
    return this_package_name


def get_python_cov(cov_json):
    package_cov = {}
    cov_lines = dict()
    with open(cov_json, 'r') as f:
        json_dict = json.load(f)
        json_dict = json_dict["files"]
    for cov_f in json_dict.keys():
        if "__init__.py" in cov_f or "testing" in cov_f:
            continue
        this_package = get_package_name(cov_f)
        short_file_name = cov_f[len("#workplace#software#tvm#tvm"):]
        cov_lines[cov_f] = json_dict[cov_f]['executed_lines']
        # print(cov_lines)
        if this_package not in package_cov.keys():
            package_cov[this_package] = []
        # package_cov[this_package].extend(cov_f + cov_lines[cov_f])
        for line in cov_lines[cov_f]:
            package_cov[this_package].append(short_file_name + '_' + str(line))
    print("python coverage.....")
    for k, v in package_cov.items():
        print(k, len(v))
    return package_cov


def get_package_cov_info(res_dir):
    cov_res_file = os.path.join(res_dir, "cstmt_info.txt")
    # fun_cov_file = os.path.join(res_dir, "cfun_info.txt")
    all_package_dict = {}
    with open(cov_res_file) as f:
        lines = f.readlines()
        for line in lines:
            file_name = line.split(":")[0]
            cov_res = line.split(":")[1]
            cov_line_id_list = cov_res.split(',')
            short_file_name = file_name[len("#workplace#software#tvm#tvm"):]
            this_package = get_package_name(file_name)
            if this_package not in all_package_dict.keys():
                all_package_dict[this_package] = []
            for line in cov_line_id_list:
                all_package_dict[this_package].append(short_file_name + '_' + str(line))
    # print("c coverage.....")
    # for k, v in all_package_dict.items():
    #     print(k, len(v))
    return all_package_dict


def collect_all(gcovpath):
    # all_function_num = 0
    # covered_fun = 0

    all_source_LOC = 62862   # python all line in tvm
    covered_LOC = 0

    python_cov_dir = os.path.join(gcovpath, 'python')
    python_cov_dict = get_python_cov(os.path.join(python_cov_dir, "coverage.json"))
    python_cov_all_line = 0
    for v in python_cov_dict.values():
        python_cov_all_line += len(v)
    print("all python line is :", python_cov_all_line)

    covered_LOC += python_cov_all_line
    all_package_cov_dict = python_cov_dict

    cov_path = os.path.join(gcovpath, "c")

    stmt_info_path = cov_path + 'stmt_info.txt'
    fun_info_path = cov_path + 'fun_info.txt'
    stmtfile = open(stmt_info_path, 'w')
    funfile = open(fun_info_path, 'w')

    gcovfilepaths = os.listdir(cov_path)

    for gcovfilepath in gcovfilepaths:
        if "3rdparty" in gcovfilepath or not gcovfilepath.startswith("#workplace#software#tvm#tvm"):
            continue
        fullpath = os.path.join(cov_path, gcovfilepath)

        gcovfile = open(fullpath, 'r')
        gcovlines = gcovfile.readlines()

        tmp = []
        tmp_fun = []

        for gcovline in gcovlines:
            gcovline = gcovline.strip()
            # if gcovline.startswith('function'):
            #     all_function_num += 1
            #     is_called = gcovline.split(" ")[-6].strip() != '0'
            #     covered_fun += is_called
            #     if is_called:
            #         fun_name = gcovline.split(' ')[1].strip()
            #         tmp_fun.append(fun_name)
            # else:  # line
            if ':' not in gcovline:
                continue
            covcnt = gcovline.split(':')[0].strip()
            linenum = gcovline.split(':')[1].strip()
            if covcnt != '-' and covcnt != '#####':
                tmp.append(linenum)
            if covcnt != '-':
                all_source_LOC += 1

        if len(tmp) > 0:
            stmtfile.write(gcovfilepath + ':' + ','.join(tmp) + '\n')
            covered_LOC += len(tmp)
        if len(tmp_fun) > 0:
            funfile.write(gcovfilepath+':'+','.join(tmp_fun)+'\n')
    print("line coverage: ", covered_LOC, all_source_LOC, covered_LOC/all_source_LOC)
    return covered_LOC
    # print("func coverage: ", covered_fun, all_function_num, covered_fun/all_function_num)
'''

    c_package_cov_dict = get_package_cov_info(gcovpath)
    for k, v in c_package_cov_dict.items():
        if k in all_package_cov_dict.keys():
            all_package_cov_dict[k].extend(v)
        else:
            all_package_cov_dict[k] = v
    # the c++ coverage:
    total_line_c = 0
    for v in c_package_cov_dict.values():
        total_line_c += len(v)
    print("------coverage for C/C++ is : ", total_line_c, "-----------")
    dict_to_file(all_package_cov_dict, gcovpath)
    return all_package_cov_dict
'''

def dict_to_file(package_cov_all, res_dir):
    res_file = os.path.join(res_dir, "line_cov.txt")
    with open(res_file, 'w', encoding='utf-8') as f:
        for v in package_cov_all.values():
            for line in v:
                f.write(line + '\n')
    f.close()


if __name__ == '__main__':
    # gcovpath = './result-cov/res-comGraph-cov'
    # gcovpath = "./result-cov/res-tvmFuzz_cov"
    gcovpath = "./result-cov/unit-test"
    package_cov_all = collect_all(gcovpath)
    print("total coverage...................")
    for k, v in package_cov_all.items():
        print(k, len(v))
    dict_to_file(package_cov_all, gcovpath)
    # print(package_cov_all)
    # get_package_cov_info(gcovpath)
    # get_python_cov("coverage.json")

