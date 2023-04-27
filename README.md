<h1 align="center" style="border-bottom:none;">Memory/Cache Hierarchy Optimizations for Graph Analytics</h1>
<h3 align="right">By Team <b>CST</b></h3>
<br>

# Members - CST
- Dheer Banker (210070028)
- Rahul Kumar (210050128)
- Kanad Shende (210050078)

# Overview
Through this project, we aim to analyze performance of memory hierarchies with various configurations on some popular graph processing workloads.

# Project Structure
Majority of the project structure is similar to that of ChampSim, with the following additions:
- `results`: Contains the simulation results on various memory hierarchies that we have experimented with. Also contains a helper code  that parses the simulation results and plots them on a graph. The subfolder `bak` contains the results from the previous runs.
- `automate.py`: A python script that automates the process of running the simulator on various memory hierarchies and generates the results.

Details and more information about using the ChampSim simulator is present in the `README_ChampSim.md` file.

# Running Details
## Cache Implementations
Two more types of cache implementations: Inclusive and Exclusive Caches
Macros for each of the cache implementations have been defined:
- Inclusive: `CT_INCLUSIVE`
- Exclusive: `CT_EXCLUSIVE`
- Non-inclusive: `CT_NONINCLUSIVE`
Define at most one of them at once (keep the other two commented) and the respective cache behaviour will be activated when you build the code next time.

## Using utility code
`automate.py` is the automation code we used to automate the process of running multiple build and run tasks in order to efficiently run many simulations for collecting the requisite data.
Ensure that you have downloaded the requisite traces (BFS, CC, SSSP: can find the names in gitignore) and run `python3 automate.py`

`plot.py` is the python code used to automate the repetitive task of parsing the simulation results of the latest runs and making plots out of the required data into png files.

# Project Presentation and Report
- [Project Presentation (Google Slides)](https://docs.google.com/presentation/d/1KdDs5tPIJus9dI6htR88me-ySZX24gyO3jsOOpupwn0/edit?usp=sharing)
- [Project Video (YouTube)](https://youtu.be/5NDiClrN8yI)
