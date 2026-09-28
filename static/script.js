let tasks = [];

function calculatePriority(deadlineStr, hours, difficulty) {
    let today = new Date();
    today.setHours(0, 0, 0, 0);

    let deadlineDate = new Date(deadlineStr);
    deadlineDate.setHours(0, 0, 0, 0);

    // Din ka difference
    let timeDiff = deadlineDate - today;
    let daysLeft = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

    let daysFactor = daysLeft <= 0 ? 0.5 : daysLeft;
    let score = (parseFloat(difficulty) * parseFloat(hours)) / daysFactor;

    if (score >= 3 || daysLeft <= 1) {
        return { label: "HIGH", colorClass: "priority-high", score: score };
    } else if (score >= 1.5) {
        return { label: "MEDIUM", colorClass: "priority-medium", score: score };
    } else {
        return { label: "LOW", colorClass: "priority-low", score: score };
    }
}

function addTask() {
    let subject = document.getElementById("subject").value.trim();
    let topic = document.getElementById("topic").value.trim();
    let deadline = document.getElementById("deadline").value;
    let hours = document.getElementById("hours").value;
    let difficulty = document.getElementById("difficulty").value;

    if (!subject || !topic || !deadline || !hours) {
        alert("Saare fields fill karein!");
        return;
    }

    let priorityInfo = calculatePriority(deadline, hours, difficulty);

    let task = {
        subject: subject,
        topic: topic,
        deadline: deadline,
        hours: hours,
        difficultyText: difficulty == 3 ? "Hard" : difficulty == 2 ? "Medium" : "Easy",
        priority: priorityInfo.label,
        colorClass: priorityInfo.colorClass,
        score: priorityInfo.score
    };

    tasks.push(task);

    // Highest score wala task sabse upar sort hoga
    tasks.sort((a, b) => b.score - a.score);

    displayTasks();

    // Inputs reset
    document.getElementById("subject").value = "";
    document.getElementById("topic").value = "";
    document.getElementById("deadline").value = "";
    document.getElementById("hours").value = "";
}

function displayTasks() {
    let taskList = document.getElementById("taskList");
    taskList.innerHTML = "";

    tasks.forEach(function(task, index) {
        taskList.innerHTML += `
            <div class="task ${task.colorClass}">
                <div class="task-header">
                    <h3>#${index + 1} ${task.subject}: ${task.topic}</h3>
                    <span class="badge ${task.colorClass}-badge">${task.priority}</span>
                </div>
                <p><strong>Deadline:</strong> ${task.deadline} | <strong>Study Time:</strong> ${task.hours} hrs | <strong>Difficulty:</strong> ${task.difficultyText}</p>
            </div>
        `;
    });
}