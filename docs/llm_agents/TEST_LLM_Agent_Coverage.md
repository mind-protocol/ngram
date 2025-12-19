# ngram LLM Agents — Tests: Coverage and Gaps

```
STATUS: DRAFT
CREATED: 2025-12-19
VERIFIED: 2025-12-19 against commit ad538f8
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Provider_Specific_LLM_Subprocesses.md
BEHAVIORS:       ./BEHAVIORS_Gemini_Agent_Output.md
ALGORITHM:       ./ALGORITHM_Gemini_Stream_Flow.md
VALIDATION:      ./VALIDATION_Gemini_Agent_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_LLM_Agent_Code_Architecture.md
THIS:            TEST_LLM_Agent_Coverage.md (you are here)
SYNC:            ./SYNC_LLM_Agents_State.md
```

---

## CURRENT COVERAGE

No automated tests are currently defined for the Gemini adapter.

---

## MANUAL VERIFICATION

### Streaming JSON Format

```
python3 -m ngram.llms.gemini_agent -p "ping" --output-format stream-json
```

Verify:
- Each chunk is a JSON object with type=assistant.
- A final JSON object with type=result includes the full response.

### Plain Text Format

```
python3 -m ngram.llms.gemini_agent -p "ping" --output-format text
```

Verify:
- Only the response text is printed to stdout.

### Missing API Key

```
env -u GEMINI_API_KEY python3 -m ngram.llms.gemini_agent -p "ping"
```

Verify:
- JSON error object is printed.
- Process exits with code 1.

---

## GAPS

- Automated unit tests for JSON stream formatting.
- Integration tests with mocked Gemini SDK.
