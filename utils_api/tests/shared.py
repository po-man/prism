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
        "sources": [
            {
                "source_type": "financial_report",
                "page_number": 5,
                "search_result_index": None,
                "quote": "Statement of Financial Activities for the year ended 31 March 2024.",
                "resolved_url": None
            }
        ]
    },
    "impact": {
        "beneficiaries": [{
            "location": "Hong Kong",
            "population": 500,
            "beneficiary_type": "companion_animals",
            "source": {
                "source_type": "annual_report",
                "page_number": 15,
                "search_result_index": None,
                "quote": "We provided services to 500 companion animals in the Hong Kong area.",
                "resolved_url": None
            }
        }],
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
                "timeframe": "annual",
                "source": {
                    "source_type": "annual_report",
                    "page_number": 12,
                    "search_result_index": None,
                    "quote": "The study showed a significant increase in animal welfare, with 1,000 animals rescued.",
                    "resolved_url": None
                }
            }
        ],
        "significant_events": [
            {
                "event_name": "Project Shelter",
                "summary": "Built a new shelter facility.",
                "intervention_type": ["individual_rescue_and_sanctuary"],
                "intervention_type_other_description": None,
                "timeframe": "annual",
                "source": {
                    "source_type": "web_search",
                    "page_number": None,
                    "search_result_index": 0,
                    "quote": "Our new shelter facility, 'Project Shelter', opened this year.",
                    "resolved_url": None
                }
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