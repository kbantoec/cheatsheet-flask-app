
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
    btn.setAttribute('class', `add-${subItemLabel}-btn add-btn`);
    btn.setAttribute('onclick', func + '(this);');
    // btn.innerText = '+';
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
        let undoBtn;

        switch (optionLabel) {
            case 'example':
                // Delete button
                deleteBtn = createOptionBtn('delete', optionLabel, div.dataset.exampleId);                
                // Update button
                // updateBtn = document.createElement('a');
                // const ico = document.createElement('i');
                // updateBtn.setAttribute('class', `update-${optionLabel}-btn ${optionLabel}-options`);
                // updateBtn.setAttribute('onclick', 'updateExample(this);');
                // ico.setAttribute('class', 'fa fa-pencil');            
                // updateBtn.append(ico);
                updateBtn = createUpdateBtn(optionLabel, 'updateExample(this);');
                
                // Undo hidden button
                undoBtn = createOptionBtn('undo', optionLabel, div.dataset.exampleId);
                
                break;
            case 'link':
                // Delete button
                deleteBtn = createOptionBtn('delete', optionLabel, div.dataset.linkId);                
                // Update button
                updateBtn = createUpdateBtn(optionLabel, 'updateLink(this);');
                // Undo hidden button
                undoBtn = createOptionBtn('undo', optionLabel, div.dataset.linkId);
        }      
        
        // Add the buttons to the div element
        optionBtnsDiv.append(deleteBtn);
        optionBtnsDiv.append(updateBtn);
        optionBtnsDiv.append(undoBtn);
        div.append(optionBtnsDiv);
    });
};


const createUpdateBtn = (optionLabel, onclickFunc) => {
    /*
     * `onclickFunc` e.g.: 'updateExample(this);'
     */
    const anchorBtn = document.createElement('a');
    const ico = document.createElement('i');
    anchorBtn.setAttribute('class', `update-${optionLabel}-btn ${optionLabel}-options`);
    anchorBtn.setAttribute('onclick', onclickFunc);
    ico.setAttribute('class', 'fa fa-pencil');            
    anchorBtn.append(ico);
    return anchorBtn;
};


const updateExample = (element) => {
    const optionBtnsDiv = element.parentElement;
    const exampleDiv = optionBtnsDiv.parentElement;

    // Create the form
    const form = document.createElement('form');
    const action = document.getElementsByClassName('modal-body')[0].dataset.actionPath;
    form.setAttribute('action', action);
    form.setAttribute('method', 'POST');
    form.setAttribute('id', 'update-example-form');

    const exampleCaptionLabel = document.createElement('label');
    exampleCaptionLabel.setAttribute('for', 'example_caption');
    exampleCaptionLabel.setAttribute('class', 'update-example-labels');
    exampleCaptionLabel.innerText = 'Example caption';

    const exampleCaptionTextarea = document.createElement('textarea');
    exampleCaptionTextarea.setAttribute('type', 'text');
    exampleCaptionTextarea.setAttribute('name', 'example_caption');
    exampleCaptionTextarea.setAttribute('class', 'update-example-content');
    exampleCaptionTextarea.setAttribute('id', 'example_caption_update');
    exampleCaptionTextarea.setAttribute('oninput', 'autoGrow(this);')
    const exampleCaption = exampleDiv.querySelector('h2');
    exampleCaptionTextarea.innerText = exampleCaption.innerText;

    const exampleContentLabel = document.createElement('label');
    exampleContentLabel.setAttribute('for', 'example_content');
    exampleContentLabel.setAttribute('class', 'update-example-labels');
    exampleContentLabel.innerText = 'Example content';

    const exampleContentTextarea = document.createElement('textarea');
    exampleContentTextarea.setAttribute('type', 'text');
    exampleContentTextarea.setAttribute('name', 'example_content');
    exampleContentTextarea.setAttribute('class', 'update-example-content');
    exampleContentTextarea.setAttribute('id', 'example_content_update');
    exampleContentTextarea.setAttribute('oninput', 'autoGrow(this);')
    exampleContentTextarea.innerText = exampleDiv.querySelector('code').innerText;

    const formName = createHiddenInput('formName', 'update example');
    const exampleId = createHiddenInput('example_id', exampleDiv.dataset.exampleId);

    const submitBtn = document.createElement('input');
    submitBtn.setAttribute('type', 'submit');
    submitBtn.setAttribute('value', 'Update example');
    submitBtn.setAttribute('class', 'submit-btn');   

    form.append(exampleCaptionLabel);
    form.append(exampleCaptionTextarea);
    form.append(exampleContentLabel);
    form.append(exampleContentTextarea);
    form.append(formName);
    form.append(exampleId);
    form.append(submitBtn);
    
    exampleCaption.classList.add('hidden');
    exampleDiv.querySelector('pre').classList.add('hidden');
    exampleDiv.insertBefore(form, optionBtnsDiv);

    const undoBtn = optionBtnsDiv.getElementsByClassName('undo-example-btn')[0];
    undoBtn.setAttribute('onclick', 'exitExampleEditMode(this);')
    undoBtn.classList.remove('hidden');

    const deleteBtn = optionBtnsDiv.getElementsByClassName('delete-example-btn')[0];
    deleteBtn.classList.add('hidden');
    const updateBtn = optionBtnsDiv.getElementsByClassName('update-example-btn')[0];
    updateBtn.classList.add('hidden');
};

