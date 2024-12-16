"use strict";

(async () => {
    const picPhoto = document.getElementById("picPhoto");
    const picDesc = document.getElementById("picDesc");

    const r = await fetch("/api/pic/" + window.picId);

    if (r.ok) {
        const data = await r.json();
        picPhoto.src = data.src;

        // We need to block dangerous things!
        const blocklist = [
            "<comment",
            "<embed",
            "<link",
            "<listing",
            "<meta",
            "<noscript",
            "<object",
            "<plaintext",
            "<script",
            "<xmp",
            "<style",
            "<applet",
            "<iframe",
            "<img",
            "onload",
            "onblur",
            "onclick",
            "onerror",
            "href",
            "javascript",
            "window",
            "src",
        ];
        let description = String(data.description);
        blocklist.forEach((word) => {
            description = description.replace(word, "");
        });

        picDesc.innerHTML = description;
    } else {
        if (r.status == 401) {
            window.location.href = "/profile";
        } else {
            alert("Unable to load photo!");
        }
    }
})();
