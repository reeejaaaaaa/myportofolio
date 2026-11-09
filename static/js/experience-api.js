// Shared form contract for Experience create and edit requests.
function experiencePayload(form) {
    const fields = new FormData(form);
    return {
        title: fields.get("title"),
        description: fields.get("description"),
        category: fields.get("category"),
        thumbnail: fields.get("thumbnail") || "",
        started_at: fields.get("started_at"),
        ended_at: fields.get("ended_at") || null,
        education: fields.get("education") || null,
        projects: fields.getAll("projects")
    };
}

function experienceErrorMessage(data, status) {
    const messages = [];
    function collect(value, field = "") {
        if (typeof value === "string") {
            messages.push(field ? `${field}: ${value}` : value);
        } else if (Array.isArray(value)) {
            value.forEach(item => collect(item, field));
        } else if (value && typeof value === "object") {
            Object.entries(value).forEach(([key, item]) => {
                collect(item, ["detail", "non_field_errors"].includes(key) ? "" : key);
            });
        }
    }
    collect(data);
    return messages.join(" ") || `Request gagal (HTTP ${status}).`;
}

async function writeExperience(url, method, payload) {
    const response = await fetch(url, {
        method,
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: payload === undefined ? undefined : JSON.stringify(payload)
    });
    const data = response.status === 204
        ? null
        : await response.json().catch(() => ({}));
    if (!response.ok) {
        throw new Error(experienceErrorMessage(data, response.status));
    }
    return data;
}