const exitExampleEditMode = (element) => {
    const optionBtnsDiv = element.parentElement;
    const exampleDiv = optionBtnsDiv.parentElement;
    const form = document.getElementById('update-example-form');

    const deleteBtn = optionBtnsDiv.getElementsByClassName('delete-example-btn')[0];
    deleteBtn.classList.remove('hidden');
    const updateBtn = optionBtnsDiv.getElementsByClassName('update-example-btn')[0];
    updateBtn.classList.remove('hidden');
    const undoBtn = optionBtnsDiv.getElementsByClassName('undo-example-btn')[0];
    undoBtn.classList.add('hidden');

    // Remove the form
    form.remove()
    // De-hide the other elements
    exampleDiv.querySelector('pre').classList.remove('hidden');
    exampleDiv.querySelector('h2').classList.remove('hidden');
};


const createUpdateFormLabel = (forValue, classValue, innerTextValue) => {
    const label = document.createElement('label');
    label.setAttribute('for', forValue);
    label.setAttribute('class', classValue);
    label.innerText = innerTextValue;
    return label;
};

const createUpdateFormTextarea = (nameAndIdValue, classValue) => {
    const textarea = document.createElement('textarea');
    textarea.setAttribute('type', 'text');
    textarea.setAttribute('name', nameAndIdValue);
    textarea.setAttribute('class', classValue);
    textarea.setAttribute('id', nameAndIdValue);
    textarea.setAttribute('oninput', 'autoGrow(this);')
    return textarea;
};


const createLinkTypeOption = (nameValue) => {
    const option = document.createElement('option');
    option.setAttribute('name', nameValue.toLowerCase());
    option.innerText = nameValue.toLowerCase();
    return option;
};


const createLinkTypeSelect = (nameValueAndId, classValue) => {
    const linkTypeSelect = document.createElement('select');
    linkTypeSelect.setAttribute('name', nameValueAndId);
    linkTypeSelect.setAttribute('id', nameValueAndId);
    linkTypeSelect.setAttribute('class', classValue);

    const video = createLinkTypeOption('video');
    const code = createLinkTypeOption('code');
    const text = createLinkTypeOption('text');
    const pdf = createLinkTypeOption('pdf');
    const zip = createLinkTypeOption('zip');
    const image = createLinkTypeOption('image');
    const excel = createLinkTypeOption('excel');
    const archive = createLinkTypeOption('archive');
    const audio = createLinkTypeOption('audio');

    linkTypeSelect.append(video);
    linkTypeSelect.append(code);
    linkTypeSelect.append(text);
    linkTypeSelect.append(pdf);
    linkTypeSelect.append(zip);
    linkTypeSelect.append(image);
    linkTypeSelect.append(excel);
    linkTypeSelect.append(archive);
    linkTypeSelect.append(audio);
    return linkTypeSelect;
};


