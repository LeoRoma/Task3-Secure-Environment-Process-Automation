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
    duplicate_donors = donors[
        donors.duplicated(subset=["donor_id"], keep=False)
    ]
    return duplicate_donors

def check_invalid_dates(donors):
    """
    Identify invalid dates in date_of_birth and last_contact.
    """
    invalid_dob = pd.to_datetime(
        donors["date_of_birth"], errors="coerce"
    ).isnull()

    invalid_contact = pd.to_datetime(
        donors["last_contact"], errors="coerce"
    ).isnull()

    return invalid_dob, invalid_contact

def check_invalid_engagement(donors):
    """
    Identify unexpected email engagement values.
    """
    valid_values = ["High", "Medium", "Low"]

    invalid_engagement = donors[
        ~donors["email_engagement"].isin(valid_values)
    ]

    return invalid_engagement

def check_future_contacts(donors):
    """
    Identify donor records with future contact dates.
    """
    contact_dates = pd.to_datetime(
        donors["last_contact"], errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    future_contacts = donors[
        contact_dates.notnull() & (contact_dates > today)
    ]

    return future_contacts