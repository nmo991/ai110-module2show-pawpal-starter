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
  +age: int
  +notes: str
  +update_profile(...)
}

class Task {
  +id: str
  +title: str
  +task_type: TaskType
  +duration_minutes: int
  +priority: Priority
  +is_required: bool
  +preferred_time_window: TimeWindow
  +validate()
  +estimate_score()
}

class TaskManager {
  +tasks: list~Task~
  +add_task(task)
  +edit_task(task_id, updates)
  +remove_task(task_id)
  +list_tasks()
  +get_required_tasks()
  +validate_tasks()
}

class Scheduler {
  +generate_daily_plan(owner, pet, tasks, date) DailyPlan
  +rank_tasks(tasks, owner, pet) list~Task~
  +filter_by_constraints(tasks, owner) list~Task~
  +order_tasks(tasks) list~ScheduleItem~
  +calculate_total_minutes(items) int
}

class ScheduleItem {
  +task: Task
  +start_time: str
  +end_time: str
  +reason_codes: list~str~
  +duration() int
}

class DailyPlan {
  +date: str
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
  +earliest: str
  +latest: str
}

Owner "1" --> "0..*" Task : defines constraints for
Pet "1" --> "0..*" Task : receives
TaskManager "1" o-- "0..*" Task : manages
Scheduler ..> Owner : uses
Scheduler ..> Pet : uses
Scheduler ..> Task : schedules
Scheduler --> DailyPlan : produces
DailyPlan "1" o-- "0..*" ScheduleItem : contains
ScheduleItem --> Task : wraps
ExplanationService ..> DailyPlan : explains
Task --> Priority
Task --> TaskType
Task --> TimeWindow