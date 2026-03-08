"""
This module contains constant definitions for the audit engine, serving as a
centralized, version-controlled source of truth for evaluation criteria.
"""

# The order of this list defines the hierarchy for evidence quality.
EVIDENCE_HIERARCHY = ["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]


INTERVENTION_TRACTABILITY_MAP = {
    "corporate_welfare_campaigns": {
        "level": "Quasi-Experimental",
        "note": "Corporate campaigns have a strong, documented history of achieving large-scale, measurable welfare improvements for farmed animals."
    },
    "policy_and_legal_advocacy": {
        "level": "Quasi-Experimental",
        "note": "Policy and legal advocacy can create systemic, legally-binding protections for animals, representing a highly tractable path to impact."
    },
    "high_volume_spay_neuter": {
        "level": "Pre-Post",
        "note": "Mass spay/neuter programmes are a well-established intervention with clear pre/post-intervention evidence for population control."
    },
    "vegan_outreach_and_education": {
        "level": "Anecdotal",
        "note": "While potentially high-impact, the long-term effectiveness of individual dietary change advocacy is difficult to measure and often relies on anecdotal or survey-based evidence."
    },
    "individual_rescue_and_sanctuary": {
        "level": "Anecdotal",
        "note": "Direct rescue provides high value to individual animals but is considered less tractable for large-scale change due to its high cost-per-animal and limited scope."
    },
    "veterinary_care_and_treatment": {
        "level": "Anecdotal",
        "note": "Providing veterinary care is crucial for animal welfare but is typically viewed as a direct service with anecdotal evidence of broader, systemic impact."
    },
    "capacity_building_and_grants": {
        "level": "Anecdotal",
        "note": "Funding and training other groups is a meta-level intervention whose tractability is dependent on the activities of its grantees and is not directly measurable."
    }
}