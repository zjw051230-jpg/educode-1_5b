# MVP-10 Model/Config Caveat Review Plan

## 1. Current Caveat
Current caveat:
- declared position encoding: `rope`
- implemented position encoding: `learned_position_embedding`
- `core_model_feature_parity=false`

## 2. Why This Matters
This matters because the project should keep configuration claims aligned with the model that actually ran.

If the config declares a feature that the core model path does not implement, then later scaling conclusions become harder to interpret:
- the run is valid as a smoke for the implemented path
- the run is not yet a validation of the declared final architecture
- future larger-model claims may inherit avoidable ambiguity

## 3. Why It Did Not Block MVP-8 / MVP-9
This caveat did not block MVP-8 or MVP-9 because those runs were explicitly bounded training-systems checks.

For MVP-8 and MVP-9, the key review goal was:
- can the reviewed public-corpus training loop run end to end
- can it remain finite across bounded steps
- can it write artifacts and verify checkpoint reload

Those goals were satisfied on the implemented model path, even though the declared final-position-encoding target was not yet aligned.

## 4. Review Options
### Option 1. Align config to the implemented model
Adjust the reviewed run configs so they declare `learned_position_embedding` when that is what the current core model actually uses.

Pros:
- removes declaration/runtime mismatch quickly
- makes future smoke results easier to interpret
- lowest-scope near-term correction

Cons:
- does not advance the project toward eventual RoPE support by itself

### Option 2. Implement RoPE later
Keep the current implementation for smoke purposes and plan a later focused RoPE implementation/validation step.

Pros:
- preserves current smoke velocity
- allows RoPE work to be reviewed as a dedicated architecture milestone

Cons:
- mismatch remains until the later implementation lands
- larger-model smoke conclusions remain partially caveated in the meantime

### Option 3. Keep smoke model explicitly separated from the final architecture
Document the current smoke path as a reviewed engineering path distinct from the final intended architecture.

Pros:
- honest separation of engineering validation vs final-model validation
- avoids overstating what current runs prove

Cons:
- adds documentation overhead
- still leaves a declaration/alignment task before stronger architecture claims

## 5. Recommended Next Action
Recommended next action:
- before any `1B` smoke, align config declarations with the actual implementation or create a separate final-architecture validation plan

The immediate priority is not to redesign the model in MVP-10.
The priority is to prevent the next-scale decision from outrunning what the current configs and implementation can honestly claim.
