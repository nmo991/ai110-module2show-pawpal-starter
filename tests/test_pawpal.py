from datetime import date, time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import (
	DailyPlan,
	Pet,
	Priority,
	Recurrence,
	Scheduler,
	ScheduleItem,
	Task,
	TaskManager,
	TaskStatus,
	TaskType,
	TimeWindow,
)


def _sample_task(task_id: str = "t1", pet_name: str = "Mochi") -> Task:
	return Task(
		id=task_id,
		pet_name=pet_name,
		title="Morning Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
		preferred_time_window=TimeWindow(earliest=time(7, 0), latest=time(9, 0)),
	)


def test_mark_complete_changes_task_status() -> None:
	task = _sample_task()

	assert task.status == TaskStatus.PENDING

	task.mark_complete()

	assert task.status == TaskStatus.COMPLETE


def test_add_task_to_pet_increases_task_count() -> None:
	pet = Pet(name="Mochi", species="dog")
	task = _sample_task(pet_name="Mochi")
	initial_count = len(pet.tasks)

	pet.add_task(task)

	assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_orders_by_earliest_then_untimed() -> None:
	scheduler = Scheduler()

	early = Task(
		id="t-early",
		pet_name="Mochi",
		title="Breakfast",
		task_type=TaskType.FEED,
		duration_minutes=15,
		priority=Priority.MEDIUM,
		preferred_time_window=TimeWindow(earliest=time(8, 0), latest=time(9, 0)),
	)
	late = Task(
		id="t-late",
		pet_name="Mochi",
		title="Evening Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
		preferred_time_window=TimeWindow(earliest=time(18, 0), latest=time(20, 0)),
	)
	untimed = Task(
		id="t-untimed",
		pet_name="Mochi",
		title="Play Time",
		task_type=TaskType.PLAY,
		duration_minutes=20,
		priority=Priority.LOW,
	)

	ordered = scheduler.sort_by_time([late, untimed, early])

	assert [task.id for task in ordered] == ["t-early", "t-late", "t-untimed"]


def test_order_tasks_returns_chronological_schedule_items() -> None:
	scheduler = Scheduler()

	morning = Task(
		id="t-morning",
		pet_name="Mochi",
		title="Breakfast",
		task_type=TaskType.FEED,
		duration_minutes=20,
		priority=Priority.MEDIUM,
		preferred_time_window=TimeWindow(earliest=time(8, 0), latest=time(9, 0)),
	)
	afternoon = Task(
		id="t-afternoon",
		pet_name="Mochi",
		title="Afternoon Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
		preferred_time_window=TimeWindow(earliest=time(13, 0), latest=time(15, 0)),
	)

	items = scheduler.order_tasks(scheduler.sort_by_time([afternoon, morning]))

	assert [item.task.id for item in items] == ["t-morning", "t-afternoon"]
	assert [item.start_time for item in items] == sorted(item.start_time for item in items)


def test_filter_tasks_by_status_or_pet_name() -> None:
	manager = TaskManager()

	mochi_pending = Task(
		id="t-mochi-pending",
		pet_name="Mochi",
		title="Morning Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
	)
	mochi_done = Task(
		id="t-mochi-done",
		pet_name="Mochi",
		title="Breakfast",
		task_type=TaskType.FEED,
		duration_minutes=15,
		priority=Priority.MEDIUM,
	)
	luna_done = Task(
		id="t-luna-done",
		pet_name="Luna",
		title="Grooming",
		task_type=TaskType.GROOM,
		duration_minutes=20,
		priority=Priority.LOW,
	)

	mochi_done.mark_complete()
	luna_done.mark_complete()

	manager.add_task(mochi_pending)
	manager.add_task(mochi_done)
	manager.add_task(luna_done)

	completed = manager.filter_tasks(status=TaskStatus.COMPLETE)
	assert {task.id for task in completed} == {"t-mochi-done", "t-luna-done"}

	for_mochi = manager.filter_tasks(pet_name="Mochi")
	assert {task.id for task in for_mochi} == {"t-mochi-pending", "t-mochi-done"}

	mochi_completed = manager.filter_tasks(status=TaskStatus.COMPLETE, pet_name="Mochi")
	assert [task.id for task in mochi_completed] == ["t-mochi-done"]


