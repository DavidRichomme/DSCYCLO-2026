document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            if (data.password === "") {
                delete data.password;
            }

            Object.keys(data).forEach(key => {
                if (data[key] === "") {
                    if (form.dataset.method === "PATCH") {
                        data[key] = null; // désattribution explicite en modification
                    } else {
                        delete data[key]; // pas de valeur à la création
                    }
                }
            });

            const response = await fetch(form.action, {
                method: form.dataset.method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erreur lors de l'enregistrement");
            }
        });
    });


    document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (event) => {
        event.stopPropagation(); // empêche le clic de remonter au tr/td parent
        
        if (!confirm("Confirmer la suppression ?")) return;

        const url = btn.dataset.url;
        const response = await fetch(url, { method: "DELETE" });

        if (response.ok) {
            window.location.reload();
        } else {
            alert("Erreur lors de la suppression");
        }
    });
});

let piecesAjoutees = [];

const addPieceBtn = document.getElementById('add-piece-btn');
if (addPieceBtn) {
    addPieceBtn.addEventListener('click', () => {
        const select = document.getElementById('piece-select');
        const quantiteInput = document.getElementById('piece-quantite');

        const pieceId = select.value;
        const pieceLibelle = select.options[select.selectedIndex].dataset.libelle;
        const quantite = parseInt(quantiteInput.value);

        if (!pieceId || quantite < 1) {
            alert("Sélectionne une pièce et une quantité valide");
            return;
        }

        piecesAjoutees.push({ piece_id: parseInt(pieceId), quantite: quantite });

        const container = document.getElementById('pieces-container');
        const ligne = document.createElement('div');
        ligne.className = "flex justify-between items-center bg-gray-100 p-2 rounded mb-1";
        ligne.innerHTML = `<span>${pieceLibelle} x${quantite}</span>`;
        container.appendChild(ligne);

        select.value = "";
        quantiteInput.value = 1;
    });
}
});