Please analyze the attached annual report for impact metrics and respond in the requested JSON format.

### Field Mapping Guidance:

- **`beneficiaries_demographic`**: Be specific. Extract concrete locations, age ranges, and populations. Avoid vague terms like 'the community' or 'disadvantaged groups' unless no other detail is provided.
- **`evidence_quality`**: This field must be one of the following exact values: `["RCT/Meta-Analysis", "Quasi-Experimental", "Pre-Post", "Anecdotal", "None"]`. Map the report's claims to the *highest appropriate* level of evidence.

{{STRINGIFIED_JSON_SCHEMA}}

Please output the result as a single JSON object.