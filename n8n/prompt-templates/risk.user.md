Conduct a risk assessment for the charity "{{CHARITY_NAME}}" (Aliases: "{{CHARITY_NAME_ALIASES}}").

Perform a comprehensive search using the following specific search angles:
1. "{{CHARITY_NAME}} Scandal"
2. "{{CHARITY_NAME}} Salary/Compensation controversy"
3. "{{CHARITY_NAME}} Misuse/Abuse"
4. "{{CHARITY_NAME}} Audit Commission reports"
5. "{{CHARITY_NAME}} fraud mismanagement"

Based on the search results, generate a JSON object adhering to the schema provided below. 

If no negative news is found, explicitly state "None" in summaries and set flags to false. Do not hallucinate risks.

Required Output Schema:

{{STRINGIFIED_JSON_SCHEMA}}