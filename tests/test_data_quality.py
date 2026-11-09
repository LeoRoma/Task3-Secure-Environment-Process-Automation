
import pandas as pd

from src.data_quality import check_missing_values


def test_check_missing_values():
    # Arrange
    donors = pd.DataFrame({
        "donor_id": ["D001", "D002"],
        "date_of_birth": ["1985-04-12", None],
        "last_contact": ["2026-08-10", "2026-08-11"],
        "email_engagement": ["High", "Low"]
    })

    # Act
    result = check_missing_values(donors)

    # Assert
    assert result["date_of_birth"] == 1
    assert result["last_contact"] == 0
