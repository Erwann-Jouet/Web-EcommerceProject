document.addEventListener("DOMContentLoaded", () => {
    const editBtn = document.getElementById("edit-btn");
    const cancelBtn = document.getElementById("cancel-btn");
    const viewMode = document.getElementById("view-mode");
    const editMode = document.getElementById("edit-mode");
    const feedback = document.getElementById("feedback");
    const errorMessage = editMode ? editMode.querySelector(".error-message") : null;

    // Clic sur le bouton "Modifier"
    if (editBtn) {
        editBtn.addEventListener("click", (e) => {
            e.preventDefault();
            viewMode.classList.add("hidden");
            editMode.classList.remove("hidden");
            feedback.classList.add("hidden");
            if (errorMessage) errorMessage.classList.add("hidden");
        });
    }

    // Clic sur le bouton "Annuler"
    if (cancelBtn) {
        cancelBtn.addEventListener("click", (e) => {
            e.preventDefault();
            editMode.classList.add("hidden");
            viewMode.classList.remove("hidden");
            feedback.classList.add("hidden");
            if (errorMessage) errorMessage.classList.add("hidden");
        });
    }

    // Soumission du formulaire avec AJAX
    if (editMode) {
        editMode.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(editMode);

            try {
                const response = await fetch(editMode.action || "/auth/profile", {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });

                const result = await response.json();

                if (result.success) {
                    // Succès
                    feedback.textContent = "Profil mis à jour avec succès";
                    feedback.className = "alert alert-success success-message mb-3";
                    feedback.classList.remove("hidden");
                    feedback.style.display = "block";

                    editMode.classList.add("hidden");
                    editMode.style.display = "none";
                    
                    viewMode.classList.remove("hidden");
                    viewMode.style.display = "block";

                    // Recharger la page après 2 secondes
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else {
                    // Erreur de validation
                    if (errorMessage) {
                        errorMessage.textContent = result.error || "Erreur lors de la mise à jour du profil";
                        errorMessage.className = "alert alert-danger error-message";
                        errorMessage.classList.remove("hidden");
                    }
                }
            } catch (error) {
                console.error("Erreur AJAX:", error);
                if (errorMessage) {
                    errorMessage.textContent = "Erreur de communication avec le serveur";
                    errorMessage.className = "alert alert-danger error-message";
                    errorMessage.classList.remove("hidden");
                }
            }
        });
    }
});