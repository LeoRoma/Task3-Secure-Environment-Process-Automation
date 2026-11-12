
import pandas as pd

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
