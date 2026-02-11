document.addEventListener("DOMContentLoaded", function () {
    const usernameField = document.getElementById("username");
    const emailField = document.getElementById("email");
    const passwordField = document.getElementById("password");
    const form = document.getElementById("register-form");

    // Pattern du mot de passe: au moins une majuscule, un chiffre et un caractère spécial
    const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;

    // Vérifier username au blur
    if (usernameField) {
        usernameField.addEventListener("blur", function() {
            const value = this.value.trim();
            if (!value) return;

            if (value.length < 3 || value.length > 64 || !/^[a-z0-9]+$/.test(value)) {
                showError(form, "Le nom utilisateur doit contenir uniquement des lettres minuscules et des chiffres (3 à 64 caractères)");
                this.classList.add("input-error");
                return;
            }

            clearError(form);
            checkUserField("username", value);
        });
    }

    // Vérifier email au blur
    if (emailField) {
        emailField.addEventListener("blur", function() {
            const value = this.value.trim();
            if (!value) return;

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                showError(form, "L'email n'est pas valide");
                this.classList.add("input-error");
                return;
            }

            clearError(form);
            checkUserField("email", value);
        });
    }

    // Vérifier mot de passe en temps réel
    if (passwordField) {
        passwordField.addEventListener("input", function() {
            validatePassword(this.value);
        });
    }
});

function checkUserField(field, value) {
    if (!value) return;

    fetch(`/api/user/check?${field}=${encodeURIComponent(value)}`)
        .then(response => response.json())
        .then(data => {
            const fieldElement = document.getElementById(field);
            const form = document.getElementById("register-form");
            
            if (!form || !fieldElement) return;

            const existsFlag = data.exists ?? data.value ?? false;
            if (existsFlag) {
                showError(form, `Ce ${field} existe déjà`);
                fieldElement.classList.add("input-error");
            } else {
                fieldElement.classList.remove("input-error");
            }
        })
        .catch(err => console.error("Erreur lors de la vérification:", err));
}

function validatePassword(password) {
    const passwordField = document.getElementById("password");
    const form = document.getElementById("register-form");
    
    if (!passwordField || !form) {
        console.warn("Champs manquants pour la validation du mot de passe");
        return;
    }

    if (!password) {
        passwordField.classList.remove("input-error", "input-success");
        return;
    }

    const isValid = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/.test(password);
    if (isValid) {
        passwordField.classList.remove("input-error");
        passwordField.classList.add("input-success");
    } else {
        passwordField.classList.add("input-error");
        passwordField.classList.remove("input-success");
        showError(form, "Le mot de passe doit contenir au moins une majuscule, un chiffre et un caractère spécial");
    }
}

function showError(form, message) {
    if (!form) return;
    let errorDiv = form.querySelector("#form-error-message");
    if (!errorDiv) {
        errorDiv = document.createElement("div");
        errorDiv.id = "form-error-message";
        errorDiv.className = "alert alert-danger";
        form.insertBefore(errorDiv, form.firstChild);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = "block";
}

function clearError(form) {
    if (!form) return;
    const errorDiv = form.querySelector("#form-error-message");
    if (errorDiv) {
        errorDiv.textContent = "";
        errorDiv.style.display = "none";
    }
}