const updateLink = (element) => {
    /*
     * We create a form on the fly and hide the other elements such that
     * if we need to undo the edit-mode, we can de-hide and remove the form,
     * otherwise, we sumit the form and return to the current page.
     */
    const optionBtnsDiv = element.parentElement;
    const li = optionBtnsDiv.parentElement;
    const anchor = li.querySelector('a');
    const span = li.querySelector('span');
    console.log(li);

    // Create the form
    const form = document.createElement('form');
    const action = document.getElementsByClassName('modal-body')[0].dataset.actionPath;
    form.setAttribute('action', action);
    form.setAttribute('method', 'POST');
    form.setAttribute('id', 'update-link-form');

    // Create form entries
    const linkLabelLabel = createUpdateFormLabel(forValue='link_label_update', classValue='update-link-labels', innerTextValue='Link label');
    const linkLabelTextarea = createUpdateFormTextarea(nameAndIdValue='link_label_update', classValue='update-link-textarea');
    linkLabelTextarea.innerText = anchor.innerText;
    const linkHrefLabel = createUpdateFormLabel(forValue='link_href_update', classValue='update-link-labels', innerTextValue='Link href');   
    const linkHrefTextarea = createUpdateFormTextarea(nameAndIdValue='link_href_update', classValue='update-link-textarea');
    linkHrefTextarea.innerText = anchor.getAttribute('href');
    const linkTypeLabel = createUpdateFormLabel(forValue='link_type_update', classValue='update-link-labels', innerTextValue='Link type');
    const linkTypeSelect = createLinkTypeSelect(nameAndIdValue='link_type_update', classValue='update-link-select');
    
    const formName = createHiddenInput('formName', 'update link');
    const linkId = createHiddenInput('link_id', li.dataset.linkId);    
    const submitBtn = document.createElement('input');
    submitBtn.setAttribute('type', 'submit');
    submitBtn.setAttribute('value', 'Update link');
    submitBtn.setAttribute('class', 'submit-btn');
    
    // Append all entries to the form
    form.append(linkLabelLabel);
    form.append(linkLabelTextarea);
    form.append(linkHrefLabel);
    form.append(linkHrefTextarea);
    form.append(linkTypeLabel);
    // form.append(linkTypeTextarea);
    form.append(linkTypeSelect);
    form.append(formName);
    form.append(linkId);
    form.append(submitBtn);

    // Insert the form in list
    li.insertBefore(form, optionBtnsDiv);

    // Hide and de-hide elements
    span.classList.add('hidden');
    anchor.classList.add('hidden');
    const undoBtn = optionBtnsDiv.getElementsByClassName('undo-link-btn')[0];
    undoBtn.classList.remove('hidden');
    undoBtn.setAttribute('onclick', 'exitLinkEditMode(this);');
    optionBtnsDiv.getElementsByClassName('delete-link-btn')[0].classList.add('hidden');
    optionBtnsDiv.getElementsByClassName('update-link-btn')[0].classList.add('hidden');
};


const exitLinkEditMode = (element) => {
    const optionBtnsDiv = element.parentElement;
    const li = optionBtnsDiv.parentElement;
    const form = document.getElementById('update-link-form');

    const deleteBtn = optionBtnsDiv.getElementsByClassName('delete-link-btn')[0];
    deleteBtn.classList.remove('hidden');
    const updateBtn = optionBtnsDiv.getElementsByClassName('update-link-btn')[0];
    updateBtn.classList.remove('hidden');
    const undoBtn = optionBtnsDiv.getElementsByClassName('undo-link-btn')[0];
    undoBtn.classList.add('hidden');

    // Remove the form
    form.remove()
    // De-hide the other elements
    li.querySelector('span').classList.remove('hidden');
    li.querySelector('a').classList.remove('hidden');
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
    const select = createLinkTypeSelect(nameAndIdValue='link_type', classValue='add-item-input')
    form.append(select);
    // createFormEntry(form, 'Link type', 'link_type');    /////////////
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

