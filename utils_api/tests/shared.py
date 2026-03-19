"""
Shared data for tests.
"""

FINANCIAL_FIGURE_SOURCE_TEMPLATE = {
    "source_type": "attached_report",
    "source_index": 0,
    "page_number": 5,
    "search_result_index": None,
    "quote": "Statement of Financial Activities for the year ended 31 March 2024.",
    "resolved_url": None,
}

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
        "income": {
            "donations": {"value": 500000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "government_grants": {"value": 250000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "total": {"value": 750000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
        },
        "expenditure": {
            "administration": {"value": 100000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "fundraising": {"value": 50000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "program_services": {"value": 400000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "total": {"value": 550000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
        },
        "reserves": {"total_reserves": {"value": 75000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE}},
        "lsg_specifics": {
            "lsg_reserve_amount": {"value": 50000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "provident_fund_reserve": {"value": 10000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
        },
        "ratio_inputs": {
            "monthly_operating_expenses": {"value": 20000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "net_current_assets": {"value": 60000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "current_assets": {"value": 80000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
            "current_liabilities": {"value": 20000, "source": FINANCIAL_FIGURE_SOURCE_TEMPLATE},
        },
    },
    "impact": {
        "beneficiaries": [{
            "location": "Hong Kong",
            "population": 500,
            "beneficiary_type": "companion_animals",
            "source": {
                "source_type": "attached_report",
                "source_index": 0,
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
                    "source_type": "attached_report",
                    "source_index": 0,
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
                    "source_index": None,
                    "page_number": None,
                    "search_result_index": 0,
                    "quote": "Our new shelter facility, 'Project Shelter', opened this year.",
                    "resolved_url": None
                }
            }
        ],
        "context": {
            "operating_scope": {
                "value": "pure_animal_advocacy",
                "source": {
                    "source_type": "web_search",
                    "source_index": None,
                    "page_number": None,
                    "search_result_index": 0,
                    "quote": "We are an organisation dedicated to animal advocacy.",
                    "resolved_url": None
                }
            },
            "explicit_unit_costs": [
                {
                    "intervention_type": "high_volume_spay_neuter",
                    "amount": 25,
                    "currency": "HKD",
                    "description": "Cost to spay one dog.",
                    "source": {
                        "source_type": "attached_report",
                        "source_index": 0,
                        "page_number": 18,
                        "search_result_index": None,
                        "quote": "It costs just $25 to spay one dog.",
                        "resolved_url": None
                    }
                }
            ]
        },
        "transparency_indicators": {
            "unintended_consequences_reported": {
                "value": False
            },
            "euthanasia_statistics_reported": {
                "value": True,
                "source": {
                    "source_type": "attached_report",
                    "source_index": 0,
                    "page_number": 1,
                    "search_result_index": None,
                    "quote": "The euthanasia is 2%",
                    "resolved_url": None
                }
            }
        }
    },
}