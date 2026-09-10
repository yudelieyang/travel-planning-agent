from enum import StrEnum


class BudgetScope(StrEnum):
    TOTAL_TRIP = "TOTAL_TRIP"
    PER_PERSON = "PER_PERSON"
    UNKNOWN = "UNKNOWN"
