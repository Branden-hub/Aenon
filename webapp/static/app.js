const capabilityList = document.getElementById("capability-list");
const reportContainer = document.getElementById("report");
const memoryContainer = document.getElementById("memory");
const form = document.getElementById("goal-form");
const feedbackBox = document.getElementById("feedback");
const feedbackStatus = document.getElementById("feedback-status");
const feedbackButton = document.getElementById("feedback-button");

async function fetchJSON(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || response.statusText);
  }
  return response.json();
}

function parseList(text) {
  return text
    .split(/\n|,/)
    .map((value) => value.trim())
    .filter(Boolean);
}

function parseMetrics(text) {
  const metrics = {};
  parseList(text).forEach((line) => {
    const [key, value] = line.split(/[:=]/).map((part) => part.trim());
    if (key) {
      metrics[key] = value || true;
    }
  });
  return metrics;
}

function renderCapabilities(capabilities) {
  capabilityList.innerHTML = "";
  Object.entries(capabilities).forEach(([name, description]) => {
    const item = document.createElement("li");
    item.innerHTML = `<strong>${name}</strong><br /><span>${description}</span>`;
    capabilityList.appendChild(item);
  });
}

function renderReport(report) {
  const lines = [`Goal summary: ${report.summary}`];
  report.responses.forEach((response) => {
    lines.push("\n" + `Capability: ${response.capability}`);
    lines.push(`Summary: ${response.summary}`);
    if (response.data?.pipeline) {
      lines.push("Pipeline:");
      response.data.pipeline.forEach((step, index) => {
        lines.push(`  ${index + 1}. ${step.step} – ${step.description}`);
      });
    }
    if (response.data?.proposal) {
      lines.push("Extension proposal:");
      response.data.proposal.forEach((step, index) => {
        lines.push(`  ${index + 1}. ${step.step} – ${step.detail}`);
      });
    }
    if (response.data?.plan) {
      lines.push("Collaboration plan:");
      response.data.plan.forEach((step, index) => {
        lines.push(`  ${index + 1}. ${step.step} – ${step.detail}`);
      });
    }
    if (response.insights?.length) {
      lines.push("Insights:");
      response.insights.forEach((insight) => {
        lines.push(`  - ${insight}`);
      });
    }
  });
  reportContainer.textContent = lines.join("\n");
}

function renderMemory(entries) {
  memoryContainer.innerHTML = "";
  entries.forEach((entry) => {
    const wrapper = document.createElement("div");
    wrapper.className = "memory-entry";
    const content = document.createElement("pre");
    content.textContent = JSON.stringify(entry, null, 2);
    wrapper.appendChild(content);
    memoryContainer.appendChild(wrapper);
  });
}

async function loadInitialData() {
  const { capabilities } = await fetchJSON("/api/capabilities");
  renderCapabilities(capabilities);
  const { entries } = await fetchJSON("/api/memory");
  renderMemory(entries);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  reportContainer.textContent = "Executing goal...";

  const payload = {
    domain: document.getElementById("domain").value.trim(),
    description: document.getElementById("description").value.trim(),
    constraints: parseList(document.getElementById("constraints").value),
    success_metrics: parseMetrics(document.getElementById("metrics").value),
    metadata: {},
  };

  const related = parseList(document.getElementById("related").value);
  if (related.length) {
    payload.metadata.related_domains = related;
  }

  try {
    const report = await fetchJSON("/api/goals", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    renderReport(report);
    const { entries } = await fetchJSON("/api/memory");
    renderMemory(entries);
  } catch (error) {
    reportContainer.textContent = `Failed to execute goal: ${error.message}`;
  }
});

feedbackButton.addEventListener("click", async () => {
  const message = feedbackBox.value.trim();
  if (!message) {
    feedbackStatus.textContent = "Please enter feedback before submitting.";
    return;
  }

  try {
    await fetchJSON("/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    feedbackStatus.textContent = "Thank you! Feedback recorded.";
    feedbackBox.value = "";
  } catch (error) {
    feedbackStatus.textContent = `Unable to save feedback: ${error.message}`;
  }
});

loadInitialData().catch((error) => {
  reportContainer.textContent = `Unable to load initial data: ${error.message}`;
});
