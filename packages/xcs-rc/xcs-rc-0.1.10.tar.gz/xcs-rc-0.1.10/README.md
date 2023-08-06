## XCS-RC

*Accuracy-based Learning Classifier Systems* with **Rule Combining** mechanism, shortly `XCS-RC` for Python3, loosely based on Martin Butz's XCS Java code (2001). Read my PhD thesis [here](https://publikationen.bibliothek.kit.edu/1000046880) for the complete algorithmic description.

*Rule Combining* is novel function that employs inductive reasoning, replacing ~~all Darwinian genetic operation like mutation and crossover~~. It can handle `binaries` and `real`, reaching better *correctness rate* and *population size* quicker than (mostly?) other XCS instances. My earlier papers comparing them can be obtained at [here](https://link.springer.com/chapter/10.1007/978-3-642-17298-4_30) and [here](https://dl.acm.org/citation.cfm?id=2331009).

---

**Initialization**
```
import xcs_rc
agent = xcs_rc.Agent()
```

**For classical Reinforcement Learning cycles**
```
action = agent.next_action(input, explore=True)  
# assign reward here  
agent.apply_reward(reward)  
```

**Or, for training and testing with a set of data**
```
agent.train(X_train, y_train)
# get the confusion matrix with test data
cm = agent.test(X_test, y_test)
```

**Print population, save it to CSV file, or use append mode**
```
agent.print_pop(title="Population")
agent.save_popfile('xcs_population.csv', title="Final XCS Population")
agent.save_popfile('xcs_pop_every_100_cycles.csv', title="Cycle: ###", save_mode='a')
```

**Finally, inserting rules to population**
```
agent.insert_to_pop("xcs_population.csv") # from a file, or
agent.insert_to_pop(my_list_of_rules) # from a list of classifiers
```

  
**New Parameters**
* **tcomb**: *combining period*, after how many learning cycles the new technique will be applied
* **predtol**: *prediction tolerance*, the maximum difference between two classifiers to be combined
* **prederrtol**: prediction error tolerance, threshold for rule deletion, indicated inappropriate combining


**How to Set**
```
agent.tcomb = 50 # perform rule combining every 50 cycles
agent.predtol = 20.0 # combines rules whose prediction value differences <= 20.0
agent.prederrtol = 10.0 # remove combine results having error > 10.0
```


**Removed/unused parameters from original XCS**
* ~~all related to mutation and crossover~~

---

**Links**
* [Github](https://github.com/nuggfr/xcs-rc-python)
* [Example](https://routing.nuggfr.com/churn)
