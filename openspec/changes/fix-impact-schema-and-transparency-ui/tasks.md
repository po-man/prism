## 1. Schema Updates (`schemas/v1/impact.schema.json`)
- [x] 1.1 Update `properties.context.properties.operating_scope` to include a `"source": { "$ref": "#/definitions/source" }` property.
- [x] 1.2 Update `properties.context.properties.explicit_unit_cost.properties.currency` description to: "The 3-letter ISO 4217 code of the currency (e.g., USD, HKD, INR)."
- [x] 1.3 Update the types within `explicit_unit_cost` (`amount`, `currency`, `description`) to allow nulls (e.g., `["number", "null"]`, `["string", "null"]`).
- [x] 1.4 Add a `"source": { "$ref": "#/definitions/source" }` property to the `explicit_unit_cost` object.

## 2. Prompt Injection Updates (`n8n/prompt-templates/impact.system.md`)
- [x] 2.1 Update rule #1 (Context Hierarchy and Provenance) to explicitly instruct the LLM: "If an explicit unit cost is not found, you MUST set the amount, currency, and description to `null`. Do not hallucinate `0`."
- [x] 2.2 Add instructions stating that both `operating_scope` and `explicit_unit_cost` now require strict provenance via the `source` object, including verbatim quotes.

## 3. Logic Layer Updates (`utils_api/app/audits/transparency.py`)
- [ ] 3.1 In `check_negative_impact_disclosure`, modify the `if disclosure:` block. Extract the quote using `record.impact.transparency_indicators.unintended_consequences_reported.source.quote` and assign it to `item.details.elaboration` using an f-string (e.g., `f"Quote: '{quote}'"`).
- [ ] 3.2 In `check_live_release_transparency`, modify the `if disclosure:` block to extract the `euthanasia_statistics_reported` quote and assign it to `item.details.elaboration`.
- [ ] 3.3 Ensure unit tests in `utils_api/tests/test_audit_transparency.py` are updated to assert the presence of the `elaboration` quotes when the status is `bonus`.