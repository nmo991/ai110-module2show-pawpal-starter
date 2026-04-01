# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner plan care tasks, generate a daily schedule, and explain why each task was chosen.

## Features

- Task ranking: required tasks are prioritized first, then higher-scoring tasks, shorter tasks, and alphabetical ties.
- Time-window sorting: tasks with preferred windows are ordered by earliest start time before untimed tasks.
- Budget filtering: the scheduler keeps tasks within the owner’s available minutes when possible.
- Recurring tasks: completing a daily or weekly task creates the next occurrence automatically.
- Conflict detection: overlapping schedule items are flagged so the owner can fix timing issues.
- Explanation output: each scheduled item includes reason codes that become readable plan explanations.

## Optional Features Implemented

- Sorted task preview in the Streamlit UI so users can see the scheduler order before generating a plan.
- Pending-task count and filtered task view to make the task list easier to scan.
- Conflict warnings shown with a clear `st.warning` message plus the specific overlapping task details.
- Streamlit session-state recovery for older saved app state, so the UI keeps working after code updates.
- Friendly success messages when no conflicts are found, so the plan status is easy to understand.

## Screenshots

### Task preview and generated plan

<a href="/screenshot1.png" target="_blank"><img src='/screenshot1.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

### App input and task list

<a href="/screenshot2.png" target="_blank"><img src='/screenshot2.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Testing PawPal+

Run the test suite with:

```bash
pip install pytest
python -m pytest
```

Current tests cover the core scheduling logic, including chronological task sorting, recurring task creation when daily and weekly tasks are completed, task filtering by pet/status, and conflict detection for overlapping or duplicate schedule times.

Confidence Level: 5/5 stars

Based on the latest run, all tests passed (9 passed), which gives strong confidence in the reliability of the current scheduling behaviors.
