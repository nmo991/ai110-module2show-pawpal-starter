from datetime import date, time

from pawpal_system import (
    ExplanationService,
    Owner,
    Pet,
    Priority,
    Scheduler,
    Task,
    TaskManager,
    TaskType,
    TimeWindow,
)


def build_demo_schedule() -> tuple[Owner, list[Pet], list[Task], list]:
    owner = Owner(
        name="Jordan",
        daily_available_minutes=180,
        preferences={"walk_time": "morning", "feeding_style": "twice_daily"},
    )

    pets = [
        Pet(name="Mochi", species="dog", age=3),
        Pet(name="Luna", species="cat", age=5),
    ]

    tasks = [
        Task(
            id="t1",
            pet_name="Mochi",
            title="Morning Walk",
            task_type=TaskType.WALK,
            duration_minutes=30,
            priority=Priority.HIGH,
            is_required=True,
            preferred_time_window=TimeWindow(earliest=time(7, 0), latest=time(9, 0)),
        ),
        Task(
            id="t2",
            pet_name="Mochi",
            title="Breakfast",
            task_type=TaskType.FEED,
            duration_minutes=15,
            priority=Priority.HIGH,
            is_required=True,
            preferred_time_window=TimeWindow(earliest=time(8, 0), latest=time(9, 30)),
        ),
        Task(
            id="t3",
            pet_name="Luna",
            title="Evening Grooming",
            task_type=TaskType.GROOM,
            duration_minutes=20,
            priority=Priority.MEDIUM,
            preferred_time_window=TimeWindow(earliest=time(18, 0), latest=time(20, 0)),
        ),
    ]

    return owner, pets, tasks


def print_schedule(owner: Owner, pets: list[Pet], tasks: list[Task]) -> None:
    task_manager = TaskManager()
    scheduler = Scheduler()
    explainer = ExplanationService()

    for task in tasks:
        task_manager.add_task(task)

    task_manager.validate_tasks()

    print("Today's Schedule")
    print("=" * 40)
    print(f"Owner: {owner.name}")
    print(f"Available minutes: {owner.daily_available_minutes}")
    print(f"Pets: {', '.join(pet.name for pet in pets)}")
    print()

    for pet in pets:
        pet_tasks = task_manager.list_tasks_for_pet(pet.name)
        plan = scheduler.generate_daily_plan(
            owner=owner,
            pet=pet,
            tasks=pet_tasks,
            date=str(date.today()),
        )

        print(f"{plan.pet_name} ({plan.date})")
        for item in plan.items:
            start = item.start_time.strftime("%H:%M")
            end = item.end_time.strftime("%H:%M")
            print(f"  {start}-{end} | {item.task.title} [{item.task.task_type.value}]")

        explanations = explainer.explain_plan(plan, context={"owner": owner.name, "pet": pet.name})
        for line in explanations:
            print(f"    Why: {line}")

        print(f"  Total planned minutes: {plan.total_minutes}")
        print()


if __name__ == "__main__":
    demo_owner, demo_pets, demo_tasks = build_demo_schedule()
    print_schedule(demo_owner, demo_pets, demo_tasks)
