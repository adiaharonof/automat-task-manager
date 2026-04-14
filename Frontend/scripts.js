//variable that keeps the current filter the user is using
let currentFilter = "All";

// Function for the create task botton, when you click on the botton the forms the user needs to fill out are shown / hidden
function togglePopup() {
    const popup = document.getElementById("pop-up");
    popup.style.display = (popup.style.display === "none" || popup.style.display === "") ? "block" : "none";
}
// when the user clicks the create task botton this calls the togglePopUp function
document.getElementById("create-task-button").onclick = togglePopup;

// Sets that when the page firstly open the "All" filter will be on - the default setting, by calling the fetchTasks function.
window.onload = () => fetchTasks("All");

// Fetch the tasks according to the current used filter
function fetchTasks(filter = currentFilter) {
    currentFilter = filter; // Save the selected filter globally
    let url = "http://localhost:8000/tasks";
    // Mapping filter names to your Backend endpoints
    if (filter === "Completed") url += "/completed";
    else if (filter === "In Progress") url += "/uncompleted";
    else if (filter === "Overdue") url += "/overdue";

    fetch(url)
    .then(response => response.json())
    .then(tasks => {
        displayTasks(tasks); // displaying the tasks
        updateFilterButtonsUI(); // Highlight the active filter button
    })
    .catch(error => console.error("Error fetching tasks:", error));
}

// displays the tasks list into the UI
function displayTasks(tasks) {
    const list = document.getElementById("tasks-list");
    list.innerHTML = ""; // deletes all the tasks from the list and only afterwards adds more

    tasks.forEach(task => {
        const li = document.createElement("li");
        const isCompleted = task.done;
        li.className = `task-item ${isCompleted ? 'completed' : ''}`;

        li.innerHTML = `
            <div class="task-info">
                <input type="checkbox" ${isCompleted ? "checked" : ""} 
                    onclick="toggleTaskStatus(${task.id}, ${isCompleted})">
                <div class="task-text" style="${isCompleted ? "text-decoration: line-through; opacity: 0.6;" : ""}">
                    <span class="task-title">${task.title}</span>
                    <span class="task-desc">${task.description || ""}</span>
                </div>
            </div>
            <div class="task-actions">
            <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
            <button onclick="editTask(${task.id}, '${task.title}', '${task.description}')">Edit</button>
    </div>
    `;
        list.appendChild(li);
    });
}

// Create a new task and stay on the current filter
function createTask() {
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const deadline = document.getElementById("deadline").value;
    const deadlineUTC = deadline ? new Date(deadline).toISOString() : null;
    if (!title) {
        alert("Please enter a title");
        return;
    }
    if (!description) {
    alert("Please enter a description");
    return;
    }
    fetch("http://localhost:8000/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            task_title: title,
            task_description: description,
            task_deadline: deadlineUTC || null
        })
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to create task");
        return response.json();
    })
    .then(() => {
        togglePopup();
        fetchTasks(currentFilter); // Refresh to show the new task while using the saved filter
        
        // Clear the inputs fild
        document.getElementById("title").value = "";
        document.getElementById("description").value = "";
        document.getElementById("deadline").value = "";
    })
    .catch(err => alert(err.message));
}
//when the user clicks on submit it calls create task
document.getElementById("submit-task").onclick = createTask;

// Delete task and then refresh the list with the current filter
function deleteTask(taskId) {
    if (!confirm("Are you sure?")) return;
    fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: "DELETE"
    })
    .then(() => fetchTasks(currentFilter))
    .catch(error => console.error("Error deleting:", error));
}

// changes the status of the task when the user clicks on the tasks checkbox
function toggleTaskStatus(taskId, currentStatus) {
    fetch(`http://localhost:8000/tasks/${taskId}?is_done=${!currentStatus}`, {
        method: "PATCH"
    })
    .then(() => fetchTasks(currentFilter))
    .catch(error => console.error("Error updating status:", error));
}

// makes the selected filter buttons darker so the user can tell what filter he uses
function updateFilterButtonsUI() {
    const filterButtons = document.querySelectorAll("#filters button");
    filterButtons.forEach(btn => {
        if (btn.innerText === currentFilter) {
            btn.style.backgroundColor = "#5BA8D4"; // Active (darker)
        } else {
            btn.style.backgroundColor = "#87CEEB"; // Default (lighter)
        }
    });
}

// every time the user clicks on a filter botton it calls the fetchTask function
const filterButtons = document.querySelectorAll("#filters button");
filterButtons.forEach(btn => {
    btn.onclick = () => fetchTasks(btn.innerText);
});

function editTask(taskId, currentTitle, currentDescription) {
    const newTitle = prompt("Edit title:", currentTitle);
    if (newTitle === null) return;

    const newDescription = prompt("Edit description:", currentDescription);
    if (newDescription === null) return;
    if (!newTitle.trim()) {
        alert("Title cannot be empty");
        return;
    }
    if (!newDescription.trim()) {
        alert("Description cannot be empty");
        return;
    }
    fetch(`http://localhost:8000/tasks/${taskId}/title?new_title=${newTitle}`, {
        method: "PATCH"
    })
    .then(() => fetch(`http://localhost:8000/tasks/${taskId}/description?new_description=${newDescription}`, {
        method: "PATCH"
    }))
    .then(() => fetchTasks(currentFilter))
    .catch(error => console.error("Error editing task:", error));
}
