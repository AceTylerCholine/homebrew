import pandas as pd

filename = "TaVNS_DATA_RAW_2023-07-12_1630"

if filename[-4:] != '.csv':
    filename = filename + '.csv'

columns = ['record_id', 'redcap_event_name', 'demo_1', 'demo_3', 'demo_4', 'demo_5___2', 'demo_5___3', 'demo_5___5', 'demo_5___6', 'demo_7', 'demo_19', 'demo_21', 'demo_22', 'demo_27', 'demo_28']

# Load the data into a DataFrame
df = pd.read_csv(filename, usecols=columns)

# Remove Pilot, PreScreen, and Missing data
df = df[~df['record_id'].str.contains('_Pilot')]
df = df.dropna()

# Remove participant ids
df = df.drop(columns=['record_id'])

# Rename columns/measures to more accurate names
df = df.rename(columns={'demo_1': 'Gender', 'demo_3': 'Age', 'demo_4': 'Ethnicity', 'demo_5___2': 'Asian', 'demo_5___3': 'Black', 'demo_5___5': 'White', 'demo_5___6': 'Other_Race', 'demo_7': 'American_Born', 'demo_19': 'Education', 'demo_21': 'Mother_education', 'demo_22': 'Employed', 'demo_27': 'Income', 'demo_28': 'Marital_Status'})

# Group the participants by arm
Active = df[df['redcap_event_name'] == 'session_1_arm_2']
Sham = df[df['redcap_event_name'] == 'session_1_arm_3']

# Create a list of demographic categories
categories = ['Gender', 'Ethnicity', 'Asian', 'Black', 'White', 'Other_Race', 'American_Born']

# Create a new DataFrame to store the demographic results
demographics = pd.DataFrame(columns=['Demographics', 'Active n', 'Active %', 'Sham n', 'Sham %', 'Total n', 'Total %'])

# Loop through each category and calculate the statistics
for category in categories:
    active_n = len(Active[Active[category] == 1.0])
    active_p = active_n / len(Active) * 100
    sham_n = len(Sham[Sham[category] == 1.0])
    sham_p = sham_n / len(Sham) * 100
    total_n = len(df[df[category] == 1.0])
    total_p = total_n / len(df) * 100

    # Create a new DataFrame for the category results
    category_df = pd.DataFrame({'Demographics': [category], 'Active n': [active_n], 'Active %': [active_p], 'Sham n': [sham_n], 'Sham %': [sham_p], 'Total n': [total_n], 'Total %': [total_p]})

    # Concatenate the category_df with the demographics DataFrame
    demographics = pd.concat([demographics, category_df], ignore_index=True)

# Handle the Employment category separately
employment_labels = {
    1.0: "Full Time",
    2.0: "Part Time"
}

unemployment_labels = {
    3.0: "Unemployed (Voluntarily)",
    4.0: "Unemployed (Involuntarily)"
}

for value, label in employment_labels.items():
    active_n = len(Active[(Active['Employed'] == value) & (Active['Employed'] != 0)])
    active_p = active_n / len(Active[Active['Employed'] != 0]) * 100
    sham_n = len(Sham[(Sham['Employed'] == value) & (Sham['Employed'] != 0)])
    sham_p = sham_n / len(Sham[Sham['Employed'] != 0]) * 100
    total_n = len(df[(df['Employed'] == value) & (df['Employed'] != 0)])
    total_p = total_n / len(df[df['Employed'] != 0]) * 100

    # Create a new DataFrame for the Employment subcategory results
    employment_df = pd.DataFrame({'Demographics': [f'Employed ({label})'], 'Active n': [active_n], 'Active %': [active_p], 'Sham n': [sham_n], 'Sham %': [sham_p], 'Total n': [total_n], 'Total %': [total_p]})

    # Concatenate the employment_df with the demographics DataFrame
    demographics = pd.concat([demographics, employment_df], ignore_index=True)

for value, label in unemployment_labels.items():
    active_n = len(Active[(Active['Employed'] == value) & (Active['Employed'] != 0)])
    active_p = active_n / len(Active[Active['Employed'] != 0]) * 100
    sham_n = len(Sham[(Sham['Employed'] == value) & (Sham['Employed'] != 0)])
    sham_p = sham_n / len(Sham[Sham['Employed'] != 0]) * 100
    total_n = len(df[(df['Employed'] == value) & (df['Employed'] != 0)])
    total_p = total_n / len(df[df['Employed'] != 0]) * 100

    # Create a new DataFrame for the Unemployment subcategory results
    unemployment_df = pd.DataFrame({'Demographics': [f'Employment ({label})'], 'Active n': [active_n], 'Active %': [active_p], 'Sham n': [sham_n], 'Sham %': [sham_p], 'Total n': [total_n], 'Total %': [total_p]})

    # Concatenate the unemployment_df with the demographics DataFrame
    demographics = pd.concat([demographics, unemployment_df], ignore_index=True)

# Handle the Income category separately
income_labels = {
    1.0: "< $20,000/yr",
    2.0: "< $20,000/yr",
    3.0: "$20,000-$39,999/yr",
    4.0: "$20,000-$39,999/yr",
    5.0: "$40,000-$59,999/yr",
    6.0: "$40,000-$59,999/yr",
    7.0: "> $60,000/yr"
}

income_data = {'Demographics': [], 'Active n': [], 'Active %': [], 'Sham n': [], 'Sham %': [], 'Total n': [], 'Total %': []}

for value, label in income_labels.items():
    active_n = len(Active[(Active['Income'] == value) & (Active['Income'] != 0)])
    sham_n = len(Sham[(Sham['Income'] == value) & (Sham['Income'] != 0)])
    total_n = len(df[(df['Income'] == value) & (df['Income'] != 0)])

    if label not in income_data['Demographics']:
        income_data['Demographics'].append(label)
        income_data['Active n'].append(active_n)
        income_data['Sham n'].append(sham_n)
        income_data['Total n'].append(total_n)
    else:
        index = income_data['Demographics'].index(label)
        income_data['Active n'][index] += active_n
        income_data['Sham n'][index] += sham_n
        income_data['Total n'][index] += total_n

total_active_n = sum(income_data['Active n'])
total_sham_n = sum(income_data['Sham n'])
total_total_n = sum(income_data['Total n'])

income_data['Active %'] = [(n / total_active_n * 100) for n in income_data['Active n']]
income_data['Sham %'] = [(n / total_sham_n * 100) for n in income_data['Sham n']]
income_data['Total %'] = [(n / total_total_n * 100) for n in income_data['Total n']]

# Create a DataFrame for the combined Income category results
income_df = pd.DataFrame(income_data)

# Concatenate the income_df with the demographics DataFrame
demographics = pd.concat([demographics, income_df], ignore_index=True)

# Save the demographic results to a new CSV file
demographics.to_csv('demographics_summary.csv', index=False)