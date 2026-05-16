# draft_status: candidate
# topic_id: RTS-002
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from math import isclose


def flatten_named_parameters(named_parameters):
    flat = {}
    for name, values in named_parameters.items():
        flat[name] = [float(x) for x in values]
    return flat


def parameters_match(before_reload, after_reload, tol=1e-8):
    before = flatten_named_parameters(before_reload)
    after = flatten_named_parameters(after_reload)

    if set(before) != set(after):
        return False, "parameter name mismatch"

    for name in before:
        left = before[name]
        right = after[name]
        if len(left) != len(right):
            return False, f"length mismatch for {name}"
        for index, (a, b) in enumerate(zip(left, right)):
            if not isclose(a, b, rel_tol=tol, abs_tol=tol):
                return False, f"value mismatch for {name}[{index}]"
    return True, "all parameters match"


saved_state = {
    "embed.weight": [0.10, 0.25, -0.30],
    "proj.weight": [0.50, -0.20, 0.90],
}

reloaded_state = {
    "embed.weight": [0.10, 0.25, -0.30],
    "proj.weight": [0.50, -0.20, 0.90],
}

ok, message = parameters_match(saved_state, reloaded_state)
print({"reload_ok": ok, "message": message})

# Teaching note:
# Equality checks are useful for structural validation.
# They do not prove that the checkpoint came from a good run.
# They only show that the serialized parameter values survived roundtrip.
