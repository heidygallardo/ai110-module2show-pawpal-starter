# PawPal+ Project Reflection

## 1. System Design

A user should be able to:
1. add a pet
2. add a task 
3. edit a task 

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

classes included:
1. Owner
    - Stores owner information (name, phone number, availability, preferences)
    - Manages pets (add, edit, remove, view)
    - Can view all pets and all tasks across pets

2. Pet 
    - Stores pet info (name, species, age, medical conditions, preferences)
    - manages tasks for that pet (add, edit, remove, view tasks)

3. Task
    - Respresents a single pet care activity
    - stores task details (name, duration, time, priority, category, completion status)
    - allow updating task details or marking the task complete

4. Scheduler
    - Generates the daily care plan
    - Organizes tasks based on priority and available time
    - Filters tasks to fit constraints
    - Produces the schedule and explanation of the plan


**b. Design changes**

- Updated the Scheduler class, since the AI-generate UML diagram had added another class. 
- Updated data type for 'availability' to integer.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers time, priority, and any conflicts there might be.

**b. Tradeoffs**

- One tradeoff my scheduler makes is that when detecting conflicts it only detects when times match, rather than when there is an overlap in times. 
- This tradeoff is reasonable scenarios where multiple pets are tasked for the same thing such as different pets being fed at the same time. 

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to help brainstorm ideas as to what features the app should have.
- I also used AI to help draft tests, once I received the draft I would review and trace through the logic to ensure the test was valid.
- I found Claude's plan mode to be very helpful when brainstorming, as well as its "Ask before edits" mode this way I was able to review its plan and edits before accepting changes.
- I also found it helpful to start a separate chat with Claude when working on a different section of the app.

**b. Judgment and verification**

- One moment where I did not accept an AI suggestion as-is was when designing the UML diagram, since it was trying to add another class that was not needed.
- I verified this by looking at the mermaid.js code the AI had given me.

---

## 4. Testing and Verification

**a. What you tested**

- Adding a task to a pet increases the pet's task count.
- New tasks start with an incomplete status.
- Marking a task as complete udpates its completion status.
- Tasks can be sorted into chronological order by time.
- Sorting tasks does not modify the original task list.
- Completing a daily recurring task creates a new task for the next day.
- Recurring tasks are created with an incomplete status.
- Scheduler detects conflicts when multiple tasks share the same time slot.
- Scheduler does not report conflicts for tasks with unique time slots.

**b. Confidence**

- I am confident that the scheduler works for the main expected behaviors.
- If I had more time I would test edge cases such as:

    - an empty task list
    - one task only
    - invalid or missing times
    -  availability limits when total task duration is too long

---

## 5. Reflection

**a. What went well**

- The part I am most satisfied about this project is the filtering logic to be able to sort by pet, as well as my final UML diagram reflecting the structure of my app.

**b. What you would improve**

- I would add more tests to improve the reliability of my app, as well as updating my UI so that it is more user-friendly. 

**c. Key takeaway**

- One important thing I learned about designing systems is to be specific on what classes the system should include as well as their attributes and methods. This way AI does not add any extra classes. 
