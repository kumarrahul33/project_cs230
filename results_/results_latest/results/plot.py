import re
import os

MULTIPLIERS = [0.5,1,2, 4, 8]

def get_file_directory(cache_level):
    dirs = []
    for i in MULTIPLIERS:
        dirs.append(os.getcwd()+f"/{cache_level}_{i}/")
    return dirs

files = ["bfs-3.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt",
"cc-5.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt",
"sssp-5.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt"
]

import numpy as np
import matplotlib.pyplot as plt
pattern ={
    'cycles': r'CPU 0 cumulative IPC: [0-9.]* instructions: [0-9]* cycles: ([0-9]*)',
    # patterns for:
    # - IPC
    # - L1D, L2C, LLC miss rates (total)
    # - L1D, L2C, LLC miss rates (load)
    # - L1D, L2C, LLC miss rates (prefetch)
    # - L1D, L2C, LLC miss latency
    'l1_miss' : r'L1D TOTAL .* ([0-9]*)$',
    'l2_miss' : r'L2C TOTAL .* ([0-9]*)$',
    'llc_miss' : r'LLC TOTAL .* ([0-9]*)$',
    'l1_access' : r'L1D TOTAL .* ACCESS:[ ]*([0-9]*)',
    'l2_access' : r'L2C TOTAL .* ACCESS:[ ]*([0-9]*)',
    'llc_access' : r'LLC TOTAL .* ACCESS:[ ]*([0-9]*)',
    'l1_pmiss' : r'L1D PREFETCH .* ([0-9]*)$',
    'l2_pmiss' : r'L2C PREFETCH .* ([0-9]*)$',
    'llc_pmiss' : r'LLC PREFETCH .* ([0-9]*)$',
    'l1_paccess' : r'L1D PREFETCH .* ACCESS:[ ]*([0-9]*)',
    'l2_paccess' : r'L2C PREFETCH .* ACCESS:[ ]*([0-9]*)',
    'llc_paccess' : r'LLC PREFETCH .* ACCESS:[ ]*([0-9]*)'
}

PLOT_CONFIG = {
    'cycles': {
        'title': 'Cycles',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Cycles',
    },
    'l1': {
        'title': 'L1D total miss',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Total miss',
    },
    'l2': {
        'title': 'L2C total miss',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Total miss',
    },
    'llc': {
        'title': 'LLC total miss',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Total miss',
    },
    
    'l1_mr': {
        'title': 'L1D total miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Miss rate',
    },
    'l2_mr': {
        'title': 'L2C total miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Miss rate',
    },
    'llc_mr': {
        'title': 'LLC total miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Miss rate',
    },
    'l1_pmr': {
        'title': 'L1D Prefetch miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Prefetch Miss rate',
    },
    'l2_pmr': {
        'title': 'L2C Prefetch miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Prefetch Miss rate',
    },
    'llc_pmr': {
        'title': 'LLC Prefetch miss rate',
        'xlabel': 'Size (multiple of baseline)',
        'ylabel': 'Prefetch Miss rate',
    },
}

x  = np.arange(len(MULTIPLIERS))
data = [str(i) for i in MULTIPLIERS]
bfs_data = np.array([])
cc_data = np.array([])
sssp_data = np.array([])

def get_data(file,key):
    # res=dict()
    with open(file, "r") as f:
        for line in f:
            # for key in pattern:
            match = re.search(pattern[key], line)
            if match:
                # res[key] = match.group(1)
                res = match.group(1)
                return int(res)
    # if not len(res):
    #     return None
    
    return -1

# print(get_data(get_file_directory("l1")[0]+files[0]))
def formula(data,file,level):
    if(data == "cycles"):
        return get_data(file,"cycles")
    elif(data == "miss_rate"):
        try:
            return get_data(file,level+"_miss")*100/get_data(file,level+"_access")
        except:
            return 0
    elif(data == "pmr"):
        try:
            return get_data(file,level+"_pmiss")*100/get_data(file,level+"_paccess")
        except:
            return 0
    elif(data == "miss"):
        return get_data(file,level+"_miss")

def parse_data(level,key):
    global bfs_data
    global cc_data
    global sssp_data

    bfs_data = np.array([])
    cc_data = np.array([])
    sssp_data = np.array([])
    # for level in ['l1']:

    # for i in range(len(files)):
    for dir in get_file_directory(level):
        for file in files:

            if(file == "bfs-3.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt"):
                bfs_data = np.append(bfs_data,formula(key,dir+file,level))
            elif(file == "cc-5.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt"): 
                cc_data =  np.append(cc_data, formula(key,dir+file,level))
            elif(file == "sssp-5.trace.gz-bimodal-no-no-no-next_line-lru-1core.txt"):
                sssp_data = np.append(sssp_data,formula(key,dir+file,level))
             


# parse_data("l1","l1")
# parse_data("l1","cycles")

# parse_data("l2","l2")
def plot(fwhat="", filename="output.png", save=False, show=True):
    global bfs_data, cc_data, sssp_data
    print(bfs_data)
    bar_width = 0.2
    # bfs_data = bfs_data/np.max(bfs_data)
    # cc_data = cc_data/np.max(cc_data)
    # sssp_data = sssp_data/np.max(sssp_data)
    plt.bar(x-bar_width, bfs_data, width=bar_width, color='b', label='bfs')            
    plt.bar(x, cc_data, width=bar_width, color='g', label='cc')
    plt.bar(x+bar_width, sssp_data, width=bar_width, color='r',  label='sssp')

    plt.xlabel(PLOT_CONFIG[fwhat]['xlabel'])
    plt.ylabel(PLOT_CONFIG[fwhat]['ylabel'])
    plt.title(PLOT_CONFIG[fwhat]['title'])
    plt.xticks(x, data)
    plt.legend()
    
    if save:
        plt.savefig(filename)
    if show:
        plt.show()

    plt.clf()

RES_DIR = "plots/"

for level in ['l1','l2','llc']:
    parse_data(level, "miss")
    plot(level, filename=f"{RES_DIR}{level}_total_miss.png", save=True, show=False)
    parse_data(level, "miss_rate")
    plot(level+"_mr", filename=f"{RES_DIR}{level}_miss_rate.png", save=True, show=False)
    parse_data(level, "pmr")
    plot(level+"_pmr", filename=f"{RES_DIR}{level}_prefetch_miss_rate.png", save=True, show=False)

    # parse_data(level, "cycles")
    # plot(level, filename=f"{RES_DIR}cycles__{level}", save=True, show=False)