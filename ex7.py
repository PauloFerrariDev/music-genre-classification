import pandas as pd
import tsfel

# Retrieves a pre-defined feature configuration file to extract all available features
cfg = tsfel.get_features_by_domain()
columnName = 'DateTime'

# Read the CSV file and parse the timestamp column
df = pd.read_csv('veiculos-cruzamentos.csv', parse_dates=[columnName])

# Extract the groups based on year and month without adding new columns
groups = df.groupby([df[columnName].dt.year, df[columnName].dt.month])

df_features = pd.DataFrame()

# Save each group to a separate CSV file
for (year, month), group in groups:
    for i in range(1, 5):
        col_list = group[group.columns[i]].values.tolist()
        features = tsfel.time_series_features_extractor(cfg, col_list)
        features.insert(0,'date',f'{year}_{month}',True)
        features.insert(0,'class',group.columns[i],True)
        df_features = pd.concat([df_features, features], ignore_index=True)
        print('features=',features)

print('df_features=',df_features)
df_features.to_csv('features-veiculos-cruzamentos.csv', index=False)

