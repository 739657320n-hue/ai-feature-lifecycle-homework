# Tool Contracts – AudioGen Assistant

## Tool Allowlist
All tools listed below are the **only** APIs the model may call. Any other tool is rejected at the orchestrator level before reaching the model.

| Tool Name           | Allowed | Parameters (JSON Schema)                                                                 | Permission | Confirmation Required | Error Handling                                 |
|---------------------|---------|-----------------------------------------------------------------------------------------|------------|-----------------------|------------------------------------------------|
| `generate_audio`    | Yes     | See [config/tool_allowlist.yaml](../configs/tool_allowlist.yaml#L1-L15)                  | Write      | Yes (user must type "confirm") | Timeout 30s → retry once → fallback error message; log failure |
| `search_sounds`     | Yes     | `{ "query": { "type": "string" }, "style": { "type": "string", "enum": [ "classical","jazz","electronic","pop","ambient" ] } }` | Read-only  | No             | Timeout 10s → return empty list; log latency |
| `delete_audio`      | **No**  | –                                                                                       | –          | –                     | Reject at orchestrator, log attempt, return error to model |

## Tool Details

### `generate_audio`
- **Parameters**: `prompt` (string, min 3, max 500), `duration_seconds` (number, 1–120), `style` (string, enum, optional)
- **Permission**: Write – modifies state (creates a new audio file)
- **Confirmation**: User must explicitly approve the exact parameters in the same session before execution.
- **Error Handling**: 
  1. Timeout (30s) → retry once with same parameters.
  2. If still failing → return `{"error_code": "timeout"}` and do not auto-retry.
  3. All errors logged with originating trace ID.

### `search_sounds`
- **Parameters**: `query` (string), `style` (optional enum)
- **Permission**: Read-only – no state change.
- **Confirmation**: Not required.
- **Error Handling**: Timeout (10s) → return empty list; log high latency.

## Access Control
- Tool access is granted per feature and per user role. Default deny.
- Write tools require explicit opt-in and are logged separately for auditing.

## Fail‑Closed Principle
Any tool not on this list is **blocked** at the orchestrator before the model sees the request. The call is logged and an error response is returned to the model.