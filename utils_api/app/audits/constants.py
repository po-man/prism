"""
This module contains constant definitions for the audit engine, serving as a
centralized, version-controlled source of truth for evaluation criteria.
"""

# The order of this list defines the hierarchy for evidence quality.
EVIDENCE_HIERARCHY = ["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]

INTERVENTION_LEVERAGE_MAP = {
    # Tier 1: Systemic Change - Interventions that create large-scale, lasting change.
    "corporate_welfare_campaigns": {
        "tier": 1, "tier_name": "Tier 1: Systemic Change",
        "note": "Corporate campaigns achieve large-scale, measurable welfare improvements by changing industry standards."
    },
    "policy_and_legal_advocacy": {
        "tier": 1, "tier_name": "Tier 1: Systemic Change",
        "note": "Policy and legal advocacy create systemic, legally-binding protections for animals."
    },
    "alternative_protein_and_food_tech": {
        "tier": 1, "tier_name": "Tier 1: Systemic Change",
        "note": "Developing and promoting alternatives to animal products addresses the root cause of industrial animal agriculture."
    },
    "undercover_investigations_and_exposes": {
        "tier": 1, "tier_name": "Tier 1: Systemic Change",
        "note": "Investigations are a key driver for corporate and legislative change, creating widespread public awareness."
    },
    "wildlife_conservation_and_habitat_protection": {
        "tier": 1, "tier_name": "Tier 1: Systemic Change",
        "note": "Protecting entire ecosystems and populations of wild animals offers broad, systemic benefits."
    },
    # Tier 2: Preventative Scale - Interventions that prevent suffering at a large scale.
    "high_volume_spay_neuter": {
        "tier": 2, "tier_name": "Tier 2: Preventative Scale",
        "note": "Mass spay/neuter is a proven method for population control, preventing future suffering at scale."
    },
    "scientific_and_welfare_research": {
        "tier": 2, "tier_name": "Tier 2: Preventative Scale",
        "note": "Research informs and improves the effectiveness of other interventions and welfare standards."
    },
    "vegan_outreach_and_dietary_change": {
        "tier": 2, "tier_name": "Tier 2: Preventative Scale",
        "note": "Promoting dietary change can reduce demand for animal products, preventing animal suffering."
    },
    "humane_education_and_community_support": {
        "tier": 2, "tier_name": "Tier 2: Preventative Scale",
        "note": "Education fosters long-term compassionate attitudes, preventing future cruelty and neglect."
    },
    # Tier 3: Direct Care & Indirect Action - Interventions focused on individual animals or enabling other groups.
    "individual_rescue_and_sanctuary": {
        "tier": 3, "tier_name": "Tier 3: Direct Care & Indirect Action",
        "note": "Direct rescue provides high value to individual animals but is less scalable for large-scale change."
    },
    "veterinary_care_and_treatment": {
        "tier": 3, "tier_name": "Tier 3: Direct Care & Indirect Action",
        "note": "Veterinary care is crucial for individual animal welfare but is a direct service with limited systemic impact."
    },
    "disaster_response_and_emergency_relief": {
        "tier": 3, "tier_name": "Tier 3: Direct Care & Indirect Action",
        "note": "Emergency relief is vital for saving lives during crises but is reactive and focused on immediate care."
    },
    "capacity_building_and_movement_growth": {
        "tier": 3, "tier_name": "Tier 3: Direct Care & Indirect Action",
        "note": "Funding and training other groups is a meta-level intervention whose tractability is dependent on its grantees."
    }
}