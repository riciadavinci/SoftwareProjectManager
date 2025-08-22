const swpr_id = null;  // optional filter
const user_id = null;  // optional filter

const queryParams = new URLSearchParams({
    swpr_id: swpr_id !== null ? swpr_id : "",
    user_id: user_id !== null ? user_id : ""
});

async function loadTasks() {
    try {
        const response = await fetch(`/api/task?${queryParams.toString()}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const tasks = result.data;

        tasks.forEach(task => {
            const card = document.createElement("div");
            card.id = `task-${task.id}`;
            card.className = "kanban-card card mb-2";
            card.innerHTML = `
                <div class="card-body p-2">
                    <h6 class="card-title">${task.title}</h6>
                    <p class="card-text small">${task.description || ""}</p>
                    <small class="text-muted">ID: ${task.id}</small>
                </div>
            `;

            const status = task.task_status_id || "todo";  // adjust field name as needed
            if (status === "todo") {
                document.getElementById("todo-column").appendChild(card);
            } else if (status === "wip") {
                document.getElementById("wip-column").appendChild(card);
            } else if (status === "done") {
                document.getElementById("done-column").appendChild(card);
            }
        });

        enableDragAndDrop(); // make cards draggable

    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

let placeholder = null;

// Drag & Drop
function enableDragAndDrop() {
    const cards = document.querySelectorAll(".kanban-card");
    const columns = document.querySelectorAll(".kanban-column");

    cards.forEach(card => {
        card.setAttribute("draggable", true);

        card.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", card.id);
            card.classList.add("dragging");

            // Make dragged element appear solid
            const clone = card.cloneNode(true);
            clone.style.position = "absolute";
            clone.style.top = "-9999px"; // move it off-screen
            document.body.appendChild(clone);
            e.dataTransfer.setDragImage(clone, 0, 0);

            setTimeout(() => document.body.removeChild(clone), 0); // remove immediately
        });

        card.addEventListener("dragend", () => {
            card.classList.remove("dragging");
            if (placeholder) {
                placeholder.remove()
            };
        });
    });

    columns.forEach(col => {
        col.addEventListener("dragover", (e) => {
            e.preventDefault();

            // Add placeholder if it doesn’t exist
            if (!placeholder) {
                placeholder = document.createElement("div");
                placeholder.className = "kanban-placeholder";
            }

            // Find the card after which to insert placeholder
            const afterElement = getDragAfterElement(col, e.clientY);
            if (afterElement) {
                col.insertBefore(placeholder, afterElement);
            } else {
                col.appendChild(placeholder);
            }

            // col.classList.add("drag-over");
        });

        col.addEventListener("dragleave", () => {
            // Optional: remove placeholder when leaving column
            if (placeholder && !col.contains(document.querySelector(".dragging"))) {
                placeholder.remove();
            }
            // col.classList.remove("drag-over");
        });

        col.addEventListener("drop", async (e) => {
            e.preventDefault();
            col.classList.remove("drag-over");

            const cardId = e.dataTransfer.getData("text/plain");
            const card = document.getElementById(cardId);

            // Insert card at placeholder position
            col.insertBefore(card, placeholder);
            placeholder.remove();
            placeholder = null;

            // col.appendChild(card);

            // Notify backend
            const newStatus = col.dataset.status;
            const card_id = cardId.split("-")[1];
            await updateTaskStatus(card_id, newStatus);
            resortColumn(col); 
        });
    });
}

async function updateTaskStatus(card_id, new_status) {
    try {
        const response = await fetch(`/api/task/${card_id}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ task_status_id: new_status })
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
    } catch (err) {
        console.error("Failed to update task status:", err);
    }
}


// Helper to get the element after which to insert the dragged card
function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll(".kanban-card:not(.dragging)")];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

function resortColumn(column) {
    // Example: sort by card title
    const cards = Array.from(column.querySelectorAll(".kanban-card"));
    cards.sort((a, b) => a.querySelector(".card-title").textContent.localeCompare(b.querySelector(".card-title").textContent));

    // Re-append in sorted order
    cards.forEach(card => column.appendChild(card));
}


// Initialize
loadTasks();