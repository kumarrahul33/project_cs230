import os
import re
import fileinput
import subprocess

# Define the pattern to search for and the replacement string
# pattern = re.compile(r'\bword\b')
DEFAULTS = {
    'L1D_WAY': 8,
    'L2C_WAY': 8,
    'LLC_WAY': 16,
    'L1D_SET': 64,
    'L2C_SET': 1024,
    'LLC_SET': 2048 
}
BUILD_COMMAND = './build_champsim.sh bimodal no no no next_line lru 1'
BASE_COMMAND = './run_champsim.sh bimodal-no-no-no-next_line-lru-1core 30 60 '

def set_way(way_l1, way_l2, way_llc):
    pattern_l1 = re.compile(f'#define L1D_WAY [0-9]*')
    pattern_l2 = re.compile(f'#define L2C_WAY [0-9]*')
    pattern_llc = re.compile(f'#define LLC_WAY [0-9]*')
    # make a list of these patterns
    replacement_l1 = '#define L1D_WAY {0}'.format(way_l1)
    replacement_l2 = '#define L2C_WAY {0}'.format(way_l2)
    replacement_llc = '#define LLC_WAY {0}'.format(way_llc)
    # make a list of these replacements
    replacements = [(pattern_l1,replacement_l1), 
                    (pattern_l2,replacement_l2), 
                    (pattern_llc,replacement_llc)]

    # Open the file in place for editing
    pwd = os.getcwd()
    with fileinput.FileInput(pwd+'/inc/cache.h', inplace=True) as file:
        # Loop through each line in the file
        # for line in file:
        #     # Replace the pattern with the replacement string
        #     line = pattern.sub(replacement_l1, line)
        #     # Print the modified line to the file
        #     print(line, end='')
        for line in file:
            for pattern, replacement in replacements:
                line = pattern.sub(replacement, line)
            print(line, end='')

# set_way(6)
# print(os.getcwd())
def set_sets(set_l1, set_l2, set_llc):
    replacements = [
        (re.compile(f'#define L1D_SET [0-9]*'), '#define L1D_SET {0}'.format(set_l1)),
        (re.compile(f'#define L2C_SET [0-9]*'), '#define L2C_SET {0}'.format(set_l2)),
        (re.compile(f'#define LLC_SET NUM_CPUS\*[0-9]*'), '#define LLC_SET NUM_CPUS*{0}'.format(set_llc)),
    ]
    with fileinput.FileInput('inc/cache.h', inplace=True) as file:
        for line in file:
            for pattern, replacement in replacements:
                line = pattern.sub(replacement, line)
            print(line, end='')



def run_tests_for_ways():
    # to_test = [4,16,64,128]
    to_test = [0.5,2, 1, 4, 8]
    trace_files = ["bfs-3.trace.gz", "cc-5.trace.gz", "sssp-5.trace.gz"]
    # trace_files = ["bfs-3.trace.gz", "cc-5.trace.gz"]

    for set_l1 in to_test:
        # set_way(way_l1, DEFAULTS['L2C_WAY'], DEFAULTS['LLC_WAY'])
        set_sets(int(set_l1*DEFAULTS['L1D_SET']), DEFAULTS['L2C_SET'], DEFAULTS['LLC_SET'])
        subprocess.run(BUILD_COMMAND,shell=True)
        for trace in trace_files:
            curr_command = BASE_COMMAND + trace
            subprocess.run(curr_command, shell=True)

        save_results(set_l1, 'l1')
    
    for set_l2 in to_test:
        # set_way(DEFAULTS['L1D_WAY'], way_l2, DEFAULTS['LLC_WAY'])
        set_sets(DEFAULTS['L1D_SET'], int(set_l2*DEFAULTS['L2C_SET']), DEFAULTS['LLC_SET'])
        subprocess.run(BUILD_COMMAND,shell=True)
        for trace in trace_files:
            curr_command = BASE_COMMAND + trace
            subprocess.run(curr_command, shell=True)

        save_results(set_l2, 'l2')

    for set_llc in to_test:
        # set_way(DEFAULTS['L1D_WAY'], DEFAULTS['L2C_WAY'], way_llc)
        set_sets(DEFAULTS['L1D_SET'], DEFAULTS['L2C_SET'], int(set_llc*DEFAULTS['LLC_SET']))
        subprocess.run(BUILD_COMMAND,shell=True)
        for trace in trace_files:
            curr_command = BASE_COMMAND + trace
            subprocess.run(curr_command, shell=True)

        save_results(set_llc, 'llc')


def save_results(way, cache):
    # if directory resutls does not exist, create it
    if not os.path.exists('results'):
        os.makedirs('results')
    # if directory for the cache_way does not exist, create it
    if not os.path.exists('results/{0}_{1}'.format(cache, way)):
        os.makedirs('results/{0}_{1}'.format(cache, way))
    
    # move the results to the directory
    subprocess.run('mv results_60M/*.txt results/{0}_{1}'.format(cache, way), shell=True)

# run_tests_for_ways()
def set_default():
    # set_way(DEFAULTS['L1D_WAY'], DEFAULTS['L2C_WAY'], DEFAULTS['LLC_WAY'])
    set_sets(DEFAULTS['L1D_SET'], DEFAULTS['L2C_SET'], DEFAULTS['LLC_SET'])
# set_default()

 
run_tests_for_ways()




