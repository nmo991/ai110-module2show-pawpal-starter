from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
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
		pass

	def get_preference(self, key: str) -> str | None:
		pass


@dataclass
class Pet:
	name: str
	species: str
	age: int | None = None
	notes: str | None = None

	def update_profile(
		self,
		*,
		name: str | None = None,
		species: str | None = None,
		age: int | None = None,
		notes: str | None = None,
	) -> None:
		pass


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

	def validate(self) -> None:
		pass

	def estimate_score(self) -> float:
		pass


@dataclass
class ScheduleItem:
	task: Task
	start_time: time
	end_time: time
	reason_codes: list[ReasonCode] = field(default_factory=list)

	def duration(self) -> int:
		pass


@dataclass
class DailyPlan:
	date: str
	owner_name: str
	pet_name: str
	items: list[ScheduleItem] = field(default_factory=list)
	unscheduled_tasks: list[Task] = field(default_factory=list)
	total_minutes: int = 0

	def add_item(self, item: ScheduleItem) -> None:
		pass

	def add_unscheduled(self, task: Task) -> None:
		pass

	def summary(self) -> str:
		pass


@dataclass
class TaskManager:
	tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def edit_task(self, task_id: str, updates: dict[str, Any]) -> None:
		pass

	def remove_task(self, task_id: str) -> None:
		pass

	def list_tasks(self) -> list[Task]:
		pass

	def list_tasks_for_pet(self, pet_name: str) -> list[Task]:
		pass

	def get_required_tasks(self) -> list[Task]:
		pass

	def validate_tasks(self) -> None:
		pass


class Scheduler:
	def generate_daily_plan(
		self, owner: Owner, pet: Pet, tasks: list[Task], date: str
	) -> DailyPlan:
		pass

	def rank_tasks(self, tasks: list[Task], owner: Owner, pet: Pet) -> list[Task]:
		pass

	def filter_by_constraints(self, tasks: list[Task], owner: Owner) -> list[Task]:
		pass

	def apply_time_windows(self, tasks: list[Task]) -> list[Task]:
		pass

	def order_tasks(self, tasks: list[Task]) -> list[ScheduleItem]:
		pass

	def calculate_total_minutes(self, items: list[ScheduleItem]) -> int:
		pass


class ExplanationService:
	def explain_item(self, item: ScheduleItem, context: dict[str, Any]) -> str:
		pass

	def explain_plan(self, plan: DailyPlan, context: dict[str, Any]) -> list[str]:
		pass

	def reason_code_to_text(self, code: ReasonCode) -> str:
		pass