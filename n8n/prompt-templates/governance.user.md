Please analyze the attached document(s) (Annual Report and/or Remuneration Report) and extract the governance data into the requested JSON format.

**Extraction Logic:**

**1. From the Annual Report:**
   * **Structure:** Count the total number of directors/board members. List the top 5 key office-holders (Chairperson, Vice-Chair, Treasurer, Secretary).
   * **Committees:** Look for mentions of sub-committees like "Audit", "Finance", "HR", or "Nomination".
   * **Leadership:** Identify the highest-ranking *paid* staff member (often "CEO", "Director General", or "Chief Executive").
   * **Policies:** Scan for keywords to confirm if these specific policies exist:
       * "Conflict of Interest" (or "Declaration of Interest")
       * "Whistleblowing"
       * "Investment" (or "Reserves Policy")
       * "Procurement" (or "Tender")

**2. From the "Review Report on Remuneration Packages" (if provided):**
   * **Remuneration:** Extract the total annual remuneration for the Top Tier (Tier 1), Second Tier (Tier 2), and Third Tier (Tier 3) staff.
   * *Note:* If the report provides a range, extract the *maximum* value of that range. If exact figures are provided, use those.
   * **Date:** Extract the "Review Date" or the fiscal year end date from the report.

**JSON Schema:**

{{STRINGIFIED_JSON_SCHEMA}}

Output only the JSON object. 