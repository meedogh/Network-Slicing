from Environment import run_env_rl
from memory_profiler import profile
from Environment import run_fifo
# from Greedy import run_env_greedy
# from FairDistribuition import run_env_fair_distribuition
import gc

# from Environment.utils.period import Period

gc.set_debug(gc.DEBUG_UNCOLLECTABLE) # Enable debugging of circular references

def main():
    env = run_env_rl.Environment("period3")
    env.run()


if __name__ == '__main__':
    main()





