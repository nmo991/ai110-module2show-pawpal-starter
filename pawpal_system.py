from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Any


class Priority(Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"


class TaskType(Enum):
	WALK = "walk"
	FEED = "feed"
	MED = "med"
	GROOM = "groom"
	VET = "vet"
	PLAY = "play"
	OTHER = "other"


class ReasonCode(Enum):
	REQUIRED_TASK = "required_task"
	HIGH_PRIORITY = "high_priority"
	FIT_AVAILABLE_TIME = "fit_available_time"
	MATCHED_PREFERENCE = "matched_preference"
	TIME_WINDOW_RESPECTED = "time_window_respected"


class TaskStatus(Enum):
	PENDING = "pending"
	COMPLETE = "complete"


@dataclass
class TimeWindow:
	earliest: time
	latest: time


@dataclass
class Owner:
	name: str
	daily_available_minutes: int
	preferences: dict[str, Any] = field(default_factory=dict)

	def set_preference(self, key: str, value: str) -> None:
		"""Store or update a named owner preference."""
		self.preferences[key] = value

	def get_preference(self, key: str) -> str | None:
		"""Return a string preference value by key if present."""
		value = self.preferences.get(key)
		return value if isinstance(value, str) else None


@dataclass
class Pet:
	name: str
	species: str
	age: int | None = None
	notes: str | None = None
	tasks: list[Task] = field(default_factory=list)

	def update_profile(
		self,
		*,
		name: str | None = None,
		species: str | None = None,
		age: int | None = None,
		notes: str | None = None,
	) -> None:
		"""Apply optional profile field updates to the pet."""
		if name is not None:
			self.name = name
		if species is not None:
			self.species = species
		if age is not None:
			if age < 0:
				raise ValueError("age cannot be negative")
			self.age = age
		if notes is not None:
			self.notes = notes

	def add_task(self, task: Task) -> None:
		"""Attach a validated task to this pet."""
		if task.pet_name != self.name:
			raise ValueError("task pet_name must match pet name")
		task.validate()
		self.tasks.append(task)


@dataclass
class Task:
	id: str
	pet_name: str
	title: str
	task_type: TaskType
	duration_minutes: int
	priority: Priority
	is_required: bool = False
	preferred_time_window: TimeWindow | None = None
	status: TaskStatus = TaskStatus.PENDING

	def validate(self) -> None:
		"""Validate required task fields and time constraints."""
		if not self.id.strip():
			raise ValueError("task id is required")
		if not self.pet_name.strip():
			raise ValueError("pet_name is required")
		if not self.title.strip():
			raise ValueError("task title is required")
		if self.duration_minutes <= 0:
			raise ValueError("duration must be greater than 0")
		if self.duration_minutes > 24 * 60:
			raise ValueError("duration cannot exceed one day")
		if self.preferred_time_window is not None:
			if self.preferred_time_window.earliest >= self.preferred_time_window.latest:
				raise ValueError("time window earliest must be before latest")

	def estimate_score(self) -> float:
		"""Compute a simple scheduling score from priority and flags."""
		priority_weight = {
			Priority.LOW: 1.0,
			Priority.MEDIUM: 2.0,
			Priority.HIGH: 3.0,
		}
		score = priority_weight[self.priority]
		if self.is_required:
			score += 2.0
		if self.preferred_time_window is not None:
			score += 0.5
		return score

	def mark_complete(self) -> None:
		"""Mark this task as completed."""
		self.status = TaskStatus.COMPLETE


@dataclass
class ScheduleItem:
	task: Task
	start_time: time
	end_time: time
	reason_codes: list[ReasonCode] = field(default_factory=list)

	def duration(self) -> int:
		"""Return scheduled duration in minutes."""
		start_minutes = _time_to_minutes(self.start_time)
		end_minutes = _time_to_minutes(self.end_time)
		if end_minutes < start_minutes:
			end_minutes += 24 * 60
		return end_minutes - start_minutes


@dataclass
class DailyPlan:
	date: str
	owner_name: str
	pet_name: str
	items: list[ScheduleItem] = field(default_factory=list)
	unscheduled_tasks: list[Task] = field(default_factory=list)
	total_minutes: int = 0

	def add_item(self, item: ScheduleItem) -> None:
		"""Add a scheduled item and update total planned time."""
		self.items.append(item)
		self.total_minutes += item.duration()

	def add_unscheduled(self, task: Task) -> None:
		"""Record a task that could not be scheduled."""
		self.unscheduled_tasks.append(task)

	def summary(self) -> str:
		"""Build a human-readable summary of the daily plan."""
		lines: list[str] = [f"Daily plan for {self.pet_name} on {self.date}"]
		for item in self.items:
			lines.append(
				f"- {item.start_time.strftime('%H:%M')}-{item.end_time.strftime('%H:%M')}: {item.task.title}"
			)
		if self.unscheduled_tasks:
			lines.append("Unscheduled tasks:")
			for task in self.unscheduled_tasks:
				lines.append(f"- {task.title}")
		lines.append(f"Total planned minutes: {self.total_minutes}")
		return "\n".join(lines)


@dataclass
class TaskManager:
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a new validated task with a unique id."""
		task.validate()
		if any(existing.id == task.id for existing in self.tasks):
			raise ValueError(f"task id already exists: {task.id}")
		self.tasks.append(task)

	def edit_task(self, task_id: str, updates: dict[str, Any]) -> None:
		"""Update task fields by id and re-validate the task."""
		task = next((item for item in self.tasks if item.id == task_id), None)
		if task is None:
			raise KeyError(f"task not found: {task_id}")

		for key, value in updates.items():
			if not hasattr(task, key):
				raise ValueError(f"unknown task field: {key}")
			setattr(task, key, value)

		task.validate()

	def remove_task(self, task_id: str) -> None:
		"""Remove a task by id or raise if it does not exist."""
		before = len(self.tasks)
		self.tasks = [task for task in self.tasks if task.id != task_id]
		if len(self.tasks) == before:
			raise KeyError(f"task not found: {task_id}")

	def list_tasks(self) -> list[Task]:
		"""Return a copy of all managed tasks."""
		return list(self.tasks)

	def list_tasks_for_pet(self, pet_name: str) -> list[Task]:
		"""Return tasks belonging to a specific pet."""
		return [task for task in self.tasks if task.pet_name == pet_name]

	def get_required_tasks(self) -> list[Task]:
		"""Return only tasks marked as required."""
		return [task for task in self.tasks if task.is_required]

	def validate_tasks(self) -> None:
		"""Validate all tasks and ensure task ids are unique."""
		seen: set[str] = set()
		for task in self.tasks:
			task.validate()
			if task.id in seen:
				raise ValueError(f"duplicate task id: {task.id}")
			seen.add(task.id)


class Scheduler:
	def generate_daily_plan(
		self, owner: Owner, pet: Pet, tasks: list[Task], date: str
	) -> DailyPlan:
		"""Generate a daily plan for one pet from candidate tasks."""
		pet_tasks = [task for task in tasks if task.pet_name == pet.name]
		for task in pet_tasks:
			task.validate()

		ranked = self.rank_tasks(pet_tasks, owner, pet)
		selected = self.filter_by_constraints(ranked, owner)
		windowed = self.apply_time_windows(selected)
		ordered_items = self.order_tasks(windowed)

		plan = DailyPlan(date=date, owner_name=owner.name, pet_name=pet.name)
		for item in ordered_items:
			plan.add_item(item)

		scheduled_ids = {item.task.id for item in ordered_items}
		for task in pet_tasks:
			if task.id not in scheduled_ids:
				plan.add_unscheduled(task)

		return plan

	def rank_tasks(self, tasks: list[Task], owner: Owner, pet: Pet) -> list[Task]:
		"""Rank tasks by required flag, score, and deterministic tie-breakers."""
		_ = owner
		_ = pet
		return sorted(
			tasks,
			key=lambda task: (
				not task.is_required,
				-task.estimate_score(),
				task.duration_minutes,
				task.title.lower(),
			),
		)

	def filter_by_constraints(self, tasks: list[Task], owner: Owner) -> list[Task]:
		"""Select tasks that fit within the owner's daily time budget."""
		selected: list[Task] = []
		minutes_used = 0

		required = [task for task in tasks if task.is_required]
		optional = [task for task in tasks if not task.is_required]

		for task in required:
			selected.append(task)
			minutes_used += task.duration_minutes

		for task in optional:
			if minutes_used + task.duration_minutes <= owner.daily_available_minutes:
				selected.append(task)
				minutes_used += task.duration_minutes

		return selected

	def apply_time_windows(self, tasks: list[Task]) -> list[Task]:
		"""Order tasks to prefer explicit time-window tasks first."""
		return self.sort_by_time(tasks)

	def sort_by_time(self, tasks: list[Task]) -> list[Task]:
		"""Sort tasks by earliest preferred time, placing untimed tasks last."""
		with_windows = [task for task in tasks if task.preferred_time_window is not None]
		without_windows = [task for task in tasks if task.preferred_time_window is None]

		with_windows.sort(
			key=lambda task: (
				task.preferred_time_window.earliest,
				-task.estimate_score(),
				task.duration_minutes,
				task.title.lower(),
			)
		)

		return with_windows + without_windows

	def order_tasks(self, tasks: list[Task]) -> list[ScheduleItem]:
		"""Assign start and end times to tasks in sequence."""
		items: list[ScheduleItem] = []
		current = time(8, 0)

		for task in tasks:
			start = current
			reasons: list[ReasonCode] = []

			if task.is_required:
				reasons.append(ReasonCode.REQUIRED_TASK)
			if task.priority == Priority.HIGH:
				reasons.append(ReasonCode.HIGH_PRIORITY)

			if task.preferred_time_window is not None:
				if start < task.preferred_time_window.earliest:
					start = task.preferred_time_window.earliest
				reasons.append(ReasonCode.TIME_WINDOW_RESPECTED)

			end = _add_minutes(start, task.duration_minutes)
			if task.preferred_time_window is not None and end > task.preferred_time_window.latest:
				continue

			reasons.append(ReasonCode.FIT_AVAILABLE_TIME)
			item = ScheduleItem(
				task=task,
				start_time=start,
				end_time=end,
				reason_codes=reasons,
			)
			items.append(item)
			current = end

		return items

	def calculate_total_minutes(self, items: list[ScheduleItem]) -> int:
		"""Sum the duration of all scheduled items."""
		return sum(item.duration() for item in items)


class ExplanationService:
	def explain_item(self, item: ScheduleItem, context: dict[str, Any]) -> str:
		"""Generate one explanation sentence for a scheduled item."""
		_ = context
		reason_text = [self.reason_code_to_text(code) for code in item.reason_codes]
		reason_part = "; ".join(reason_text) if reason_text else "no specific reason provided"
		return (
			f"{item.task.title} from {item.start_time.strftime('%H:%M')} "
			f"to {item.end_time.strftime('%H:%M')}: {reason_part}."
		)

	def explain_plan(self, plan: DailyPlan, context: dict[str, Any]) -> list[str]:
		"""Generate explanation lines for all plan outcomes."""
		explanations = [self.explain_item(item, context) for item in plan.items]
		if plan.unscheduled_tasks:
			names = ", ".join(task.title for task in plan.unscheduled_tasks)
			explanations.append(f"Unscheduled due to constraints: {names}.")
		return explanations

	def reason_code_to_text(self, code: ReasonCode) -> str:
		"""Map a reason code to user-facing explanatory text."""
		mapping = {
			ReasonCode.REQUIRED_TASK: "task is required",
			ReasonCode.HIGH_PRIORITY: "task has high priority",
			ReasonCode.FIT_AVAILABLE_TIME: "task fits available time",
			ReasonCode.MATCHED_PREFERENCE: "task matches owner preference",
			ReasonCode.TIME_WINDOW_RESPECTED: "preferred time window was respected",
		}
		return mapping.get(code, "unknown reason")


def _time_to_minutes(value: time) -> int:
	"""Convert a time-of-day value to minutes from midnight."""
	return value.hour * 60 + value.minute


def _add_minutes(value: time, minutes: int) -> time:
	"""Return a time shifted forward by a number of minutes."""
	base = datetime.combine(datetime.today().date(), value)
	result = base + timedelta(minutes=minutes)
	return result.time()