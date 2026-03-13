# Amazon Reviews Data Analysis
### Group 19 ECE 143 Project

#### Objective: 
1) Question: What quantifiable metrics contribute to a helpful review?
2) Help buyers sift through reviews to be better informed
3) Question: For sellers, how can helpful reviews benefit the product?

## Dataset
Amazon review dataset collected by UCSD McAuley lab: ([Amazon review dataset](https://amazon-reviews-2023.github.io/))

This dataset contains reviews grouped into many item categories (appliances, automotive, toys and games, baby products, etc.). The dataset spans from May. 1996 - Sep.2023, and contains information such as rating, helpful votes, review message, verified purchase tag, and product metadata (overall rating, number of ratings, price, etc.)


## 📁 To Run ```final_notebook.ipynb```:

1) Clone this branch of the repo

2) Add two folders named ```meta_categories``` and ```review_categories``` with the respective ```.jsonl``` files following the directory structure below:

```text
G:\AmazonReviewsDataAnalysis/           # coded in as {BASE_PATH}
├── csv/                                # Processed datasets for plotting
│   └── helpfulness_summary.csv
│
├── meta_categories/                    # Product metadata (Git-ignored)
│   └── meta_[Category].jsonl
│
├── plots/                              # Exported visualizations & figures
│   └── *.png
│
├── review_categories/                  # Raw review datasets (Git-ignored)
│   └── [Category].jsonl
│
├── scripts/                            # Modular Python logic
│   ├── dataset_filter.py               # Data cleaning & preprocessing
│   ├── reviews_over_time.py            # Temporal trend analysis
│   └── stats_tests.py                  # Statistical testing (Granger, etc.)
│
└── final_notebook.ipynb                # Main consolidated project .ipynb
```

3) Run final_notebook.ipynb after connecting to a runtime. This file will have the necessary functions to run the filtering and statsitical testing used to generate all figures for this project.

## Libraries Used
1. Pandas
2. Numpy
3. Seaborn
4. Matplotlib
5. Statsmodels
6. json