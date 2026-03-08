"""
Shared data for tests.
"""

# A sample record with all the necessary nested structures.
# This can be used as a base for tests that require a valid OrganisationRecord.
VALID_BASE_RECORD = {
    "meta": {
        "chinese_name": "測試機構",
        "aliases": ["TEST"],
        "domains": ["example.org"],
        "registration_id": "91/12345"
    },
    "financials": {
        "financial_year": "2023-24",
        "currency": {
            "original_code": "HKD",
            "usd_exchange_rate": 0.128,
            "rate_date": "2023-12-31",
        },
        "income": {"donations": 500000, "government_grants": 250000, "total": 750000},
        "expenditure": {"administration": 100000, "fundraising": 50000, "program_services": 400000, "total": 550000},
        "reserves": {"total_reserves": 75000},
        "lsg_specifics": {"lsg_reserve_amount": 50000, "provident_fund_reserve": 10000},
        "ratio_inputs": {
            "monthly_operating_expenses": 20000,
            "net_current_assets": 60000,
            "current_assets": 80000,
            "current_liabilities": 20000,
        },
    },
    "impact": {
        "beneficiaries": [{"location": "Hong Kong", "population": 500, "beneficiary_type": "companion_animals"}],
        "metrics": [
            {
                "metric_name": "Animals Rescued",
                "quantitative_data": {"value": 1000, "unit": "animals"},
                "context_qualifier": "Rescued from unsafe conditions.",
                "counterfactual_baseline": {
                    "description": "Without intervention, these animals would have remained at risk.",
                    "value": 50,
                },
                "evidence_quality": "RCT/Meta-Analysis",
                "source_citation": "Annual Report 2023, p. 12",
                "source_url": None,
                "source_document": "pdf",
                "evidence_quote": "The study showed a significant increase in animal welfare.",
                "search_result_index": None,
                "timeframe": "annual",
            }
        ],
        "significant_events": [
            {
                "event_name": "Project Shelter",
                "summary": "Built a new shelter facility.",
                "intervention_type": ["individual_rescue_and_sanctuary"],
                "intervention_type_other_description": None,
                "source_url": None,
                "source_document": "pdf",
                "source_quote": None,
                "search_result_index": None,
                "timeframe": "annual"
            }
        ],
        "context": {
            "operating_scope": "pure_animal_advocacy",
            "explicit_unit_cost": {
                "amount": 25,
                "currency": "HKD",
                "description": "Cost to spay one dog."
            },
        }
    },
}