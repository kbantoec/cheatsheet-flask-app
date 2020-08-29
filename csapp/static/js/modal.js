
document.addEventListener("DOMContentLoaded", () => {
    // Build a Popup With JavaScript: https://www.youtube.com/watch?v=MBaw_6cPmAw
    const openModalButtons = document.querySelectorAll('[data-modal-target]');
    const closeModalButtons = document.querySelectorAll('[data-close-button]');
    const overlay = document.getElementById('overlay');

    openModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Use the data attribute from the button with button.dataset
            const modal = document.querySelector(button.dataset.modalTarget);
            openModal(modal);
            const modalBody = modal.lastElementChild;
            
    
            createSyntaxFrom(button, modalBody);
            createExampleFrom(button, modalBody);
            createLinksListFrom(button, modalBody);
            // modalBody.setAttribute('onload', 'hljs.initHighlightingOnLoad()');
        });
    });

    closeModalButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            closeModal(modal);
        });
    });

    overlay.addEventListener('click', () => {
        const modals = document.querySelectorAll('.modal.activateModal');
        modals.forEach(modal => {  
            // to close modal when clicking outside
            closeModal(modal);
        });
    });
});


const openModal = (modal) => {
    if (modal != null) {
        modal.classList.add('activateModal');
        overlay.classList.add('activateOverlay');
    }
};


const closeModal = (modal) => {
    if (modal != null) {
        let modalBody = modal.lastElementChild;
        // modalBody.removeChild(modalBody.lastChild);
        modalBody.innerHTML = '';
        modal.classList.remove('activateModal');
        overlay.classList.remove('activateOverlay');
    }
};



const createSyntaxFrom = (button, element) => {
    // let tr = document.querySelectorAll('[data-modal-target]')[0].parentElement.parentElement;
    const tr = button.parentElement.parentElement;

    if (tr.dataset.syntaxContent.length > 0) {
        const lang = tr.dataset.lang;
        const syntaxContent = tr.dataset.syntaxContent;

        const h1 = document.createElement('h1');
        h1.innerText = "Syntax";

        const pre = document.createElement('pre');
        // pre.classList.add('lil');

        const code = document.createElement('code');
        code.classList.add(lang);
        code.innerText = syntaxContent;

        pre.append(code);
        element.append(h1);
        element.append(pre);
    }    
};

const createExampleFrom = (button, element) => {
    const tr = button.parentElement.parentElement;

    if (tr.dataset.exampleContent.length > 0) {
        const lang = tr.dataset.lang;
        const exampleContent = tr.dataset.exampleContent;
        const exampleCaption = tr.dataset.exampleCaption;

        const h1 = document.createElement('h1');
        h1.innerText = "Examples";

        const h2 = document.createElement('h2');
        h2.innerHTML = exampleCaption;

        const pre = document.createElement('pre');
        // pre.classList.add('lil');

        const code = document.createElement('code');
        code.classList.add(lang);
        code.innerText = exampleContent;

        pre.append(code);
        element.append(h1);
        element.append(h2);
        element.append(pre);
    }    
};

const createLinksListFrom = () => {

};



