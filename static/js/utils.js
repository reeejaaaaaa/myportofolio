function getCookie(name) {
    let cookieValue = null;

    if (
        document.cookie &&
        document.cookie !== ""
    ) {
        const cookies =
            document.cookie.split(";");

        for (const item of cookies) {
            const cookie = item.trim();

            if (
                cookie.startsWith(
                    `${name}=`
                )
            ) {
                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;
            }
        }
    }

    return cookieValue;
}


function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}


function getFormErrorMessages(errors) {
    if (!errors) {
        return [];
    }

    return Object
        .values(errors)
        .flat()
        .map(error => error.message);
}