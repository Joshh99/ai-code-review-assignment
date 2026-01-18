# AI Code Review Assignment (Python)

## Candidate
- Name: Joshua Wisdom Momo (joshuawisdom92@gmail.com)
- Approximate time spent: 100 minutes

---

# Task 1 — Average Order Value

## 1) Code Review Findings
### Critical bugs
- Incorrect denominator: The function divides by len(orders) (total count) but only sums non-cancelled orders, resulting in mathematically incorrect averages. It should divide by count of non-cancelled orders only.
- Division by zero: Empty input list causes ZeroDivisionError when len(orders) returns 0.

### Edge cases & risks
- None input: Function crashes if orders is None (cannot call len() on None).
- All cancelled orders: If every order is cancelled, the sum is 0 but count is len(orders), returning 0.0 average (technically correct but via wrong calculation).
- Missing keys: No validation that orders contain required "status" and "amount" keys - will raise KeyError.
- Non-numeric amounts: If "amount" is a string or None, attempting to add it to total will fail with TypeError.
- Non-dict entries: If the list contains non-dictionary items, accessing order["status"] will crash.

### Code quality / design issues
- Silent assumptions: Code assumes well-formed input without any validation or error handling.
- No type hints or docstring: Missing documentation about expected input format and return value.
- Inconsistent handling: Filters by status but doesn't validate data quality.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Fixed denominator to count only non-cancelled orders (the actual bug causing incorrect averages)
- Added input validation to handle None and empty inputs gracefully
- Added type checking to skip non-dictionary entries instead of crashing
- Added key validation to skip orders missing required fields
- Added exception handling for non-numeric amounts with graceful degradation
- Returns 0.0 for edge cases (empty input, all cancelled, no valid orders) instead of crashing
- Added comprehensive docstring documenting behavior

Design philosophy: I chose graceful degradation over failing fast. In batch processing contexts (like calculating metrics across many orders), it's better to skip invalid entries and compute from valid data rather than crash the entire operation. Invalid entries could be logged separately for investigation.

### Corrected code
See `correct_task1.py`

> Note: The original AI-generated code is preserved in `task1.py`.

 ### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?

Critical Path:
- Empty orders list → should return 0.0 (prevents division by zero)
- All cancelled orders → should return 0.0 (no valid orders to average)
- Mix of cancelled and non-cancelled → correct average of non-cancelled only
- Single non-cancelled order → should return that order's amount

I'll test Edge cases:
- None input → should return 0.0 (graceful handling)
- Non-list iterables (tuple, set) → should work if they contain valid orders
- Orders with missing "status" key → should skip and continue
- Orders with missing "amount" key → should skip and continue
- Non-dictionary items in list → should skip and continue
- String amounts that can convert to float (e.g., "42.50") → should work
- String amounts that cannot convert (e.g., "invalid") → should skip
- None as amount value → should skip
- Negative amounts → currently allowed (may need to clarify this from business logic)
- Zero amounts → currently allowed and included in average

I'll test Data Quality scenarios:
- Mixed valid and invalid orders → should compute average from valid ones only
- Orders with extra fields → should ignore extra fields, process normally

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function calculates average order value by summing the amounts of all non-cancelled orders and dividing by the number of orders. It correctly excludes cancelled orders from the calculation.

### Issues in original explanation
- It is not factually incorrect: It claims it "correctly excludes cancelled orders" but actually divides by total count, not non-cancelled count. The math is wrong.
- It omits critical issues: It doesn't mention the risk of dividing by zero, no error handling, or assumptions about input validity.

### Rewritten explanation
- Iterates through the orders list
- Filters out cancelled orders and invalid entries (non-dicts, missing keys, non-numeric amounts)
- Sums the amounts of valid, non-cancelled orders
- Divides by the count of valid, non-cancelled orders (not the total count)
- Returns 0.0 if the input is empty, None, or contains no valid orders. Invalid entries are skipped gracefully rather than causing the function to crash, making it resilient in batch processing scenarios.

