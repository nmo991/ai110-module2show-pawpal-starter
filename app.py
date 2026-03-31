import streamlit as st
from datetime import date

from pawpal_system import (
    ExplanationService,
    Owner,
    Pet,
    Priority,
    Scheduler,
    Task,
    TaskManager,
    TaskType,
)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", daily_available_minutes=180)
if "pet" not in st.session_state:
    st.session_state.pet = Pet(name="Mochi", species="dog")
if "task_manager" not in st.session_state:
    st.session_state.task_manager = TaskManager()
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "explainer" not in st.session_state:
    st.session_state.explainer = ExplanationService()
if "task_counter" not in st.session_state:
    st.session_state.task_counter = 1

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pet")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
available_minutes = st.number_input(
    "Available minutes today",
    min_value=1,
    max_value=1440,
    value=st.session_state.owner.daily_available_minutes,
)

species_options = ["dog", "cat", "other"]
pet_name = st.text_input("Pet name", value=st.session_state.pet.name)
current_species = (
    st.session_state.pet.species
    if st.session_state.pet.species in species_options
    else "other"
)
species = st.selectbox("Species", species_options, index=species_options.index(current_species))

st.session_state.owner.name = owner_name
st.session_state.owner.daily_available_minutes = int(available_minutes)
st.session_state.pet.update_profile(name=pet_name, species=species)

st.markdown("### Tasks")
st.caption("Add tasks for the selected pet.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    priority_map = {
        "low": Priority.LOW,
        "medium": Priority.MEDIUM,
        "high": Priority.HIGH,
    }
    task = Task(
        id=f"task-{st.session_state.task_counter}",
        pet_name=st.session_state.pet.name,
        title=task_title,
        task_type=TaskType.OTHER,
        duration_minutes=int(duration),
        priority=priority_map[priority],
    )
    try:
        st.session_state.task_manager.add_task(task)
        st.session_state.pet.add_task(task)
        st.session_state.task_counter += 1
        st.success("Task added to the current pet.")
    except (ValueError, KeyError) as exc:
        st.error(f"Could not add task: {exc}")

pet_tasks = st.session_state.task_manager.list_tasks_for_pet(st.session_state.pet.name)
if pet_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "id": task.id,
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority.value,
            }
            for task in pet_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a schedule using your TaskManager, Scheduler, and ExplanationService.")

if st.button("Generate schedule"):
    try:
        tasks_for_pet = st.session_state.task_manager.list_tasks_for_pet(st.session_state.pet.name)
        if not tasks_for_pet:
            st.info("Add at least one task before generating a schedule.")
        else:
            plan = st.session_state.scheduler.generate_daily_plan(
                owner=st.session_state.owner,
                pet=st.session_state.pet,
                tasks=tasks_for_pet,
                date=str(date.today()),
            )

            st.success("Schedule generated.")
            st.markdown(f"### Today's Plan for {plan.pet_name}")

            if plan.items:
                st.table(
                    [
                        {
                            "start": item.start_time.strftime("%H:%M"),
                            "end": item.end_time.strftime("%H:%M"),
                            "task": item.task.title,
                            "priority": item.task.priority.value,
                        }
                        for item in plan.items
                    ]
                )
            else:
                st.warning("No tasks could be scheduled with current constraints.")

            explanations = st.session_state.explainer.explain_plan(
                plan,
                context={"owner": st.session_state.owner.name, "pet": st.session_state.pet.name},
            )
            st.markdown("### Why this plan")
            for line in explanations:
                st.write(f"- {line}")

            st.caption(f"Total planned minutes: {plan.total_minutes}")
    except (ValueError, KeyError) as exc:
        st.error(f"Could not generate schedule: {exc}")
