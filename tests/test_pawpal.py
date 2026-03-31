from datetime import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Priority, Task, TaskStatus, TaskType, TimeWindow


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
