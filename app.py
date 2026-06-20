import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Pink theme -------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(160deg, #fff0f6 0%, #ffe3ef 100%);
    }
    h1, h2, h3, h4 { color: #c2185b !important; }
    /* Primary buttons */
    .stButton > button {
        background-color: #ec407a;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #d81b60;
        color: white;
    }
    /* Tables */
    table { border-radius: 8px; overflow: hidden; }
    thead tr th { background-color: #f8bbd0 !important; color: #880e4f !important; }
    tbody tr:nth-child(even) { background-color: #fff5f9 !important; }
    /* Inputs and dividers */
    hr { border-color: #f48fb1 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        border-color: #f48fb1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    st.write("### Current tasks")

    # A scheduler instance lets us reuse the backend's sort/filter/conflict logic
    # purely for display (no plan is generated here).
    pet_by_task = {id(t): p.name for p in owner.pets for t in p.tasks}
    view = Scheduler(
        tasks=all_tasks,
        availability=owner.availability,
        preferences=owner.preferences,
        pet_by_task=pet_by_task,
    )

    fcol, scol = st.columns(2)
    with fcol:
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + [p.name for p in owner.pets]
        )
    with scol:
        sort_by = st.selectbox("Sort by", ["priority", "time of day"])

    # Apply the chosen pet filter, then the chosen ordering.
    shown = (
        view.tasks
        if pet_filter == "All pets"
        else view.filter_by_pet(view.tasks, pet_filter)
    )
    shown = (
        view.organize_by_priority(shown)
        if sort_by == "priority"
        else view.sort_by_time(shown)
    )

    if shown:
        st.table(
            [
                {
                    "pet": pet_by_task.get(id(t), "?"),
                    "task": t.name,
                    "duration (min)": t.duration,
                    "time": t.time,
                    "priority": PRIORITY_LABELS.get(t.priority, t.priority),
                    "category": t.category,
                    "done": "✅" if t.is_complete else "",
                }
                for t in shown
            ]
        )
        st.caption(
            f"Showing {len(shown)} of {len(all_tasks)} task(s)"
            + ("" if pet_filter == "All pets" else f" for {pet_filter}")
        )
    else:
        st.info(f"No tasks for {pet_filter} yet.")

    # Surface scheduling conflicts (same time slot) before a plan is even built.
    conflicts = view.detect_conflicts(shown)
    if conflicts:
        st.warning("Possible scheduling conflicts:\n\n" + "\n\n".join(conflicts))
    else:
        st.success("No time-slot conflicts in the current view.")
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
        plan = scheduler.generate_plan()

        if not plan:
            st.warning("No tasks could be scheduled within the available time.")
        else:
            used = sum(t.duration for t in plan)
            st.success(
                f"Scheduled {len(plan)} task(s) using {used} of "
                f"{owner.availability} available minutes."
            )

            # Order the plan by time of day so the table reads like a daily agenda.
            time_order = ["morning", "afternoon", "evening", "night"]
            ordered = sorted(
                plan,
                key=lambda t: (
                    time_order.index(t.time)
                    if t.time in time_order
                    else len(time_order),
                    t.priority,
                ),
            )
            st.table(
                [
                    {
                        "time": t.time,
                        "pet": pet_by_task.get(id(t), "?"),
                        "task": t.name,
                        "duration (min)": t.duration,
                        "priority": PRIORITY_LABELS.get(t.priority, t.priority),
                        "category": t.category,
                    }
                    for t in ordered
                ]
            )

            # Tasks that didn't make the cut, so the demo shows what was trimmed.
            scheduled_ids = {id(t) for t in plan}
            skipped = [t for t in tasks if id(t) not in scheduled_ids]
            if skipped:
                st.warning(
                    "Left out (over time budget or already complete): "
                    + ", ".join(t.name for t in skipped)
                )

            # Flag any same-time-slot conflicts within the final plan.
            conflicts = scheduler.detect_conflicts(plan)
            if conflicts:
                st.warning(
                    "Conflicts in the plan:\n\n" + "\n\n".join(conflicts)
                )
