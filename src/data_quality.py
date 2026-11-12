import pandas as pd

VALID_ENGAGEMENT_VALUES = ["High", "Medium", "Low"]


def check_missing_values(donors):
    """
    Identify missing values in the donor dataset.
    """
    missing_values = donors.isnull().sum()
    return missing_values


def check_duplicate_donors(donors):
    """
    Identify donor records with duplicate donor IDs.
    """
    duplicate_donors = donors[donors.duplicated(subset=["donor_id"], keep=False)]
    return duplicate_donors


def check_invalid_dates(donors):
    """
    Identify invalid dates in date_of_birth and last_contact.
    """
    invalid_dob = pd.to_datetime(donors["date_of_birth"], errors="coerce").isnull()

    invalid_contact = pd.to_datetime(donors["last_contact"], errors="coerce").isnull()

    return invalid_dob, invalid_contact


def check_invalid_engagement(donors):
    """
    Identify unexpected email engagement values.
    """
    valid_values = VALID_ENGAGEMENT_VALUES

    invalid_engagement = donors[~donors["email_engagement"].isin(valid_values)]

    return invalid_engagement


def check_future_contacts(donors):
    """
    Identify donor records with future contact dates.
    """
    contact_dates = pd.to_datetime(donors["last_contact"], errors="coerce")

    today = pd.Timestamp.today().normalize()

    future_contacts = donors[contact_dates.notnull() & (contact_dates > today)]

    return future_contacts


def build_quality_report(
    donors,
    original_dob,
    original_contact,
    invalid_dob,
    invalid_contact,
    duplicate_donors,
    invalid_engagement,
    future_contacts,
):
    """
    Build a report containing all identified data quality issues.
    """

    issues = []

    # Record missing values
    for column, original_values in [
        ("date_of_birth", original_dob),
        ("last_contact", original_contact),
    ]:
        for index in original_values[original_values.isnull()].index:
            issues.append(
                {
                    "donor_id": donors.loc[index, "donor_id"],
                    "issue": f"Missing value: {column}",
                    "original_value": None,
                }
            )

    # Record invalid dates
    for index in donors.index:
        if (
            invalid_dob.loc[index]
            and original_dob.loc[index] is not None
            and pd.notna(original_dob.loc[index])
        ):
            issues.append(
                {
                    "donor_id": donors.loc[index, "donor_id"],
                    "issue": "Invalid date: date_of_birth",
                    "original_value": original_dob.loc[index],
                }
            )

        if (
            invalid_contact.loc[index]
            and original_contact.loc[index] is not None
            and pd.notna(original_contact.loc[index])
        ):
            issues.append(
                {
                    "donor_id": donors.loc[index, "donor_id"],
                    "issue": "Invalid date: last_contact",
                    "original_value": original_contact.loc[index],
                }
            )

    # Record duplicate donor IDs
    for index in duplicate_donors.index:
        issues.append(
            {
                "donor_id": donors.loc[index, "donor_id"],
                "issue": "Duplicate donor ID",
                "original_value": None,
            }
        )

    # Record unexpected engagement values
    for index in invalid_engagement.index:
        issues.append(
            {
                "donor_id": donors.loc[index, "donor_id"],
                "issue": "Unexpected email engagement value",
                "original_value": donors.loc[index, "email_engagement"],
            }
        )

    # Record future contact dates
    for index in future_contacts.index:
        issues.append(
            {
                "donor_id": donors.loc[index, "donor_id"],
                "issue": "Future contact date",
                "original_value": original_contact.loc[index],
            }
        )

    return pd.DataFrame(issues, columns=["donor_id", "issue", "original_value"])
