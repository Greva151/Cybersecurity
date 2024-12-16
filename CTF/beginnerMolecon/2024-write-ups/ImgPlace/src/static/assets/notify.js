"use strict";

const notifySubmit = document.getElementById("notifySubmit");
const notifyForm = document.getElementById("notifyForm");
const successAlert = document.getElementById("successAlert");

notifyForm.onsubmit = async (e) => {
    e.preventDefault();

    notifySubmit.disabled = true;
    successAlert.style.display = "none";

    const r = await fetch("/api/proposals", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            id: window.picId,
            pow: e.target.pow.value,
        }),
    });

    if (r.ok) {
        successAlert.style.display = "block";
    } else {
        alert(
            "An error occured while sending this proposal. Reload the page and try again",
        );
    }

    notifySubmit.disabled = false;
};
