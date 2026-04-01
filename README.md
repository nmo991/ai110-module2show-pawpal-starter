# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

Recent scheduler improvements include:

- Time-aware sorting: tasks can be sorted by preferred start windows, with untimed tasks placed last.
- Flexible task filtering: tasks can be filtered by completion status, pet name, or both.
- Recurring task support: completing daily or weekly tasks automatically creates the next occurrence.
- Conflict detection warnings: overlapping scheduled tasks are detected across pets and returned as warning messages (without crashing the app).
- Explanation-ready output: schedule items carry reason codes that are converted into user-facing plan explanations.

## Testing PawPal+

Run the test suite with:

```
python -m pytest
```

Current tests cover the core scheduling logic, including chronological task sorting, recurring task creation when daily and weekly tasks are completed, task filtering by pet/status, and conflict detection for overlapping or duplicate schedule times.

Confidence Level: 5/5 stars

Based on the latest run, all tests passed (9 passed), which gives strong confidence in the reliability of the current scheduling behaviors.
