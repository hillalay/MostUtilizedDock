# Most Utilized Dock — Algorithm Analysis Project

This project identifies the most utilized dock using a binary occupancy matrix and compares two methods:

1. Sequential Algorithm
2. Divide & Conquer Algorithm

## The workflow includes data preprocessing, occupancy matrix creation, algorithm comparison, visualizations, and timing experiments.

# Project Structure

MostUtilizedDock/
├── data/
│ ├── dock_events_raw_sample.csv
│ ├── dock_occupancy_matrix.csv
│ ├── dock_occupied_counts.csv
│ ├── raw_logs.csv
│ └── results.csv
│
├── figures/
│ ├── bar_totals.png
│ ├── heatmap.png
│ └── runtime_analysis.png
│
├── report/
│ └── .gitkeep
│
├── src/
│ ├── create_data.py
│ ├── divide_conquer.py
│ ├── run_experiment.py
│ ├── sequential.py
│ ├── setup_full_data.py
│ ├── test_sequential.py
│ └── visualize_results.py
│
└── README.md

---

# Problem Definition

We represent dock usage as a binary matrix:

                  U ∈ {0,1}^(R*T)

- R → number of docks (rows)
- T → time slots
- U[i, t] = 1 → dock i is occupied at time t

Goal:
Find the dock with the maximum number of 1s.
Ties → choose the smallest index.

---

# Role A — Data Preparation & Sequential Method

✔️ Data Preparation

Scripts:

- src/create_data.py
- src/setup_full_data.py

These scripts:

- Load raw logs (raw_logs.csv)
- Convert events into equal-length time slots (Δ = 10 minutes)
- Create occupancy matrix dock_occupancy_matrix.csv
- (Optional) Save per-dock totals → dock_occupied_counts.csv

✔️ Sequential Algorithm

File: 'src/sequential.py'

✔️ Algorithm:

- For each row (dock), count 1s
- Track maximum count
- Ties keep the smaller dock index
- Return (best_row, best_count)

✔️ Complexity:

- Time: Θ(RT)
- Space: O(1)

Run manually:
'python src/sequential.py'

# Role B — Divide & Conquer Method

File: 'src/divide_conquer.py'

✔️ Method Summary

1. Split matrix columns into left/right halves
2. Recursively compute row sums
3. Combine by adding row-sum vectors
4. Run recursive argmax
5. Tie → smaller index

✔️ Complexity

- Work: Θ(RT)
- Span: Θ(log T) (parallelizable)
- Space: O(log T) recursion depth

### Run manually:

'python src/divide_conquer.py'

# Timing Experiments

File: src/run_experiment.py

This script:

- Loads dock_occupancy_matrix.csv
- Verifies Sequential == D&C output
- Runs both algorithms many times
- Produces:
  data/results.csv
  figures/runtime_analysis.png

Run:

python src/run_experiment.py

# Figures & Visualizations

File: src/visualize_results.py

Generates:

| Figure             | File                           |
| ------------------ | ------------------------------ |
| Heatmap of U       | `figures/heatmap.png`          |
| Totals per dock    | `figures/bar_totals.png`       |
| Runtime comparison | `figures/runtime_analysis.png` |

Run:
python src/visualize_results.py

# Testing

File: src/test_sequential.py

Run:

python src/test_sequential.py

# Covers:

- basic correctness
- ties
- zeros
- simple matrices

---

# Expected Outputs

After running all scripts, you should have:

data/dock_occupancy_matrix.csv
data/results.csv
figures/heatmap.png
figures/bar_totals.png
figures/runtime_analysis.png

Console output example:

Sequential: best_row = 3, best_count = 142
Divide&Conquer: best_row = 3, best_count = 142
OK: Both methods match.

---

📝 Reproducibility Checklist

- Occupancy matrix generated
- Sequential & D&C return same results
- Figures saved (heatmap, bar_totals, runtime_analysis)
- Timing results saved to data/results.csv
- Test script passes
- Report PDF added under /report

---

# Authors (Roles)

# Role A:

Data preparation, Sequential algorithm, Visualizations

# Role B:

## Divide & Conquer method, Performance experiments, Complexity analysis

📜 License
This project is developed as part of Algorithm and Analysis coursework (HW2).
