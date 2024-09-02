# %%
import os
import utils.experiment
import utils.dirtools
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# %%
from config import config_vars

experiment_name = 'impact_of_augmented_dataset_size'

partition = "validation"

total_repetitions = 5

config_vars = utils.dirtools.setup_experiment(config_vars, experiment_name)

config_vars

# %%
results = pd.DataFrame(columns=["Samples", "Repeat", "F1","Jaccard", "Missed", "Merges", "Splits"])
idx = 0

for max_samples in [2, 4, 6, 8, 10, 20, 40, 60, 80, 100]:
    for repetition in range(total_repetitions):
        print("Experiment", idx, "- max_samples:", max_samples, "- repetition:", repetition)
        
        # Modify settings
        config_vars["max_training_images"] = max_samples
    
        # Reconfigure variables and data partitions
        config_vars = utils.dirtools.setup_experiment(config_vars, experiment_name)
        data_partitions = utils.dirtools.read_data_partitions(config_vars)
        
        # Run experiment
        output = utils.experiment.run(config_vars, data_partitions, experiment_name, partition, GPU="0")
        print(output["F1"])
        print(output["Jaccard"])
        # Collect outputs
        record = {
            "Samples": max_samples,
            "Repeat": repetition,
            "F1": output["F1"],
            "Jaccard": output["Jaccard"],
            "Missed": output["Missed"].sum(),
            "Merges": output["Merges"],
            "Splits": output["Splits"]
        }
        results.loc[idx] = record
        idx += 1
        
        # Clean up directories
        experiment_dir = config_vars["root_directory"] + "/experiments/" + experiment_name
        if os.path.exists(experiment_dir):
            os.system("rm -Rf " + experiment_dir)
            
        # Save results
        results.to_csv(config_vars["root_directory"] + "/experiments/" + experiment_name + ".csv")

# %%
results = pd.read_csv(config_vars["root_directory"]+"/experiments/impact_of_augmented_dataset_size.csv")
mean = results.groupby("Samples").mean().reset_index()
sem = results.groupby("Samples").sem().reset_index()
sem.columns = [c+"_se" for c in sem.columns]
data = pd.concat([mean, sem], axis=1).drop(["Samples_se", "Repeat", "Repeat_se"], axis=1)
data

# %%
plt.figure(figsize=(8,8))
plt.errorbar(x=data["Samples"], y=data["Missed"], yerr=data["Missed_se"])
plt.xscale("log")

# %%



