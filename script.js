function findSchemes() {
    const age = document.getElementById("age").value;
    const income = document.getElementById("income").value;
    const category = document.getElementById("category").value;
    const community = document.getElementById("community").value;
    const state = document.getElementById("state").value;

    fetch("/find_schemes", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({age, income, category, community, state})
    })
    .then(res => res.json())
    .then(data => {
        let output = "";

        data.eligible_schemes.forEach(s => {
            output += `
                <div class="scheme">
                    <b>${s.name}</b><br>
                    ${s.description}<br>
                    <b>Eligibility Score:</b> ${s.eligibility_score}%<br>
                    <b>Documents:</b> ${s.documents.join(", ")}
                </div>
            `;
        });

        document.getElementById("results").innerHTML = output;
        document.getElementById("missed").innerText =
            "Estimated Missed Benefit: ₹" + data.missed_benefit;
    });
}

function checkFraud() {
    const message = document.getElementById("fraudText").value;

    fetch("/fraud_check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("fraudResult").innerText =
            data.fraud
            ? "⚠ HIGH RISK SCAM (Score: " + data.fraud_score + ")"
            : "✅ Message looks safe (Score: " + data.fraud_score + ")";
    });
}