## 4) Final Judgment
- Decision: Request Changes
- Justification:The original code contains a critical mathematical bug that produces incorrect results; it divides by the total count instead of the count of non-cancelled orders.This makes every average calculation wrong unless all orders happen to be non-cancelled. It doesn't handle error and will crash on empty input, None, or malformed data.
The core logic (filtering cancelled orders) is sound though, but the implementation has fundamental issues. 
- Confidence & unknowns: I have high confidence the mathematical bug needs fixing. I have high confidence the division by zero protection is necessary. 
My confidence is medium on graceful degradation approach. In some contexts, fail-fast with clear exceptions might be preferred over silently skipping invalid data. The right choice depends on whether this is used for real-time API responses (fail-fast better) or batch analytics (graceful better). I assumed batch processing context.
Unknown: Business logic questions like whether negative amounts or zero amounts should be allowed, and whether there are other order statuses besides "cancelled" that should be filtered (e.g., "pending", "refunded").

---

# Task 2 — Count Valid Emails

## 1) Code Review Findings
### Critical bugs
- Simply checking if "@" in email is far too weak. It accepts invalid formats like "@@@@", "user@", "@domain", "multiple@at@symbols", "user @domain.com" (with spaces), etc.
- No validation that items in the list are strings. Will crash with TypeError if email is None, an integer, or any non-string type when trying to use the in operator.
- Doesn't check for local part, domain part, or top-level domain (TLD) structure.

### Edge cases & risks
- If emails is None, the for loop will crash with TypeError.
- List containing integers, None, or other types will crash on "@" in email.
- Email with leading/trailing spaces would fail the weak "@" check.
- Empty strings would be counted as invalid (no "@"), but no explicit handling. 
- Multiple @ symbols like in "user@@domain.com" would pass the current implementation.
- Missing domain/local part like  "user@" or "@domain.com" would pass if they contain "@"
- "user@domain" would pass but isn't a valid email format.

### Code quality / design issues
- Missing docstring explaining what constitutes a "valid" email.
- Assumes all elements are strings without validation.
- Poor separation of concerns;validation logic and counting are coupled.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Added input validation to handle None and empty inputs gracefully
- Added type checking to skip non-string elements instead of crashing
- Added whitespace trimming to handle emails with leading/trailing spaces
- Implemented proper email structure validation:
        Exactly one @ symbol (not zero, not multiple)
        Non-empty local part (before @)
        Non-empty domain part (after @)
        Domain must contain at least one dot (for TLD)
        Domain cannot start or end with dot
        TLD (last part of domain) must be at least 2 characters
- Added comprehensive docstring documenting behavior and validation rules
- Maintains graceful degradation approach: skips invalid entries rather than crashing

Design Philosophy: I used baalanced validation. I focused on catching common invalid formats without over-engineering (no regex). It validates structural requirements that real emails must have while remaining readable and maintainable.

### Corrected code
See `correct_task2.py`

> Note: The original AI-generated code is preserved in `task2.py`. 


### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?
- Empty list → should return 0
- Valid emails with common formats → counted
- Mix of valid and invalid emails → should count only valid ones
- All invalid emails → should return 0
- Invalid patterns (`"@"`, `"user@"`, `"@domain"`, `"a@b@c"`) → rejected
- Edge cases: whitespace, multiple `@`, domains without dots → handled
- Non-string entries in list → silently skipped
- List with non-string elements (integers, None, dicts) → should skip them
- List with only non-strings → should return 0

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function counts the number of valid email addresses in the input list. It safely ignores invalid entries and handles empty input correctly.

### Issues in original explanation
- It makes incorrect claim about "valid" emails. The validation is so weak (just checking for "@") that it accepts obviously invalid formats. Calling them "valid email addresses" is misleading.
- It's partially true about empty input. It handles empty lists correctly (returns 0), but crashes on None input.

### Rewritten explanation
- Must be a string (non-strings are skipped)
- Contains exactly one @ symbol
- Has non-empty local part (before @) and domain part (after @)
- Domain contains at least one dot (separating domain from TLD)
- Domain doesn't start or end with a dot
- Top-level domain (TLD) is at least 2 characters

## 4) Final Judgment
- Decision: Reject
- Justification: Checking only for the presence of "@" anywhere in the string is insufficient. The validation is so weak it provides negligible value over simply returning len(emails). A complete rewrite is required; the validation logic needs fundamental restructuring.
- Confidence & unknowns: I have high confidence -> `@` check is objectively insufficient for email validation. I have high confidence -> type checking needed to prevent crashes on non-string inputs
Unknowns: Graceful degradation vs. exception raising depends on use case. Case sensitivity requirements unspecified. Special character handling in local part follows permissive approach.

---

# Task 3 — Aggregate Valid Measurements

