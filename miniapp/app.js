async function search() {
    const city = document.getElementById("city").value;

    const res = await fetch("http://localhost:8000/task", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({
            type: "rent.search",
            payload: { city, budget: 1000 }
        })
    });

    const data = await res.json();
    const taskId = data.task_id;

    let result;

    for (let i = 0; i < 10; i++) {
        await new Promise(r => setTimeout(r, 1000));

        const r = await fetch(`http://localhost:8000/task/${taskId}`);
        const j = await r.json();

        if (j.status === "done") {
            result = j.result.results;
            break;
        }
    }

    document.getElementById("out").innerText =
        JSON.stringify(result, null, 2);
}
