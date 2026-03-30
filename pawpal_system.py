from __future__ import annotations

from dataclasses import dataclass, field
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


@dataclass
class TimeWindow:
	earliest: str
	latest: str


@dataclass
class Owner:
	name: str
	daily_available_minutes: int
	preferences: dict[str, str] = field(default_factory=dict)

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
	start_time: str
	end_time: str
	reason_codes: list[str] = field(default_factory=list)

	def duration(self) -> int:
		pass


@dataclass
class DailyPlan:
	date: str
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

	def order_tasks(self, tasks: list[Task]) -> list[ScheduleItem]:
		pass

	def calculate_total_minutes(self, items: list[ScheduleItem]) -> int:
		pass


class ExplanationService:
	def explain_item(self, item: ScheduleItem, context: dict[str, Any]) -> str:
		pass

	def explain_plan(self, plan: DailyPlan, context: dict[str, Any]) -> list[str]:
		pass

	def reason_code_to_text(self, code: str) -> str:
		pass