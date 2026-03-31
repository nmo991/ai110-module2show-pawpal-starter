from datetime import date, time

from pawpal_system import (
    DailyPlan,
    Owner,
    Pet,
    Priority,
    ReasonCode,
    ScheduleItem,
    Task,
    TaskType,
    TimeWindow,
)


def build_demo_schedule() -> tuple[Owner, list[Pet], list[DailyPlan]]:
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

    mochi_items = [
        ScheduleItem(
            task=tasks[0],
            start_time=time(7, 30),
            end_time=time(8, 0),
            reason_codes=[ReasonCode.REQUIRED_TASK, ReasonCode.HIGH_PRIORITY],
        ),
        ScheduleItem(
            task=tasks[1],
            start_time=time(8, 10),
            end_time=time(8, 25),
            reason_codes=[ReasonCode.REQUIRED_TASK, ReasonCode.TIME_WINDOW_RESPECTED],
        ),
    ]

    luna_items = [
        ScheduleItem(
            task=tasks[2],
            start_time=time(18, 30),
            end_time=time(18, 50),
            reason_codes=[ReasonCode.FIT_AVAILABLE_TIME, ReasonCode.MATCHED_PREFERENCE],
        )
    ]

    plans = [
        DailyPlan(
            date=str(date.today()),
            owner_name=owner.name,
            pet_name="Mochi",
            items=mochi_items,
            total_minutes=45,
        ),
        DailyPlan(
            date=str(date.today()),
            owner_name=owner.name,
            pet_name="Luna",
            items=luna_items,
            total_minutes=20,
        ),
    ]

    return owner, pets, plans


def print_schedule(owner: Owner, pets: list[Pet], plans: list[DailyPlan]) -> None:
    print("Today's Schedule")
    print("=" * 40)
    print(f"Owner: {owner.name}")
    print(f"Available minutes: {owner.daily_available_minutes}")
    print(f"Pets: {', '.join(pet.name for pet in pets)}")
    print()

    for plan in plans:
        print(f"{plan.pet_name} ({plan.date})")
        for item in plan.items:
            start = item.start_time.strftime("%H:%M")
            end = item.end_time.strftime("%H:%M")
            print(f"  {start}-{end} | {item.task.title} [{item.task.task_type.value}]")
        print(f"  Total planned minutes: {plan.total_minutes}")
        print()


if __name__ == "__main__":
    demo_owner, demo_pets, demo_plans = build_demo_schedule()
    print_schedule(demo_owner, demo_pets, demo_plans)
