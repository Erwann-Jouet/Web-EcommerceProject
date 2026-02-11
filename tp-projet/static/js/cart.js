const BASE_URL = window.location.origin;
const API_CART_ADD = `${BASE_URL}/api/cart/add`;
const API_CART_REMOVE = `${BASE_URL}/api/cart/remove`;

document.addEventListener("DOMContentLoaded", () => {
    configurerBoutonsAjouterPanier();
    configurerBoutonsSupprimerPanier();
    configurerChampQuantitePanier();
});

// --- FONCTIONS DE CONFIGURATION ---

function configurerBoutonsAjouterPanier() {
    const buttons = document.querySelectorAll('.add-to-cart-btn');
    buttons.forEach(bouton => {
        bouton.addEventListener('click', () => {
            const productId = bouton.dataset.productId;
            const qtyInput = document.getElementById(`qty-${productId}`);
            const quantity = qtyInput ? parseInt(qtyInput.value) : 1;
            
            ajouterAuPanier(productId, quantity);
        });
    });
}

function configurerBoutonsSupprimerPanier() {
    const buttons = document.querySelectorAll('.remove-from-cart-btn');
    buttons.forEach(bouton => {
        bouton.addEventListener('click', () => {
            const productId = bouton.dataset.productId;
            supprimerDuPanier(productId);
        });
    });
}

function configurerChampQuantitePanier() {
    const inputs = document.querySelectorAll('.cart-item-quantity');
    inputs.forEach(input => {
        input.addEventListener('change', (event) => {
            const productId = input.dataset.productId;
            const newQuantity = parseInt(event.target.value);
            mettreAJourQuantite(productId, newQuantity); 
        });
    });
}

// --- FONCTIONS API (AJAX) ---

function ajouterAuPanier(productId, quantity) {
    const url = `${API_CART_ADD}/${productId}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: parseInt(quantity) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const badge = document.getElementById('cart-item-count');
            if (badge) badge.innerText = data.cart_count;
            
            if (document.querySelector('.cart-container')) {
                window.location.reload();
            }
        } else {
            alert("Erreur : " + data.error);
        }
    })
    .catch(error => console.error("Erreur API:", error));
}

function mettreAJourQuantite(productId, quantity) {
    const url = `${BASE_URL}/api/cart/update/${productId}`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: parseInt(quantity) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Erreur : " + data.error);
        }
    })
    .catch(error => console.error("Erreur API:", error));
}

function supprimerDuPanier(productId) {
    const url = `${API_CART_REMOVE}/${productId}`;

    fetch(url, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        } else {
            alert("Erreur lors de la suppression");
        }
    })
    .catch(error => console.error("Erreur API:", error));
}