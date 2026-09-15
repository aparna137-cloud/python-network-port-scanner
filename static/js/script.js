document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const button = document.querySelector("#scanButton");

    const progressBox = document.querySelector("#scanProgress");
    const progressFill = document.querySelector("#progressFill");
    const progressText = document.querySelector("#progressText");
    const currentPort = document.querySelector("#currentPort");
    const openPorts = document.querySelector("#openPorts");

    if (!form || !button) {
        return;
    }

    // Hide progress box when the page first loads
    if (progressBox) {
        progressBox.style.display = "none";
    }

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        button.disabled = true;

        button.innerHTML = `
            <span class="spinner"></span>
            Scanning...
        `;

        button.style.cursor = "wait";

        // Show progress section
        if (progressBox) {
            progressBox.style.display = "block";
        }

        const formData = new FormData(form);

        try {

            const response = await fetch("/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            });

            const data = await response.json();

            if (!data.scan_id) {
                throw new Error("Scan ID was not returned.");
            }

            checkProgress(data.scan_id);

        } catch (error) {

            console.error("Scan error:", error);

            button.disabled = false;
            button.innerHTML = "Start Security Scan";
            button.style.cursor = "pointer";

            if (progressBox) {
                progressBox.style.display = "none";
            }

            alert("Unable to start the scan.");
        }
    });


    async function checkProgress(scanId) {

        try {

            const response = await fetch(`/progress/${scanId}`);
            const data = await response.json();

            console.log("Scan progress:", data);

            // Update percentage
            if (progressText) {
                progressText.textContent = `${data.progress}%`;
            }

            // Update progress bar
            if (progressFill) {
                progressFill.style.width = `${data.progress}%`;
            }

            // Update current port
            if (currentPort) {
                currentPort.textContent =
                    `Current port: ${data.current_port}`;
            }

            // Update open port count
            if (openPorts) {
                openPorts.textContent =
                    `Open ports: ${data.results.length}`;
            }


            if (
                data.status === "starting" ||
                data.status === "scanning"
            ) {

                setTimeout(function () {
                    checkProgress(scanId);
                }, 300);

            }

            else if (data.status === "completed") {

                // Make sure progress reaches 100%
                if (progressFill) {
                    progressFill.style.width = "100%";
                }

                if (progressText) {
                    progressText.textContent = "100%";
                }

                // Give the user a moment to see 100%
                setTimeout(function () {
                    window.location.reload();
                }, 500);

            }

            else if (data.status === "error") {

                alert(data.error || "Scan failed.");

                button.disabled = false;
                button.innerHTML = "Start Security Scan";
                button.style.cursor = "pointer";
            }

        } catch (error) {

            console.error("Progress check error:", error);

            setTimeout(function () {
                checkProgress(scanId);
            }, 1000);
        }
    }

});