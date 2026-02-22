"""
Shared data for tests.
"""

# A sample record with all the necessary nested structures.
# This can be used as a base for tests that require a valid OrganisationRecord.
VALID_BASE_RECORD = {
    "financials": {
        "financial_year": "2023-24",
        "income": {"donations": 500000, "government_grants": 250000, "total": 750000},
        "expenditure": {"administration": 100000, "fundraising": 50000, "program_services": 400000, "total": 550000},
        "lsg_specifics": {"lsg_reserve_amount": 50000, "provident_fund_reserve": 10000},
        "ratio_inputs": {
            "monthly_operating_expenses": 20000,
            "net_current_assets": 60000,
            "current_assets": 80000,
            "current_liabilities": 20000
        },
    },
    "governance": {
        "structure": {
            "board_size": 10,
            "board_members": [{"name": "John Doe", "title": "Chairman", "is_executive": False}],
            "committees": ["Audit", "Remuneration"]
        },
        "leadership": {"ceo_name": "Jane Doe", "ceo_title": "CEO"},
        "remuneration_disclosure": {
            "source_document_present": True,
            "top_tier_total_salary": 120000,
            "second_tier_total_salary": 90000,
            "third_tier_total_salary": 70000,
            "review_date": "2023-06-15"
        },
        "policies": {
            "has_conflict_of_interest": True,
            "has_whistleblowing": True,
            "has_investment_policy": True,
            "has_procurement_policy": True
        }
    },
    "impact": {
        "importance_factors": {
            "beneficiaries_demographic": [{"location": "HK", "gender": "female", "age_range": "20-30", "population": 500, "beneficiary_type": "human"}],
            "problem_profile": {
                "problem_name": "Problem X", "target_population": "Group Y",
                "severity_dimensions": [{
                    "dimension": "Health", "metric_name": "QALY", "quantitative_data": {"value": 1000, "unit": "years"},
                    "context_qualifier": "context", "counterfactual_baseline": {"description": "baseline", "value": 1},
                    "evidence_quality": "RCT/Meta-Analysis", "source_citation": "Source Z"
                }]
            }
        },
        "tractability_factors": {"significant_events": [{"event_name": "E1", "summary": "S1"}], "evaluation_systems": "System A"},
        "neglectedness_factors": {"funding_sources": ["Gov"], "funding_landscape": "Crowded"}
    }
}