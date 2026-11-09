
import pandas as pd

from data_quality import ( 
    check_missing_values, 
    check_duplicate_donors, 
    check_invalid_dates, 
    check_invalid_engagement,
    check_future_contacts,
    VALID_ENGAGEMENT_VALUES
)

# Define the input file
input_file = "data/sample_donors.csv"

# Read the donor data from the CSV file
donors = pd.read_csv(input_file)

# Keep the original date values before conversion
original_dob = donors["date_of_birth"].copy()
original_contact = donors["last_contact"].copy()

# Display the donor records
print("Donor records loaded successfully:")
print(donors)

# Display the total number of records
print(f"\nTotal donor records: {len(donors)}")

# Check for missing values in each column
missing_values = check_missing_values(donors)

# Display the missing values report
print("\nMissing values report:")
print(missing_values)

# Check for invalid dates
invalid_dob, invalid_contact = check_invalid_dates(donors)

# Convert dates for further processing
donors["date_of_birth"] = pd.to_datetime(
    donors["date_of_birth"], errors="coerce"
)

donors["last_contact"] = pd.to_datetime(
    donors["last_contact"], errors="coerce"
)

# Identify invalid dates
invalid_dates = donors[invalid_dob | invalid_contact]

print("\nInvalid or missing dates:")
print(invalid_dates[["donor_id", "date_of_birth", "last_contact"]])


# Check for duplicate donor IDs
duplicate_donors = check_duplicate_donors(donors)

print("\nDuplicate donor records:")
print(duplicate_donors)


# Check for unexpected email engagement values
valid_engagement_values = VALID_ENGAGEMENT_VALUES

invalid_engagement = check_invalid_engagement(donors)

print("\nUnexpected email engagement values:")
print(invalid_engagement[["donor_id", "email_engagement"]])

# Identify invalid dates that were not originally empty
invalid_dob = original_dob.notnull() & donors["date_of_birth"].isnull()
invalid_contact = original_contact.notnull() & donors["last_contact"].isnull()

# Check for future contact dates
today = pd.Timestamp.today().normalize()

future_contacts = check_future_contacts(donors)

print("\nFuture contact dates:")
print(future_contacts[["donor_id", "last_contact"]])


# Create a list to store all data quality issues
issues = []

# Record missing values from the original CSV
for column, original_values in [
    ("date_of_birth", original_dob),
    ("last_contact", original_contact)
]:
    for index in original_values[original_values.isnull()].index:
        issues.append({
            "donor_id": donors.loc[index, "donor_id"],
            "issue": f"Missing value: {column}"
        })

# Record invalid dates
for index in donors[invalid_dob | invalid_contact].index:
    issues.append({
        "donor_id": donors.loc[index, "donor_id"],
        "issue": "Invalid date"
    })

# Record duplicate donor IDs
for index in duplicate_donors.index:
    issues.append({
        "donor_id": donors.loc[index, "donor_id"],
        "issue": "Duplicate donor ID"
    })

# Record unexpected engagement values
for index in invalid_engagement.index:
    issues.append({
        "donor_id": donors.loc[index, "donor_id"],
        "issue": "Unexpected email engagement value"
    })

# Record future contact dates
for index in future_contacts.index:
    issues.append({
        "donor_id": donors.loc[index, "donor_id"],
        "issue": "Future contact date"
    })

# Convert the issues into a DataFrame
report = pd.DataFrame(issues)

# Save the report as a CSV file
output_file = "output/data_quality_report.csv"
report.to_csv(output_file, index=False)

print(f"\nData quality report saved successfully: {output_file}")
