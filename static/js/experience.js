(() => {
    const app =
        document.getElementById(
            "experience-app"
        );

    if (!app) {
        return;
    }

    const experiencesUrl =
        app.dataset.experiencesUrl;

    const detailPattern = app.dataset.detailPattern;
    const starPattern = app.dataset.starPattern;
    const editPattern = app.dataset.editPattern;

    function experienceEndpoint(pattern, id) {
        return pattern.replace("00000000-0000-0000-0000-000000000000", id);
    }

    function formatMonthYear(value) {
        const [year, month, day] = value.split("-").map(Number);
        return new Intl.DateTimeFormat("en", {
            month: "short", year: "numeric", timeZone: "UTC"
        }).format(new Date(Date.UTC(year, month - 1, day || 1)));
    }

    const projectsUrl =
        app.dataset.projectsUrl;

    const loginUrl =
        app.dataset.loginUrl;

    const isSuperuser =
        app.dataset.isSuperuser === "true";

    const isEditor =
        app.dataset.isEditor === "true";

    const isAuthenticated =
        app.dataset.isAuthenticated === "true";


    const loadingState =
        document.getElementById(
            "experience-loading"
        );

    const errorState =
        document.getElementById(
            "experience-error"
        );

    const emptyState =
        document.getElementById(
            "experience-empty"
        );

    const grid =
        document.getElementById(
            "experience-grid"
        );

    const searchForm =
        document.getElementById(
            "experience-search-form"
        );

    const searchInput =
        document.getElementById(
            "experience-search-input"
        );

    const categoryFilter =
        document.getElementById(
            "experience-category-filter"
        );

    const sortSelect =
        document.getElementById(
            "experience-sort"
        );
    const summaryTotal =
        document.getElementById(
            "summary-total"
        );

    const summaryOngoing =
        document.getElementById(
            "summary-ongoing"
        );

    const summaryProjects =
        document.getElementById(
            "summary-projects"
        );

    const summaryStars =
        document.getElementById(
            "summary-stars"
        );
    const experienceForm =
        document.getElementById(
            "experience-form"
        );


    const SEARCH_DEBOUNCE_DELAY = 300;

    let searchDebounceTimer;
    let experienceAbortController;
    let currentExperienceData = [];


    function displayState({
        loading = false,
        error = false,
        empty = false,
        showGrid = false
    }) {
        loadingState.classList.toggle(
            "hide",
            !loading
        );

        errorState.classList.toggle(
            "hide",
            !error
        );

        emptyState.classList.toggle(
            "hide",
            !empty
        );

        grid.classList.toggle(
            "hide",
            !showGrid
        );
    }


    function buildProjectLinks(projects) {
        if (!projects.length) {
            return `
                <span class="experience-related-empty">
                    Belum ada project terkait.
                </span>
            `;
        }

        return projects
            .map(project => `
                <a
                    href="${escapeHtml(projectsUrl)}"
                    class="experience-project-link"
                >
                    ${escapeHtml(project.title)}
                </a>
            `)
            .join("");
    }


    function buildExperienceCardElement(experience) {

        const article =
            document.createElement(
                "article"
            );

        article.className =
            "experience-card";


        const thumbnailHtml =
            experience.thumbnail
                ? `
                    <img
                        src="${escapeHtml(experience.thumbnail)}"
                        alt="${escapeHtml(experience.title)}"
                        class="experience-thumbnail"
                    >
                `
                : "";


        const educationHtml =
            experience.education_name
                ? `
                    <div class="experience-related">
                        <span class="experience-related-label">
                            Education
                        </span>

                        <span class="experience-related-value">
                            ${escapeHtml(experience.education_name)}
                        </span>
                    </div>
                `
                : "";


        const starTitle =
            experience.star_count > 0
                ? `Dibintangi oleh ${escapeHtml(
                    experience.starred_by_names
                )}`
                : "Jadilah yang pertama memberi star";


        let starHtml;

        if (isAuthenticated) {
            starHtml = `
                <button
                    type="button"
                    class="button button-star${experience.is_starred ? " is-starred" : ""}"
                    data-star-url="${escapeHtml(experienceEndpoint(starPattern, experience.id))}"
                    title="${starTitle}"
                >
                    <span aria-hidden="true">
                        ★
                    </span>

                    <span class="star-label">
                        ${experience.is_starred ? "Unstar" : "Star"}
                    </span>

                    <span class="star-count">
                        ${experience.star_count}
                    </span>
                </button>
            `;
        } else {
            starHtml = `
                <a
                    href="${escapeHtml(loginUrl)}"
                    class="button button-star"
                >
                    Login untuk Star
                </a>
            `;
        }


        const editHtml =
            isSuperuser || isEditor
                ? `
                    <a
                        href="${escapeHtml(experienceEndpoint(editPattern, experience.id))}"
                        class="button button-secondary"
                    >
                        Edit
                    </a>
                `
                : "";

        const deleteHtml =
            isSuperuser
                ? `
            <button
                type="button"
                class="button button-danger"
                data-delete-url="${escapeHtml(
                    experienceEndpoint(detailPattern, experience.id)
                )}"
                data-experience-title="${escapeHtml(
                    experience.title
                )}"
            >
                Delete
            </button>
        `
                : "";


        article.innerHTML = `
    ${thumbnailHtml}

    <span class="experience-category">
        ${escapeHtml(
            experience.category_display
        )}
    </span>

    <p class="experience-period">
        ${escapeHtml(
            formatMonthYear(experience.started_at)
        )}
        —
        ${experience.ended_at
                ? escapeHtml(
                    formatMonthYear(experience.ended_at)
                )
                : "Present"
            }
    </p>

    <h2>
        ${escapeHtml(
                experience.title
            )}
    </h2>

    <p class="experience-description">
        ${escapeHtml(
                experience.description
            )}
    </p>

    ${educationHtml}

    <div class="experience-related">

        <span class="experience-related-label">
            Related Projects
        </span>

        <div class="experience-project-list">
            ${buildProjectLinks(
                experience.project_details
            )}
        </div>

    </div>

    <p class="experience-status">
        ${experience.is_ongoing
                ? "Sedang berlangsung"
                : "Selesai"
            }
    </p>

    <div class="experience-actions">
        ${starHtml}
        ${editHtml}
        ${deleteHtml}
    </div>
`;


        return article;
    }




    function updateSummary(data) {
        const ongoingCount =
            data.filter(
                item =>
                    item.is_ongoing
            ).length;


        const uniqueProjectIds =
            new Set();


        let totalStars = 0;


        data.forEach(experience => {


            totalStars +=
                experience.star_count;


            experience.project_details.forEach(
                project => {
                    uniqueProjectIds.add(
                        project.id
                    );
                }
            );
        });


        summaryTotal.textContent =
            data.length;

        summaryOngoing.textContent =
            ongoingCount;

        summaryProjects.textContent =
            uniqueProjectIds.size;

        summaryStars.textContent =
            totalStars;
    }

    function renderExperiences() {
        const selectedCategory =
            categoryFilter.value;

        let filteredData =
            selectedCategory
                ? currentExperienceData.filter(
                    item =>
                        item.category ===
                        selectedCategory
                )
                : [...currentExperienceData];


        if (sortSelect.value === "oldest") {
            filteredData.reverse();
        }


        if (sortSelect.value === "stars") {
            filteredData.sort(
                (a, b) =>
                    b.star_count -
                    a.star_count
            );
        }


        if (sortSelect.value === "az") {
            filteredData.sort(
                (a, b) =>
                    a.title.localeCompare(
                        b.title
                    )
            );
        }

        updateSummary(
            filteredData
        );

        grid.innerHTML = "";


        if (filteredData.length === 0) {
            displayState({
                empty: true
            });

            return;
        }


        filteredData.forEach(
            item => {
                grid.appendChild(
                    buildExperienceCardElement(
                        item
                    )
                );
            }
        );


        displayState({
            showGrid: true
        });
    }


    async function fetchExperiences(
        searchQuery = ""
    ) {
        if (experienceAbortController) {
            experienceAbortController.abort();
        }

        experienceAbortController =
            new AbortController();


        try {
            displayState({
                loading: true
            });


            const url =
                new URL(
                    experiencesUrl,
                    window.location.origin
                );


            if (searchQuery) {
                url.searchParams.set(
                    "q",
                    searchQuery
                );
            }


            const response =
                await fetch(
                    url,
                    {
                        headers: {
                            "Accept":
                                "application/json"
                        },

                        signal:
                            experienceAbortController
                                .signal
                    }
                );


            if (!response.ok) {
                throw new Error(
                    "Gagal mengambil data experience."
                );
            }


            currentExperienceData =
                await response.json();


            renderExperiences();

        } catch (error) {
            if (
                error.name ===
                "AbortError"
            ) {
                return;
            }

            console.error(
                "Error loading experiences:",
                error
            );

            displayState({
                error: true
            });
        }
    }


    function searchExperiences() {
        fetchExperiences(
            searchInput.value.trim()
        );
    }


    searchInput.addEventListener(
        "input",
        () => {
            clearTimeout(
                searchDebounceTimer
            );

            searchDebounceTimer =
                setTimeout(
                    searchExperiences,
                    SEARCH_DEBOUNCE_DELAY
                );
        }
    );


    searchForm.addEventListener(
        "submit",
        event => {
            event.preventDefault();

            clearTimeout(
                searchDebounceTimer
            );

            searchExperiences();
        }
    );


    categoryFilter.addEventListener(
        "change",
        renderExperiences
    );




    sortSelect.addEventListener(
        "change",
        renderExperiences
    );

    grid.addEventListener(
        "click",
        async event => {
            const deleteButton =
                event.target.closest(
                    "[data-delete-url]"
                );

            if (deleteButton) {
                const experienceTitle =
                    deleteButton.dataset.experienceTitle;

                const confirmed =
                    window.confirm(
                        `Yakin ingin menghapus "${experienceTitle}"?`
                    );

                if (!confirmed) {
                    return;
                }

                deleteButton.disabled = true;

                try {
                    const response =
                        await fetch(
                            deleteButton.dataset.deleteUrl,
                            {
                                method: "DELETE",

                                headers: {
                                    "X-CSRFToken":
                                        getCookie(
                                            "csrftoken"
                                        ),

                                    "X-Requested-With":
                                        "XMLHttpRequest",

                                    "Accept":
                                        "application/json"
                                }
                            }
                        );

                    if (!response.ok) {
                        throw new Error(
                            `Gagal menghapus experience (${response.status}).`
                        );
                    }

                    showToast(
                        "Berhasil",
                        "Experience berhasil dihapus.",
                        "success"
                    );

                    fetchExperiences(
                        searchInput.value.trim()
                    );

                } catch (error) {
                    console.error(
                        "Error deleting experience:",
                        error
                    );

                    showToast(
                        "Gagal menghapus",
                        error.message,
                        "error"
                    );

                } finally {
                    deleteButton.disabled = false;
                }

                return;
            }
            const starButton =
                event.target.closest(
                    "[data-star-url]"
                );

            if (!starButton) {
                return;
            }


            starButton.disabled = true;


            try {
                const response =
                    await fetch(
                        starButton.dataset.starUrl,
                        {
                            method: "POST",

                            headers: {
                                "X-CSRFToken":
                                    getCookie(
                                        "csrftoken"
                                    ),

                                "X-Requested-With":
                                    "XMLHttpRequest",

                                "Accept":
                                    "application/json"
                            }
                        }
                    );


                if (!response.ok) {
                    throw new Error(
                        "Gagal memperbarui star."
                    );
                }


                const result =
                    await response.json();


                showToast(
                    "Berhasil",
                    result.is_starred
                        ? "Experience berhasil diberi star."
                        : "Star berhasil dihapus.",
                    "success"
                );


                fetchExperiences(
                    searchInput.value.trim()
                );

            } catch (error) {
                console.error(
                    "Error updating star:",
                    error
                );

                showToast(
                    "Gagal",
                    "Star tidak dapat diperbarui.",
                    "error"
                );

            } finally {
                starButton.disabled = false;
            }
        }
    );


    async function addExperience(event) {
        event.preventDefault();

        if (!experienceForm) {
            return;
        }


        const submitButton =
            experienceForm.querySelector(
                'button[type="submit"]'
            );

        submitButton.disabled = true;


        const fields = new FormData(experienceForm);
        const payload = {
            title: fields.get("title"),
            description: fields.get("description"),
            category: fields.get("category"),
            thumbnail: fields.get("thumbnail") || "",
            started_at: fields.get("started_at"),
            ended_at: fields.get("ended_at") || null,
            education: fields.get("education") || null,
            projects: fields.getAll("projects")
        };

        try {
            const response =
                await fetch(
                    experiencesUrl,
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken":
                                getCookie(
                                    "csrftoken"
                                ),

                            "Accept": "application/json",
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify(payload)
                    }
                );


            const result =
                await response
                    .json()
                    .catch(
                        () => ({})
                    );


            if (response.ok) {
                experienceForm.reset();

                document
                    .getElementById(
                        "add-experience-modal"
                    )
                    .hidePopover();


                showToast(
                    "Berhasil",
                    "Experience berhasil ditambahkan.",
                    "success"
                );


                fetchExperiences(
                    searchInput.value.trim()
                );

                return;
            }


            const errorMessages =
                Object.values(result).flat().filter(
                    value => typeof value === "string"
                );


            showToast(
                "Gagal menambahkan experience",
                errorMessages.length
                    ? errorMessages.join(" ")
                    : (
                        result.detail ||
                        `Terjadi kesalahan (${response.status}).`
                    ),
                "error"
            );

        } catch (error) {
            console.error(
                "Error adding experience:",
                error
            );


            showToast(
                "Gagal menambahkan experience",
                "Tidak dapat terhubung ke server.",
                "error"
            );

        } finally {
            submitButton.disabled = false;
        }
    }


    if (experienceForm) {
        experienceForm.addEventListener(
            "submit",
            addExperience
        );
    }


    fetchExperiences();
})();
