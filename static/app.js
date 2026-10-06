
const form = document.getElementById("predictionForm");
const button = document.getElementById("predictBtn");
const emptyState = document.getElementById("emptyState");
const resultContent = document.getElementById("resultContent");
const errorBox = document.getElementById("errorBox");
const probability = document.getElementById("probability");
const meterFill = document.getElementById("meterFill");
const riskBadge = document.getElementById("riskBadge");
const decisionIcon = document.getElementById("decisionIcon");
const decisionText = document.getElementById("decisionText");
const decisionMessage = document.getElementById("decisionMessage");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    errorBox.classList.add("hidden");
    button.disabled = true;
    button.querySelector("span:nth-child(2)").textContent = "Analyzing customer risk...";

    const data = {};
    new FormData(form).forEach((value, key) => data[key] = value);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (!response.ok || !result.success) {
            throw new Error(result.error || "Prediction failed.");
        }

        emptyState.classList.add("hidden");
        resultContent.classList.remove("hidden");

        probability.textContent = `${result.probability.toFixed(2)}%`;
        meterFill.style.width = `${Math.min(result.probability, 100)}%`;

        const highRisk = result.prediction === 1;
        riskBadge.textContent = highRisk ? "HIGH RISK" : "LOWER RISK";
        riskBadge.classList.toggle("high", highRisk);

        decisionIcon.textContent = highRisk ? "!" : "✓";
        decisionIcon.classList.toggle("high", highRisk);
        decisionText.textContent = result.status;
        decisionMessage.textContent = result.message;
    } catch (error) {
        errorBox.textContent = error.message;
        errorBox.classList.remove("hidden");
    } finally {
        button.disabled = false;
        button.querySelector("span:nth-child(2)").textContent = "Run AI Risk Analysis";
    }
});
