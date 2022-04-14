import os
import subprocess
import logging
logging.basicConfig(filename='coverage_cpp.log', level=logging.INFO)


def exccmd(com):
    # print(f"run commend: {com}")
    r = []
    p = os.popen(com, 'r')
    lines = p.readlines()  # return a list, but each item end with '\n'
    for line in lines:
        r.append(line.strip())
    return r


def Red(string):
    return '\033[1;31m' + string + '\033[0m'


def Blue(string):
    return '\033[1;34m' + string + '\033[0m'


srcpaths = ['/workplace/software/tvm/tvm/build/CMakeFiles/tvm_objs.dir/src/',
            '/workplace/software/tvm/tvm/build/CMakeFiles/tvm_runtime_objs.dir/src/runtime/']


def init():
    for gcdapath in srcpaths:
        cmd = "find {} -name '*.gcda' -type f | xargs rm -rf".format(gcdapath)
        print(cmd)
        status = os.system(cmd)
        # subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
        if status:
            raise Exception('Fail in deleting gcda files')


def deal(srcpath, sl):
    if sl.endswith('.gcno'):
        elename = sl[:-5]
        elename = elename+".o"
        string = 'llvm-cov gcov -p -b -f ' + os.path.join(srcpath, elename)  # -p : get full path/ -b: branch cov;
        # string = 'gcov -p ' + os.path.join(srcpath, elename)
        subprocess.run(string, shell=True, stdout=subprocess.PIPE)
        # exccmd(string)

    elif os.path.isdir(os.path.join(srcpath, sl)):
        path = os.path.join(srcpath, sl)
        elelist = os.listdir(path)

        for ele in elelist:
            deal(path, ele)


def cov():
    res = ''
    for srcpath in srcpaths:
        srclist = os.listdir(srcpath)
        for sl in srclist:
            if '3rdparty' in sl:
                continue
            deal(srcpath, sl)
    return res


if __name__ == '__main__':
    gcovpath = './result-cov/c-cov-comGraph'
    if not os.path.exists(gcovpath):
        os.makedirs(gcovpath)
    res = cov()
    subprocess.run('mv *.gcov {}'.format(gcovpath), shell=True, stdout=subprocess.PIPE)
    logging.info('Finish.')
