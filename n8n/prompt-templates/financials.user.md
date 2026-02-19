Please analyze the attached audited financial report for the most recent financial year and extract the data into the requested JSON format.

### Field Mapping Guidance:
- **`net_current_assets`**: Look for "Net Current Assets" or "Net Working Capital" on the Balance Sheet.
- **`current_assets`**: If "Net Current Assets" is not available, find the total "Current Assets".
- **`current_liabilities`**: If "Net Current Assets" is not available, find the total "Current Liabilities".
- **`monthly_operating_expenses`**: Find "Total Operating Expenditure" for the year and divide by 12. If not available, use "Total Expenditure".
- **`lsg_reserve_amount`**: Look for "Lump Sum Grant Reserve" or "LSG Reserve" in the notes to the financial statements.

{{STRINGIFIED_JSON_SCHEMA}}

Please output the result as a single JSON object.