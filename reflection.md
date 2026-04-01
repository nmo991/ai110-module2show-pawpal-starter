# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

3 identified core user action features:
	Add pets, Schedule a task, View the day's tasks

My initial UML used a layered design: domain objects for data, a manager for task CRUD, a scheduler for planning, and an explanation service for transparent reasoning.

Core classes and responsibilities:
- `Owner`: stores owner context, available minutes, and preferences.
- `Pet`: stores pet profile information.
- `Task`: represents one care task (type, duration, priority, optional time window).
- `TimeWindow`: value object for earliest/latest preferred timing.
- `TaskManager`: adds, edits, removes, validates, and lists tasks.
- `Scheduler`: ranks tasks, applies constraints, orders selected tasks, and generates a daily plan.
- `ScheduleItem`: represents a scheduled task instance with time placement and reason codes.
- `DailyPlan`: aggregates scheduled and unscheduled tasks for a date and tracks total planned minutes.
- `ExplanationService`: converts reason codes into user-facing explanations of why tasks were chosen and ordered.

This design supports the three core user actions: add pets/tasks, generate a schedule, and view/explain the day's plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, I made several structural updates after reviewing potential bottlenecks:
- I added a `pet_name` field to `Task` so each task is explicitly linked to a pet, which avoids ambiguity in multi-pet scenarios.
- I changed time-related fields from `str` to `datetime.time` in `TimeWindow` and `ScheduleItem` to make ordering and validation less error-prone.
- I added `owner_name` and `pet_name` to `DailyPlan` so each generated plan keeps clear context for display and explanation.
- I introduced a `ReasonCode` enum and updated explanation inputs to use typed reason codes, which creates a clean contract between scheduling and explanation logic.
- I broadened `Owner.preferences` to `dict[str, Any]` to support richer constraint values (not only strings).

These changes were made to improve relationship clarity, reduce type-related bugs in scheduling, and keep the explanation pipeline consistent and maintainable.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

My scheduler considers task priority, whether a task is required, available owner time, preferred time windows, task duration, and recurrence.

I gave required tasks the highest weight because they are the most important care actions to preserve. After that, I used priority and score to rank tasks, then applied the owner's daily time budget so the plan stays realistic. Preferred time windows matter next because some pet care tasks are more useful at a specific time of day, but they should not override required care or basic feasibility.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff in my scheduler is that conflict detection uses a lightweight pairwise overlap check across scheduled items and returns warnings, instead of doing a more advanced optimization pass that auto-resolves all conflicts.

I also reviewed an AI-style suggestion to compress parts of filtering and ordering into dense list-comprehension chains. While that version was more "Pythonic," it reduced readability for debugging and class discussion. I kept the clearer step-by-step version (`rank_tasks` -> `filter_by_constraints` -> `sort_by_time` -> `order_tasks`) because it is easier to reason about and modify, even if it is slightly less compact.

This tradeoff is reasonable for this project because correctness, transparency, and maintainability matter more than micro-optimizations at the current task scale.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot for class brainstorming, UML refinement, implementation help, test generation, and README/reflection cleanup. It was most useful when I gave it a specific file and a narrow task, like generating tests for a single method or asking how two classes should interact.

Being as specific as possible and including the file context produced the best results. Broad prompts were less useful than targeted prompts tied to one phase of the project.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

After designing my UML, I got an AI suggestion that changed the class structure too aggressively and would have made the project harder to explain. I rejected that version and kept the design closer to my UML so the code, tests, and diagram stayed aligned.

I verified the final decision by checking the actual class relationships in `pawpal_system.py`, running the test suite, and making sure the Streamlit UI could use the same objects without extra translation layers.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, task addition to a pet, time-based sorting, recurring task creation, filtering by pet/status, and conflict detection for overlapping or duplicate schedule times.

These tests were important because they cover the core behaviors that make PawPal+ useful: keeping task data consistent, producing a predictable schedule order, handling recurring care, and warning the owner when a plan is impossible or conflicting.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am very confident in the current scheduler because the main behaviors are covered by passing tests and the Streamlit UI is wired to the same methods used in the backend.

If I had more time, I would test tasks with invalid time windows, plans that run out of owner availability mid-schedule, exact boundary cases where one task ends when another starts, and recurring tasks with missing or unusual due dates.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the backend, tests, and UI now line up. The scheduler is no longer just a logic layer; it produces sorted plans, recurring tasks, and conflict warnings that the UI can actually show to a user in a readable way.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the scheduling algorithm so it can better resolve conflicts automatically instead of only warning about them. I would also redesign the UI input flow so users can manage multiple pets and richer task types more naturally.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned is that AI is most effective when it is used as a collaborator on small, well-scoped problems, while I stay responsible for architecture, tradeoffs, and verification.
