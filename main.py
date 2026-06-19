from pawpal_system import Pet, Owner, Task, Scheduler

# Create an Owner 
mary = Owner('Mary', '8882151', 120)

# Create two pets
whiskers = Pet('Whiskers', 'cat', 3)
rex = Pet('Rex', 'dog', 5)

mary.add_pet(whiskers)
mary.add_pet(rex)

# Add three Tasks with different times to those pets
whiskers.add_task(Task('Morning feeding', 10, 'morning', 1, 'feeding'))
rex.add_task(Task('Afternoon walk', 30, 'afternoon', 2, 'exercise'))
rex.add_task(Task('Evening feeding', 15, 'evening', 1, 'feeding'))

# Map each task back to the pet it belongs to (keyed by task identity).
pet_by_task = {id(task): pet.name for pet in mary.pets for task in pet.tasks}

# Print "Today's Schedule"
print(f"            Today's Schedule for {mary.name}        ")
print("=====================================================")
scheduler = Scheduler(
    mary.view_all_tasks(),
    mary.availability,
    mary.preferences,
    pet_by_task=pet_by_task,
)
scheduler.generate_plan()
print(scheduler.explanation)

