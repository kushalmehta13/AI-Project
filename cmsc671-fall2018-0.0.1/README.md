# CMSC 671 (Fall 2018) Final project

Code for the final project of CMSC 671 course (Fall 2018)

To run the code, use the following command:
```bash
$ python play.py --height 10 --width 10 \
  --num-powerups 2 --num-monsters 1 \
  --initial-strength 100 \
  --save-dir map1/ \
  --verbose
```

To implement a new agent, create a new agent class inheriting from the `BaseAgent` class in the `agent.py` file. You just need to implement the `step(...)` function. See a look at how `RandomAgent` has been implemented.
