
const textInput = document.getElementById("textInput");
const detectBtn = document.getElementById("detectBtn");
const clearBtn = document.getElementById("clearBtn");
const result = document.getElementById("result");

detectBtn.addEventListener("click", async () => {
    const text = textInput.value.trim();

    if (!text) {
        result.textContent = "Please enter a sentence first.";
        result.className = "result error";
        return;
    }

    detectBtn.disabled = true;
    detectBtn.textContent = "Detecting...";
    result.textContent = "Analyzing text...";
    result.className = "result";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        result.replaceChildren();

        const heading = document.createElement("strong");
        heading.textContent =
            "Predicted language: " + data.predicted_language;

        const inputLine = document.createElement("p");
        inputLine.textContent = "Input: " + data.input_text;

        result.append(heading, inputLine);
        result.className = "result success";

    } catch (error) {
        result.textContent = error.message;
        result.className = "result error";
    } finally {
        detectBtn.disabled = false;
        detectBtn.textContent = "Detect Language";
    }
});

clearBtn.addEventListener("click", () => {
    textInput.value = "";
    result.textContent = "Your prediction will appear here.";
    result.className = "result";
    textInput.focus();
});
