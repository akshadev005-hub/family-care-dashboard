function setHeader() {
    let now = new Date();

    let hour = now.getHours();
    let greet = "Good Evening 🌙";

    if (hour < 12) greet = "Good Morning ☀️";
    else if (hour < 17) greet = "Good Afternoon 🌤️";

    document.getElementById("greet").innerText = greet;
    document.getElementById("date").innerText = now.toDateString();
}

setHeader();

async function addReminder() {
    let data = {
        person: document.getElementById("person").value,
        task: document.getElementById("task").value,
        time: document.getElementById("time").value
    };

    await fetch("/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    loadReminders();
}

async function loadReminders() {
    let res = await fetch("/get");
    let data = await res.json();

    let dadHTML = "";
    let momHTML = "";

    let dadCount = 0;
    let momCount = 0;

    data.forEach(r => {
        let card = `
        <div class="reminder">
            💊 ${r.task} | ⏰ ${r.time}
            <button onclick="deleteReminder(${r.id})">🗑️</button>
        </div>`;

        if (r.person === "Dad") {
            dadHTML += card;
            dadCount++;
        } else {
            momHTML += card;
            momCount++;
        }
    });

    document.getElementById("dad-list").innerHTML = dadHTML;
    document.getElementById("mom-list").innerHTML = momHTML;

    document.getElementById("total").innerText = data.length;
    document.getElementById("dadCount").innerText = dadCount;
    document.getElementById("momCount").innerText = momCount;
}

async function deleteReminder(id) {
    await fetch("/delete/" + id, { method: "DELETE" });
    loadReminders();
}

loadReminders();