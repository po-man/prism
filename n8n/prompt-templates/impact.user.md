Please analyze the attached annual report for impact metrics and respond in the requested JSON format.

### Field Mapping Guidance:

- **`beneficiaries_demographic`**: Be specific. Extract concrete locations, age ranges, and populations. Avoid vague terms like 'the community' or 'disadvantaged groups' unless no other detail is provided.
- **`evidence_quality`**: This field must be one of the following exact values: `["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]`. Map the report's claims to the *highest appropriate* level of evidence based strictly on the definitions in your system instructions. (Note: General surveys and feedback forms are "Anecdotal", not "Pre-Post" or "Quasi-Experimental").
- **`quantitative_data.value`**: This MUST be an absolute count of outputs/outcomes (e.g., number of unique people helped, number of counseling sessions delivered). **NEVER** put monetary values (e.g., HKD, USD) or percentages in this field. If the outcome is monetary or a percentage, leave the value as `null`.
- **`counterfactual_baseline.value`**: Only populate this if a specific numerical baseline is provided in the text. Otherwise, leave it as `null`.

{{STRINGIFIED_JSON_SCHEMA}}

Please output the result as a single JSON object.