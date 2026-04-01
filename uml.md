classDiagram
class Owner {
  +name: str
  +daily_available_minutes: int
  +preferences: dict
  +set_preference(key, value)
  +get_preference(key)
}

class Pet {
  +name: str
  +species: str
  +age: int | None
  +notes: str | None
  +tasks: list~Task~
  +update_profile(...)
  +add_task(task)
}

class Task {
  +id: str
  +pet_name: str
  +title: str
  +task_type: TaskType
  +duration_minutes: int
  +priority: Priority
  +is_required: bool
  +preferred_time_window: TimeWindow | None
  +status: TaskStatus
  +recurrence: Recurrence
  +due_date: date | None
  +validate()
  +estimate_score()
  +mark_complete() Task | None
  +create_next_occurrence() Task | None
}

class TaskManager {
  +tasks: list~Task~
  +add_task(task)
  +edit_task(task_id, updates)
  +remove_task(task_id)
  +complete_task(task_id) Task | None
  +list_tasks()
  +list_tasks_for_pet(pet_name)
  +filter_tasks(status, pet_name)
  +get_required_tasks()
  +validate_tasks()
}

class Scheduler {
  +generate_daily_plan(owner, pet, tasks, date) DailyPlan
  +rank_tasks(tasks, owner, pet) list~Task~
  +filter_by_constraints(tasks, owner) list~Task~
  +apply_time_windows(tasks) list~Task~
  +sort_by_time(tasks) list~Task~
  +order_tasks(tasks) list~ScheduleItem~
  +calculate_total_minutes(items) int
  +detect_conflicts(plans) list~str~
  +_overlaps(left, right) bool
}

class ScheduleItem {
  +task: Task
  +start_time: time
  +end_time: time
  +reason_codes: list~ReasonCode~
  +duration() int
}

class DailyPlan {
  +date: str
  +owner_name: str
  +pet_name: str
  +items: list~ScheduleItem~
  +unscheduled_tasks: list~Task~
  +total_minutes: int
  +add_item(item)
  +add_unscheduled(task)
  +summary()
}

class ExplanationService {
  +explain_item(item, context) str
  +explain_plan(plan, context) list~str~
  +reason_code_to_text(code) str
}

class Priority {
  <<enumeration>>
  LOW
  MEDIUM
  HIGH
}

class TaskStatus {
  <<enumeration>>
  PENDING
  COMPLETE
}

class Recurrence {
  <<enumeration>>
  NONE
  DAILY
  WEEKLY
}

class ReasonCode {
  <<enumeration>>
  REQUIRED_TASK
  HIGH_PRIORITY
  FIT_AVAILABLE_TIME
  MATCHED_PREFERENCE
  TIME_WINDOW_RESPECTED
}

class TaskType {
  <<enumeration>>
  WALK
  FEED
  MED
  GROOM
  VET
  PLAY
  OTHER
}

class TimeWindow {
  +earliest: time
  +latest: time
}

Owner "1" ..> "0..*" Task : constrains
Pet "1" o-- "0..*" Task : has
TaskManager "1" o-- "0..*" Task : manages
Scheduler ..> Owner : uses
Scheduler ..> Pet : uses
Scheduler ..> Task : schedules
Scheduler --> DailyPlan : produces
DailyPlan "1" o-- "0..*" ScheduleItem : contains
ScheduleItem --> Task : wraps
ExplanationService ..> DailyPlan : explains
ExplanationService ..> ScheduleItem : explains
ExplanationService ..> ReasonCode : maps
Task --> Priority
Task --> TaskStatus
Task --> Recurrence
Task --> TaskType
Task --> TimeWindow
ScheduleItem --> ReasonCode