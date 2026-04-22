## 1. Prompt Engineering (`n8n/prompt-templates`)
- [x] 1.1 Open `n8n/prompt-templates/impact.system.md`.
- [x] 1.2 Locate Principle 1 (Context Hierarchy and Provenance).
- [x] 1.3 Modify the instruction for `explicit_unit_costs` to remove the phrase "or deliver an intervention". It should read: "If the charity explicitly states the exact cost to help *one individual animal* (e.g., 'It costs $25 to spay a dog', 'Sponsor a farm rescue for £50'), you must capture each statement as an entry in the `explicit_unit_costs` array."
- [x] 1.4 Append a strict negative constraint immediately after: "Do NOT extract aggregate budgets, total grant awards, monthly team costs, or overall fundraising campaign targets. It MUST be a discrete unit cost per individual animal."