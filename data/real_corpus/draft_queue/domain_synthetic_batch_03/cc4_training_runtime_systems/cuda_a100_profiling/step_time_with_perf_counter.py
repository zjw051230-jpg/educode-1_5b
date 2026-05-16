# draft_status: candidate
# topic_id: RTS-009
# source_category: synthetic_examples
# project_backbone: cs_ml_python_transformer_training_systems
# worker_id: CC4
# approved_for_training: false
# contains_external_text: false
# contains_private_data: false
# target_use: draft_review_only

from time import perf_counter


def simulate_training_step(work_units):
    total = 0
    for value in range(work_units):
        total += value * value
    return total


def timed_step(work_units):
    start = perf_counter()
    simulate_training_step(work_units)
    end = perf_counter()
    duration_s = end - start
    return {
        "step_time_s": round(duration_s, 6),
        "work_units": work_units,
    }


for work_units in (1000, 3000, 6000):
    print(timed_step(work_units))

# Teaching note:
# In GPU training, asynchronous execution can complicate timing.
# This tiny example only teaches the shape of a timing helper.
# Real step timing reviews should define where the timer starts and stops.
