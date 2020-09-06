const addItem = () => {
    const container = document.getElementById('container');

    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('name', 'label');
    input.setAttribute('id', 'label');

    const submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Add item');
    submit.setAttribute('class', 'submit-btn');

    const hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'formName');    
    hiddenInput.setAttribute('value', 'create');
    
    const form = document.createElement('FORM');
    form.setAttribute('action', '/');
    form.setAttribute('method', 'POST');
    form.appendChild(input);
    form.appendChild(hiddenInput);
    form.appendChild(submit);

    const div = document.createElement('div');
    div.setAttribute('class', 'form-add-div');
    div.appendChild(form);

    let numberItems = container.children.length
    container.insertBefore(div, container.children[numberItems - 1]);
};


const replaceParagraphWithForm = (element) => {
    const mainDiv = element.parentElement.parentElement;
    const div = mainDiv.getElementsByClassName('item-label-paragraph')[0].parentElement;

    const aTag = mainDiv.querySelector('a');
    const itemId = mainDiv.dataset.itemId;

    const form = document.createElement('form');
    form.setAttribute('action', '/');
    form.setAttribute('method', 'POST');
    form.setAttribute('class', 'overlaid-form')    

    const input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('name', 'label');
    input.setAttribute('id', 'label');
    input.setAttribute('value', div.firstElementChild.innerText);

    const hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'formName');
    hiddenInput.setAttribute('value', 'update');

    const hiddenItemId = document.createElement('input');
    hiddenItemId.setAttribute('type', 'hidden');
    hiddenItemId.setAttribute('name', 'itemId');
    hiddenItemId.setAttribute('value', itemId);

    const submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Update item label');
    submit.setAttribute('class', 'submit-btn');
    submit.setAttribute('id', 'update-submit-btn');

    form.appendChild(input);
    form.appendChild(hiddenInput);
    form.appendChild(hiddenItemId);
    form.appendChild(submit);
    aTag.replaceWith(form);

    const optionBtnsDiv = mainDiv.getElementsByClassName('option-btns')[0];
    const undoAnchor = document.createElement('a');
    undoAnchor.setAttribute('onclick', 'exitEditMode(this);')
    undoAnchor.setAttribute('class', 'undo-btn options');
    const ico = document.createElement('i');   
    ico.setAttribute('class', 'fa fa-undo');
    undoAnchor.append(ico);
    optionBtnsDiv.append(undoAnchor);
};


const exitEditMode = (element) => {
    const mainDiv = element.parentElement.parentElement;
    const label = mainDiv.firstElementChild.firstElementChild.value;

    // Re-create former anchor tag
    const anchor = document.createElement('a');
    anchor.setAttribute('class', 'show-item');
    anchor.setAttribute('href', `./cheatsheet/${label}`);
    const div = document.createElement('div');
    const par = document.createElement('p');
    par.setAttribute('class', 'item-label-paragraph');
    par.innerText = label;
    div.append(par);
    anchor.append(div);

    // Replace the update form tag with the re-created anchor tag
    const form = mainDiv.firstElementChild;
    form.replaceWith(anchor);

    // Remove the exit-mode button from the option-btns div
    const exitEditModeAnchor = mainDiv.lastElementChild.lastElementChild;
    exitEditModeAnchor.remove();
};