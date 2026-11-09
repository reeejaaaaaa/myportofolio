(() => {
    const form = document.getElementById("experience-edit-form");
    if (!form) return;

    form.addEventListener("submit", async event => {
        event.preventDefault();
        const button = form.querySelector('button[type="submit"]');
        if (button.disabled) return;
        button.disabled = true;
        form.setAttribute("aria-busy", "true");
        try {
            const experience = await writeExperience(
                form.dataset.detailUrl, "PATCH", experiencePayload(form)
            );
            // Show the sanitized values returned by the serializer without reloading.
            form.elements.namedItem("title").value = experience.title;
            form.elements.namedItem("description").value = experience.description;
            showToast("Berhasil", "Experience berhasil diperbarui.", "success");
        } catch (error) {
            showToast("Gagal memperbarui experience", error.message, "error");
        } finally {
            button.disabled = false;
            form.removeAttribute("aria-busy");
        }
    });
})();
