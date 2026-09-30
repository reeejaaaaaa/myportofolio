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

    const createUrl =
        app.dataset.createUrl;

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


    function buildExperienceCardElement(item) {
        const experience =
            item.fields;

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
            experience.education
                ? `
                    <div class="experience-related">
                        <span class="experience-related-label">
                            Education
                        </span>

                        <span class="experience-related-value">
                            ${escapeHtml(experience.education)}
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
                    data-star-url="${escapeHtml(experience.star_url)}"
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
                        href="${escapeHtml(experience.edit_url)}"
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
                    experience.delete_url
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
            experience.started_at
        )}
        —
        ${experience.ended_at
                ? escapeHtml(
                    experience.ended_at
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
                experience.projects
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
                    item.fields.is_ongoing
            ).length;


        const uniqueProjectIds =
            new Set();


        let totalStars = 0;


        data.forEach(item => {
            const experience =
                item.fields;


            totalStars +=
                experience.star_count;


            experience.projects.forEach(
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
                        item.fields.category ===
                        selectedCategory
                )
                : [...currentExperienceData];


        if (sortSelect.value === "oldest") {
            filteredData.reverse();
        }


        if (sortSelect.value === "stars") {
            filteredData.sort(
                (a, b) =>
                    b.fields.star_count -
                    a.fields.star_count
            );
        }


        if (sortSelect.value === "az") {
            filteredData.sort(
                (a, b) =>
                    a.fields.title.localeCompare(
                        b.fields.title
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

                    const result =
                        await response
                            .json()
                            .catch(
                                () => ({})
                            );

                    if (!response.ok) {
                        throw new Error(
                            result.message ||
                            "Gagal menghapus experience."
                        );
                    }

                    showToast(
                        "Berhasil",
                        result.message,
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
                    result.message,
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


        try {
            const response =
                await fetch(
                    createUrl,
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken":
                                getCookie(
                                    "csrftoken"
                                ),

                            "X-Requested-With":
                                "XMLHttpRequest"
                        },

                        body:
                            new FormData(
                                experienceForm
                            )
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
                    result.message ||
                    "Experience berhasil ditambahkan.",
                    "success"
                );


                fetchExperiences(
                    searchInput.value.trim()
                );

                return;
            }


            const errorMessages =
                getFormErrorMessages(
                    result.errors
                );


            showToast(
                "Gagal menambahkan experience",
                errorMessages.length
                    ? errorMessages.join(" ")
                    : (
                        result.message ||
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
