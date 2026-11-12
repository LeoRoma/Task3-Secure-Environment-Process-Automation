
import pandas as pd
from datetime import timedelta

from src.data_quality import (
    check_missing_values, 
    check_duplicate_donors, 
    check_invalid_dates, 
    check_invalid_engagement,
    check_future_contacts,
    build_quality_report,
)


def test_check_missing_values():
    # Arrange: create a small test dataset
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002"],
        "date_of_birth": ["1985-04-12", None],
        "last_contact": ["2026-08-10", "2026-08-11"],
        "email_engagement": ["High", "Low"]
    })

    # Act: run the data quality check
    result = check_missing_values(donors)

    # Assert: verify the expected results
    assert result["date_of_birth"] == 1
    assert result["last_contact"] == 0

def test_check_duplicate_donors():
    # Arrange: create a dataset containing a duplicate donor ID
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002", "D001"],
        "date_of_birth": ["1985-04-12", "1990-11-23", "1985-04-12"],
        "last_contact": ["2026-08-10", "2026-08-11", "2026-08-10"],
        "email_engagement": ["High", "Low", "High"]
    })

    # Act: identify duplicate donor records
    result = check_duplicate_donors(donors)

    # Assert: verify that both records with D001 are identified
    assert len(result) == 2
    assert result["donor_id"].tolist() == ["D001", "D001"]

def test_check_invalid_dates():
    # Arrange: create a dataset containing invalid dates
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002", "D003"],
        "date_of_birth": ["1985-04-12", "1988-15-40", None],
        "last_contact": ["2026-08-10", "invalid-date", "2026-08-11"],
        "email_engagement": ["High", "Low", "Medium"]
    })

    # Act: check date validity
    invalid_dob, invalid_contact = check_invalid_dates(donors)

    # Assert: verify invalid and missing dates are identified
    assert invalid_dob.tolist() == [False, True, True]
    assert invalid_contact.tolist() == [False, True, False]

def test_check_invalid_engagement():
    # Arrange: create a dataset with valid and unexpected engagement values
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002", "D003", "D004"],
        "date_of_birth": [
            "1985-04-12",
            "1990-11-23",
            "1978-06-05",
            "1988-03-15"
        ],
        "last_contact": [
            "2026-08-10",
            "2026-08-11",
            "2026-08-12",
            "2026-08-13"
        ],
        "email_engagement": ["High", "Low", "Medium", "Unknown"]
    })

    # Act: identify unexpected engagement values
    result = check_invalid_engagement(donors)

    # Assert: only the record with Unknown engagement is identified
    assert len(result) == 1
    assert result["donor_id"].tolist() == ["D004"]

def test_check_future_contacts():
    # Arrange: create a dataset with a past and a future contact date
    today = pd.Timestamp.today().normalize()

    donors = pd.DataFrame({
        "donor_id": ["D001", "D002"],
        "date_of_birth": ["1985-04-12", "1990-11-23"],
        "last_contact": [
            (today - timedelta(days=10)).strftime("%Y-%m-%d"),
            (today + timedelta(days=10)).strftime("%Y-%m-%d")
        ],
        "email_engagement": ["High", "Low"]
    })

    # Act: identify future contact dates
    result = check_future_contacts(donors)

    # Assert: only the record with a future date is identified
    assert len(result) == 1
    assert result["donor_id"].tolist() == ["D002"]

def test_build_quality_report():
    # Arrange: create a dataset containing different quality issues
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002", "D001"],
        "date_of_birth": ["1985-04-12", "invalid-date", "1985-04-12"],
        "last_contact": ["2026-08-10", None, "2026-08-10"],
        "email_engagement": ["High", "Unknown", "High"]
    })

    original_dob = donors["date_of_birth"].copy()
    original_contact = donors["last_contact"].copy()

    invalid_dob, invalid_contact = check_invalid_dates(donors)
    duplicate_donors = check_duplicate_donors(donors)
    invalid_engagement = check_invalid_engagement(donors)
    future_contacts = check_future_contacts(donors)

    # Act: build the quality report
    report = build_quality_report(
        donors,
        original_dob,
        original_contact,
        invalid_dob,
        invalid_contact,
        duplicate_donors,
        invalid_engagement,
        future_contacts
    )

    # Assert: verify that all expected issues are included
    assert len(report) == 5
    assert "Invalid date: date_of_birth" in report["issue"].values
    assert "Missing value: last_contact" in report["issue"].values
    assert "Duplicate donor ID" in report["issue"].values
    assert "Unexpected email engagement value" in report["issue"].values