## 1) Code Review Findings
### Critical bugs
- The function divides by len(values) (total count including None) but only sums non-None values, resulting in mathematically incorrect averages. Should divide by count of valid numeric values only.
-  Empty input list causes ZeroDivisionError when len(values) returns 0. 
- float(v) will raise ValueError for non-numeric strings (e.g., "invalid", "N/A", "") and TypeError for unconvertible types (e.g., lists, dicts). No exception handling.

### Edge cases & risks
- Function crashes if values is None (cannot call len() on None).
- If list contains only non-numeric strings, first invalid value causes crash.
- No mechanism to skip invalid values - first invalid one crashes the function.
- Empty string "" will crash when passed to float().
- Concerning string numbers, "42.5" should convert fine, but "42.5°C" or "42,500" will crash.

### Code quality / design issues
- It assumes all non-None values are numeric without validation.
- It is missing docstring about expected input format, what counts as "valid", and return behavior.
- It has fragile error handling. First invalid value crashes entire function.
- It has inconsistent filtering. Filters None but not other invalid types.

## 2) Proposed Fixes / Improvements
### Summary of changes
- Fixed denominator to count only valid numeric values (the actual bug causing incorrect averages)
- Added input validation to handle None and empty inputs gracefully
- Added try-except block around float() conversion to handle non-numeric values
- Changed to skip invalid values rather than crash (graceful degradation)
- Returns 0.0 for edge cases (empty input, all None, all invalid, no valid values)
- Added comprehensive docstring documenting behavior
- Explicitly continue on None before attempting conversion (clearer logic flow)

Design philosophy: I chose graceful degradation for batch processing contexts. In measurement aggregation scenarios (sensors, analytics, data pipelines), it's better to compute averages from valid data while skipping bad readings rather than crash on one malformed value. Invalid values could be logged separately for investigation.

### Corrected code
See `correct_task3.py`

> Note: The original AI-generated code is preserved in `task3.py`.

### Testing Considerations
If you were to test this function, what areas or scenarios would you focus on, and why?
- Empty list → should return 0.0 (prevents division by zero)
- All None values → should return 0.0 (no valid measurements)
- All valid numeric values → correct average calculation
- Mix of None and valid numbers → correct average of non-None values only
- String numbers: ["1.5", "2.5"] → should convert and average correctly
- Mixed types: [1, 2.5, "3.5", None] → should handle all, average valid ones
- Non-numeric strings: ["invalid", "N/A", ""] → should skip all, return 0.0
- Mixed valid and invalid: [1, 2, "invalid", None, 3] → should return 2.0 (average of 1,2,3)
- Zero values: [0, 0, 0] → should return 0.0
- Special float strings: ["inf", "-inf", "nan"] → currently would convert and include (may need business logic clarification)

## 3) Explanation Review & Rewrite
### AI-generated explanation (original)
> This function calculates the average of valid measurements by ignoring missing values (None) and averaging the remaining values. It safely handles mixed input types and ensures an accurate average

### Issues in original explanation
- It makes a factually incorrect claim. It claims "accurate average" but divides by total count instead of valid count.
- Its explanation about None handling is incomplete; it says it "ignores" None, but doesn't explain this creates a denominator mismatch.
- It doesn't consider edge cases. It doesn't address empty input, all None values, or division by zero risk.

### Rewritten explanation
- Iterates through the values list
- Skips None values (missing measurements)
- Attempts to convert each non-None value to float
- Skips values that cannot be converted to numeric (invalid strings, unconvertible types)
- Sums valid numeric values
- Divides by the count of valid numeric values only (not the total count)

Returns 0.0 if the input is empty, None, or contains no valid numeric values. Invalid entries are skipped gracefully with exception handling.

## 4) Final Judgment
- Decision: Request Changes
- Justification: The original code has the same critical mathematical bug as Task 1 - it divides by the total count of values instead of the count of valid values, producing incorrect averages whenever None values are present. Additionally, the code lacks any exception handling and will crash on the first non-numeric value encountered, despite claiming to "safely handle mixed input types." The None-filtering logic is correct in intent but incomplete in execution.

- Confidence & unknowns: 
Confidence:
High: Mathematical bug must be fixed (wrong denominator)
High: Exception handling needed for float() conversion
High: Division by zero protection required

Unknowns:
Graceful handling vs. fail-fast depends on context (assumed sensor/analytics)
Return 0.0 vs. None vs. exception for no valid data; this depends on business logic decision
Special float values (inf, nan); treat as valid or sensor errors?
Negative measurements validity (domain-dependent)
