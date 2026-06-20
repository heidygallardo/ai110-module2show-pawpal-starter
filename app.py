import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
availability = st.number_input(
    "Time available today (minutes)", min_value=0, max_value=1440, value=120
)

# Create the owner once, then keep it in sync with the inputs on later re-runs.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name, phone_number="", availability=int(availability)
    )
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.availability = int(availability)

owner = st.session_state.owner

st.divider()

# --- Adding a Pet -----------------------------------------------------------
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
age = st.number_input("Age (years)", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    try:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added pet '{pet_name}'.")
    except ValueError as e:
        st.warning(str(e))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": p.name, "species": p.species, "age": p.age, "tasks": len(p.tasks)}
            for p in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Adding / Scheduling a Task --------------------------------------------
st.subheader("Add a Task")
st.caption("Tasks belong to a pet and feed into the scheduler.")

# UI uses words; the Task class and Scheduler use ints (lower = higher priority).
PRIORITY_MAP = {"high": 1, "medium": 2, "low": 3}
PRIORITY_LABELS = {v: k for k, v in PRIORITY_MAP.items()}  # int -> word, for display

if not owner.pets:
    st.info("Add a pet first, then you can add tasks for it.")
else:
    task_pet_name = st.selectbox("For which pet?", [p.name for p in owner.pets])

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        time_of_day = st.selectbox(
            "Time of day", ["morning", "afternoon", "evening", "night"]
        )
    with col5:
        category = st.selectbox(
            "Category", ["exercise", "feeding", "grooming", "medical", "play", "other"]
        )

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == task_pet_name)
        try:
            pet.add_task(
                Task(
                    name=task_title,
                    duration=int(duration),
                    time=time_of_day,
                    priority=PRIORITY_MAP[priority],
                    category=category,
                )
            )
            st.success(f"Added task '{task_title}' for {pet.name}.")
        except ValueError as e:
            st.warning(str(e))

all_tasks = owner.view_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    pet_of = {id(t): p.name for p in owner.pets for t in p.tasks}
    st.table(
        [
            {
                "pet": pet_of.get(id(t), "?"),
                "task": t.name,
                "duration": t.duration,
                "time": t.time,
                "priority": PRIORITY_LABELS.get(t.priority, t.priority),
                "category": t.category,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet.")

st.divider()

# --- Build Schedule ---------------------------------------------------------
st.subheader("Build Schedule")
st.caption("Runs your Scheduler over every task across all pets.")

if st.button("Generate schedule"):
    tasks = owner.view_all_tasks()
    if not tasks:
        st.warning("No tasks to schedule. Add some tasks first.")
    else:
        # Tell the scheduler which pet each task belongs to (id(task) -> pet name).
        pet_by_task = {id(t): p.name for p in owner.pets for t in p.tasks}
        scheduler = Scheduler(
            tasks=tasks,
            availability=owner.availability,
            preferences=owner.preferences,
            pet_by_task=pet_by_task,
        )
        scheduler.generate_plan()
        st.text(scheduler.explanation)