def test_complete_daily_task_creates_next_occurrence() -> None:
	manager = TaskManager()
	task = Task(
		id="t-daily",
		pet_name="Mochi",
		title="Daily Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
		recurrence=Recurrence.DAILY,
		due_date=date(2026, 3, 31),
	)
	manager.add_task(task)

	next_task = manager.complete_task("t-daily")

	assert task.status == TaskStatus.COMPLETE
	assert next_task is not None
	assert next_task.status == TaskStatus.PENDING
	assert next_task.recurrence == Recurrence.DAILY
	assert next_task.due_date == date(2026, 4, 1)
	assert next_task.id == "t-daily-2026-04-01"


def test_complete_weekly_task_creates_next_occurrence() -> None:
	manager = TaskManager()
	task = Task(
		id="t-weekly",
		pet_name="Luna",
		title="Weekly Grooming",
		task_type=TaskType.GROOM,
		duration_minutes=20,
		priority=Priority.MEDIUM,
		recurrence=Recurrence.WEEKLY,
		due_date=date(2026, 3, 31),
	)
	manager.add_task(task)

	next_task = manager.complete_task("t-weekly")

	assert task.status == TaskStatus.COMPLETE
	assert next_task is not None
	assert next_task.recurrence == Recurrence.WEEKLY
	assert next_task.due_date == date(2026, 4, 7)
	assert next_task.id == "t-weekly-2026-04-07"


def test_detect_conflicts_returns_warning_instead_of_crash() -> None:
	scheduler = Scheduler()

	mochi_task = Task(
		id="t-mochi-overlap",
		pet_name="Mochi",
		title="Morning Walk",
		task_type=TaskType.WALK,
		duration_minutes=30,
		priority=Priority.HIGH,
	)
	luna_task = Task(
		id="t-luna-overlap",
		pet_name="Luna",
		title="Vet Prep",
		task_type=TaskType.VET,
		duration_minutes=30,
		priority=Priority.MEDIUM,
	)

	mochi_plan = DailyPlan(
		date="2026-03-31",
		owner_name="Jordan",
		pet_name="Mochi",
		items=[
			ScheduleItem(task=mochi_task, start_time=time(8, 0), end_time=time(8, 30)),
		],
	)
	luna_plan = DailyPlan(
		date="2026-03-31",
		owner_name="Jordan",
		pet_name="Luna",
		items=[
			ScheduleItem(task=luna_task, start_time=time(8, 15), end_time=time(8, 45)),
		],
	)

	warnings = scheduler.detect_conflicts([mochi_plan, luna_plan])

	assert len(warnings) == 1
	assert "Conflict detected" in warnings[0]
	assert "Mochi" in warnings[0]
	assert "Luna" in warnings[0]


def test_detect_conflicts_flags_duplicate_times() -> None:
	scheduler = Scheduler()

	mochi_task = Task(
		id="t-mochi-duplicate",
		pet_name="Mochi",
		title="Medication",
		task_type=TaskType.MED,
		duration_minutes=15,
		priority=Priority.HIGH,
	)
	luna_task = Task(
		id="t-luna-duplicate",
		pet_name="Luna",
		title="Feeding",
		task_type=TaskType.FEED,
		duration_minutes=15,
		priority=Priority.MEDIUM,
	)

	mochi_plan = DailyPlan(
		date="2026-03-31",
		owner_name="Jordan",
		pet_name="Mochi",
		items=[
			ScheduleItem(task=mochi_task, start_time=time(9, 0), end_time=time(9, 15)),
		],
	)
	luna_plan = DailyPlan(
		date="2026-03-31",
		owner_name="Jordan",
		pet_name="Luna",
		items=[
			ScheduleItem(task=luna_task, start_time=time(9, 0), end_time=time(9, 15)),
		],
	)

	warnings = scheduler.detect_conflicts([mochi_plan, luna_plan])

	assert len(warnings) == 1
	assert "Conflict detected" in warnings[0]
	assert "09:00-09:15" in warnings[0]
