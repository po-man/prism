## 1. Audit Engine Logic Update (`utils_api`)
- [ ] 1.1 Open `utils_api/app/audits/impact.py` and locate the `calculate_ies` function.
- [ ] 1.2 Replace the current `species_key` search block (around Step 5) with an expanded text search:
    ```python
    # 5. Species Weight (W_species)
    species_key = None
    search_text = f"{metric.metric_name} {metric.quantitative_data.unit if metric.quantitative_data.unit else ''} {metric.context_qualifier or ''}".lower()
    if metric.source and metric.source.quote:
        search_text += f" {metric.source.quote.lower()}"
        
    for key in moral_weights:
        if key in search_text or key.rstrip('s') in search_text:
            species_key = key
            break
    ```
- [ ] 1.3 Implement the intermediate fuzzy-matching fallback immediately below:
    ```python
    if not species_key:
        matched_beneficiary = None
        if metric.source and metric.source.quote:
            for b in record.impact.beneficiaries.beneficiaries:
                if b.source and b.source.quote and _fuzzy_match(metric.source.quote, b.source.quote):
                    matched_beneficiary = b
                    break
                
        if matched_beneficiary:
            species_key = beneficiary_to_species_map.get(matched_beneficiary.beneficiary_type.value)
        else:
            species_key = beneficiary_to_species_map.get(dominant_beneficiary_type)
            
        if not species_key or species_key not in moral_weights:
            species_key = "generic_unspecified"
    ```
- [ ] 1.4 Update the `w_species` source explanation string to accurately reflect whether the fallback came from a matched beneficiary or the dominant organisation type.

## 2. Unit Testing
- [ ] 2.1 Open `utils_api/tests/test_audit_impact.py`.
- [ ] 2.2 In `test_calculate_ies_metric`, add a new mock metric and beneficiary to `record_data` representing a multi-domain overlap (e.g., metric unit is simply `"animals"`, but the quote matches a `farmed_animals` beneficiary).
- [ ] 2.3 Add assertions to verify that the `w_species` assigned to this new metric correctly maps to `generic_farmed` rather than falling back to the dominant `generic_companion`.