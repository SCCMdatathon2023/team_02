import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Load your dataset (replace 'your_dataset.csv' with the actual file path)
data = pd.read_csv('/Users/fredrikwhaug/research/datathons/sccm2023/team_02/data/preprocessed.csv')

setting = "mortality_logreg"

# Select features and target variable
features = [
    'admission_age', 'sex_female', 'weight_admission', 'height_admission', 'BMI_admission',
    # Add more features from the list as needed
]

X = subset[conf]
Y = subset["mortality"]

n_rep = 20
odds_ratios = []

# Outer loop
for i in tqdm(range(n_rep)):
    # List to append inner ORs
    ORs = []

    # Normal k-fold cross validation
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=i)
    
    # Inner loop, in each fold
    for train_index, test_index in tqdm(kf.split(X, r)):
    X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    # Fit logistic regression model
    model = LogisticRegression(max_iter=10000)
    model.fit(X_test, y_test)

    idx = X_test.columns.get_loc(val)
    param = model.coef_[0][idx]
    OR_inner = np.exp(param)

    # Append OR to list
    ORs.append(OR_inner)

    print(f"OR: {OR_inner:.5f}")

    # Calculate odds ratio based on all 5 folds, append
    odds_ratios.append(np.mean(ORs))

# Calculate confidence intervals
CI_lower = np.percentile(odds_ratios, 2.5)
OR = np.percentile(odds_ratios, 50)
CI_upper = np.percentile(odds_ratios, 97.5)

print(f"OR (95% CI): {OR:.3f} ({CI_lower:.3f} - {CI_upper:.3f})")

# Append results to dataframe
results_df = pd.concat([results_df, pd.DataFrame({  "OR": [OR],
                                                    "2.5%": [CI_lower],
                                                    "97.5%": [CI_upper],
                                                    "N": [len(data[data[val]==1])]})], 
                                                    ignore_index=True)
# Save results 
results_df.to_csv(f"results/models/{setting}.csv", index=False)
