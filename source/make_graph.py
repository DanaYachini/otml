from pathlib import Path
import re
import matplotlib.pyplot as plt

current_file_path = Path(__file__)
source_directory_path = current_file_path.parent
logging_directory_path = Path(source_directory_path, "logging")
log_file_path = str(Path(logging_directory_path, "ab_for_paper.txt"))

with open(log_file_path) as log:
    logs = log.read().split("-------------------------------------------------------------------------------------------------------------------------")

res_dict = {
    "simulated_annealing": {
        "step": [0],
        "time": [0],
        "energy": [206318]
    },
    "genetic_algorithm": {
        "step": [0],
        "time": [0],
        "energy": [206318]
    }
}


for log in logs[1:]:
    match_1 = re.search("INFO (\w+_\w+) (Generation|Step) ([\d,]+) of [\d,]", log)
    match_2 = re.search("Time from simulation start: ((\d+) hours,+ +)*((\d+) minutes,+ +)*((\d+) seconds)*", log)
    match_3 = re.search("Energy: (\d+,*\d+) bits", log)
    energy = int(match_3.group(1).replace(",", ""))
    time_in_secs = int(match_2.group(2) or 0)*60 + int(match_2.group(4) or 0) + int(match_2.group(6))/60
    res_dict[match_1.group(1)]["step"].append(int(match_1.group(3).replace(",", "")))
    res_dict[match_1.group(1)]["time"].append(time_in_secs)
    res_dict[match_1.group(1)]["energy"].append(energy)


ga_time = res_dict["genetic_algorithm"]["time"]
ga_steps = res_dict["genetic_algorithm"]["step"]
ga_energy = res_dict["genetic_algorithm"]["energy"]


plt.plot(ga_time, ga_energy, label="Genetic Algorithm")


sa_time = res_dict["simulated_annealing"]["time"]
sa_steps = res_dict["simulated_annealing"]["step"]
sa_energy = res_dict["simulated_annealing"]["energy"]


plt.plot(sa_time, sa_energy, label="Simulated Annealing")

plt.xlabel('Time (minutes)')
plt.ylabel('DL')
plt.title('Description Length over Time')
plt.legend()
plt.show()