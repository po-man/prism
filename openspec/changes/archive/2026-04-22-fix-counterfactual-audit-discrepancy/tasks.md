## 1. Prompt Engineering (`n8n/prompt-templates`)
- [x] 1.1 Open `n8n/prompt-templates/impact.system.md`.
- [x] 1.2 Locate the instructions regarding strict extraction (Principle 2 or similar). Add the following explicit directive: "If a specific data point, quote, or counterfactual is NOT found in the text, you MUST output a native JSON `null`. Under NO circumstances should you output filler text such as 'Not found', 'None', 'N/A', or 'Not specified'."

## 2. Python Audit Engine Updates (`utils_api`)
- [x] 2.1 Open `utils_api/app/audits/impact.py` and locate the `check_counterfactual_baseline` function.
- [x] 2.2 Define a helper function or lambda within the scope to sanitise the quote:
    ```python
    def is_genuine_qualitative_quote(quote: str) -> bool:
        if not quote or len(quote.strip()) < 10:
            return False
        
        lower_quote = quote.lower()
        denial_phrases = [
            "not found", "no statement", "no counterfactual", 
            "not specified", "unspecified", "none", "n/a",
            "not reported", "no baseline"
        ]
        
        if any(phrase in lower_quote for phrase in denial_phrases):
            return False
            
        return True
    ```
- [x] 2.3 Refactor the evaluation loop to utilise the sanitisation check:
    ```python
    qualitative_quote = None
    
    for metric in record.impact.metrics.metrics:
        cb = metric.counterfactual_baseline
        if cb and cb.source and cb.source.quote:
            
            # Apply heuristic sanitisation to prevent false-positive denial statements
            if not is_genuine_qualitative_quote(cb.source.quote):
                continue

            if cb.value is not None:
                # Immediate Pass if quantified
                base_item.status = "pass"
                base_item.details.elaboration = f"Quote: '{cb.source.quote}'"
                base_item.details.calculation = "A quantified counterfactual baseline was provided."
                return base_item
            elif qualitative_quote is None:
                # Store the first genuine qualitative quote found as a fallback
                qualitative_quote = cb.source.quote

    if qualitative_quote:
        # Downgrade to Warning if only qualitative data exists
        base_item.status = "warning"
        base_item.details.elaboration = f"Quote: '{qualitative_quote}'"
        base_item.details.calculation = "A qualitative counterfactual baseline was provided, but lacked quantified data."
        return base_item

    base_item.status = "fail"
    base_item.details.calculation = "No counterfactual baseline was provided."
    return base_item
    ```
- [x] 2.4 Open `utils_api/tests/test_audit_impact.py`.
- [x] 2.5 Update the `test_check_counterfactual_baseline` unit test to assert the new `warning` state when `value` is `None` but a valid narrative `quote` exists.
- [x] 2.6 Add a specific assertion to ensure that passing a `quote` like `"No counterfactual statement found."` correctly results in a `fail`.