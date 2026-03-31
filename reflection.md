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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
