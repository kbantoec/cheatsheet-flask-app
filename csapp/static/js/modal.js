
document.addEventListener("DOMContentLoaded", () => {
    // Build a Popup With JavaScript: https://www.youtube.com/watch?v=MBaw_6cPmAw
    const openModalButtons = document.querySelectorAll('[data-modal-target]');
    const closeModalButtons = document.querySelectorAll('[data-close-button]');
    const overlay = document.getElementById('overlay');

    openModalButtons.forEach(button => {
        // Give each button the ability to have an onclick event that opens and closes a modal
        button.addEventListener('click', () => {
            
            const modal = document.querySelector(button.dataset.modalTarget);
            openModal(modal);

            const modalBody = modal.lastElementChild;            
            appendSyntax(button, modalBody);
            appendExamples(button, modalBody);
            appendLinks(button, modalBody);
            document.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightBlock(block);
              });            
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


const appendSyntax = (button, element) => {
    // For JS console:
    // let tr = document.querySelectorAll('[data-modal-target]')[0].parentElement.parentElement;
    const tr = button.parentElement.parentElement.parentElement;

    if (tr.dataset.syntax.length > 0) {
        const lang = tr.dataset.lang;
        const syntaxContent = tr.dataset.syntax;

        const h1 = document.createElement('h1');
        h1.innerText = "Syntax";

        const pre = document.createElement('pre');
        // pre.classList.add('lil');

        const code = document.createElement('code');
        code.classList.add(lang);
        code.innerText = syntaxContent;

        pre.append(code);
        // The `element` is the modal body
        element.append(h1);
        element.append(pre);
    }    
};


const createFormEntry = (formToBeModified, labelText, attrValue) => {
    const div = document.createElement('div');
    const label = document.createElement('label');
    label.setAttribute('for', attrValue);
    label.innerText = labelText;
    const textarea = document.createElement('textarea');
    textarea.setAttribute('name', attrValue);
    textarea.setAttribute('id', attrValue);
    textarea.setAttribute('placeholder', 'Type ' + labelText.toLowerCase() + ' here...');
    textarea.setAttribute('oninput', 'autoGrow(this);');
    textarea.setAttribute('class', 'add-item-input')
    div.append(label);
    div.append(textarea);
    formToBeModified.append(div);
};


const createHiddenInput = (name, value) => {
    const input = document.createElement('input');
    input.setAttribute('type', 'hidden');
    input.setAttribute('name', name);
    input.setAttribute('value', value);
    return input;
};


const createInput = (name, value, type) => {
    const input = document.createElement('input');
    input.setAttribute('type', type);
    input.setAttribute('name', name);
    input.setAttribute('value', value);
    return input;
};


const createExamplesForm = (actionPath, commandId) => {
    const form = document.createElement('form');
    form.setAttribute('class', 'hidden');
    form.setAttribute('action', actionPath);
    form.setAttribute('method', 'POST');
    form.setAttribute('id', 'add-example-to-command');

    createFormEntry(form, 'Example caption', 'example_caption');
    createFormEntry(form, 'Example content', 'example_content');
    const hiddenInput = createHiddenInput('command_id', commandId);
    const hiddenFormName = createHiddenInput('formName', 'create new example');

    const submitInput = document.createElement('input');
    submitInput.setAttribute('type', 'submit');
    submitInput.setAttribute('value', 'Add the example to the command.');
    submitInput.setAttribute('id', 'submit-btn-example-input');

    const submitDiv = document.createElement('div');
    submitDiv.append(hiddenInput);
    submitDiv.append(hiddenFormName)
    submitDiv.append(submitInput);
    form.append(submitDiv);

    return form;
};


const subItemAddBtn = (subItemLabel, func) => {
    const btnContainer = document.createElement('div');
    btnContainer.setAttribute('id', 'add-' + subItemLabel + '-div');

    const btn = document.createElement('button');
    btn.setAttribute('class', 'add-item-btn');
    btn.setAttribute('onclick', func + '(this);');
    btn.innerHTML = `<i class="fa fa-plus-square"></i>`;
    return [btnContainer, btn];
};


const appendExamples = (button, element) => {
    // Retrieve parent data-* attributes from parent table row
    const tr = button.parentElement.parentElement.parentElement;

    // Create section title
    const h1 = document.createElement('h1');
    h1.innerText = "Examples";
    
    // Append the `+` button to the examples section
    const [exampleDivBtn, addExampleBtn] = subItemAddBtn('example', 'addExamplesToCommand');
    
    // Create section form
    const form = createExamplesForm(element.dataset.actionPath, tr.dataset.commandId);
    
    // Append all elements to modal body
    exampleDivBtn.append(addExampleBtn);
    element.append(h1);
    element.append(exampleDivBtn);
    element.append(form);

    // Show examples from GET request by adding them after the form tag with 'add-example-to-command' id
    loadDoc('/commands/' + tr.dataset.commandId, getDataExamples);
};


const addOptionsBtns = (optionLabel) => {
    const divs = document.getElementsByClassName(`${optionLabel}-div`);

    Object.entries(divs).forEach((entry) => {
        const div = entry[1];

        const optionBtnsDiv = document.createElement('div');
        optionBtnsDiv.setAttribute('class', 'option-btns-div');

        let deleteBtn;
        let updateBtn;

        switch(optionLabel) {
            case 'example':
                // Delete button
                deleteBtn = createOptionBtn('delete', optionLabel, div.dataset.exampleId);                
                // Update button
                updateBtn = createOptionBtn('update', optionLabel, div.dataset.exampleId);
                break;
            case 'link':
                // Delete button
                deleteBtn = createOptionBtn('delete', optionLabel, div.dataset.linkId);                
                // Update button
                updateBtn = createOptionBtn('update', optionLabel, div.dataset.linkId);
        }      
        
        // Add the buttons to the div element
        optionBtnsDiv.append(deleteBtn);
        optionBtnsDiv.append(updateBtn);
        div.append(optionBtnsDiv);
    });
};


const getDataExamples = (xhttp) => {
    const div = document.createElement('div');
    div.innerHTML = xhttp.responseText;
    const examplesContainer = div.lastElementChild;
    const referenceNode = document.getElementById("add-example-to-command");
    const modalBody = referenceNode.parentNode;
    modalBody.insertBefore(examplesContainer, referenceNode.nextSibling);

    // Highlight code
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });

    addOptionsBtns('example');
};

const getDataLinks = (xhttp) => {
    const div = document.createElement('div');
    div.innerHTML = xhttp.responseText;

    const referenceNode = document.getElementById("add-link-to-command");
    referenceNode.parentNode.insertBefore(div.lastElementChild, referenceNode.nextSibling);

    addOptionsBtns('link');
};


const createLinksForm = (actionPath, commandId) => {
    const form = document.createElement('form');
    form.setAttribute('class', 'hidden');
    form.setAttribute('action', actionPath);
    form.setAttribute('method', 'POST');
    form.setAttribute('id', 'add-link-to-command');

    createFormEntry(form, 'Link label', 'link_label');
    createFormEntry(form, 'Link href', 'link_href');
    createFormEntry(form, 'Link type', 'link_type');    
    const hiddenInput = createHiddenInput('command_id', commandId);
    const hiddenFormName = createHiddenInput('formName', 'create new link');
    
    const submitInput = document.createElement('input');
    submitInput.setAttribute('type', 'submit');
    submitInput.setAttribute('value', 'Add the link to the command.');
    submitInput.setAttribute('id', 'submit-btn-link-input');

    const submitDiv = document.createElement('div');
    submitDiv.append(hiddenInput);
    submitDiv.append(hiddenFormName);
    submitDiv.append(submitInput);
    form.append(submitDiv);

    return form;
};


const appendLinks = (button, element) => {
    // Retrieve parent data-* attributes from parent table row
    const tr = button.parentElement.parentElement.parentElement;

    // Create section title
    const h1 = document.createElement('h1');
    h1.innerText = "Links";
    
    // Append the `+` button to the examples section
    const [linkDivBtn, addLinkBtn] = subItemAddBtn('link', 'addLinksToCommand');
    
    // Create section form
    const form = createLinksForm(element.dataset.actionPath, tr.dataset.commandId);
    
    // Append all elements to modal body
    linkDivBtn.append(addLinkBtn);
    element.append(h1);
    element.append(linkDivBtn);
    element.append(form);

    // Show examples from GET request
    loadDoc('/links/' + tr.dataset.commandId, getDataLinks);
};


const loadDoc = (url, cFunction) => {
    var xhttp;
    xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        cFunction(this);
      }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
  }

