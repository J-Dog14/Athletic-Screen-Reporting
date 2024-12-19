import pandas as pd

# Define the path to the CSV file
input_file_path = r"H:\Pitching\WF Data_Final.csv"
output_file_path = r"H:\Pitching\WF Data_Cleaned.csv"

# Read the CSV file, skipping the first row
df = pd.read_csv(input_file_path, skiprows=1)

# Verify the column name for the filenames
file_column = 'Filename'  # Update if the actual column name differs

# Extract the unique file path portion (excluding 'Report' or 'Report_exp' distinction)
df['base_path'] = df[file_column].str.replace(r"\\Report.*?cmz", "", regex=True)

# Debugging Step: Inspect the extracted 'base_path'
print("Unique base paths (sample):")
print(df['base_path'].drop_duplicates().head(20))

# Add a column to indicate whether a file is '_exp'
df['is_exp'] = df[file_column].str.contains(r"_exp", na=False)

# Debugging Step: Count '_exp' and non-'_exp' files
print("\nCounts of '_exp' vs. non-'_exp':")
print(df['is_exp'].value_counts())

# Sort to prioritize non-'_exp', and remove duplicates based on 'base_path'
cleaned_df = (
    df.sort_values(by='is_exp')  # Non-'_exp' files come first
    .drop_duplicates(subset='base_path', keep='first')  # Drop duplicates based on 'base_path'
)

# Debugging Step: Verify rows being dropped
print("\nFiles being dropped due to duplicates:")
dropped_files = df[~df.index.isin(cleaned_df.index)]
print(dropped_files[[file_column, 'base_path']])

# Drop helper columns
cleaned_df = cleaned_df.drop(columns=['base_path', 'is_exp'])

# Save the cleaned DataFrame to a new CSV file
cleaned_df.to_csv(output_file_path, index=False)

print(f"\nCleaned data saved to {output_file_path}")
