const createDeleteBtn = (optionLabel, id) => {
    const deleteBtn = document.createElement('a');
    deleteBtn.setAttribute('href', '/delete/' + id);
    deleteBtn.setAttribute('class', `delete-${optionLabel}-btn ${optionLabel}-options`);
    const trashIcon = document.createElement('i');
    trashIcon.setAttribute('class', 'fa fa-trash');
    deleteBtn.append(trashIcon);
    return deleteBtn;
};


// const updateCommand = (element) => {
//     const tdCommand = element.parentElement;
//     const tr = tdCommand.parentElement;
//     const paragraphs = tr.querySelectorAll('p');

//     if (paragraphs.length === 2) {
//         const pCommand = paragraphs[0];
//         const pDescription = paragraphs[1];

//         const commandInput = createNewInput('')
//         pCommand.replaceWith();
//     }
// };


// const createNewInput = () => {

// };


const createOptionBtn = (action, optionLabel, id) => {
    const btn = document.createElement('a');
    const ico = document.createElement('i');

    switch(action) {
        case 'delete':
            btn.setAttribute('href', `/delete_${optionLabel}/${id}`);
            btn.setAttribute('class', `delete-${optionLabel}-btn ${optionLabel}-options`);
            ico.setAttribute('class', 'fa fa-trash');
            break;
        case 'update':
            btn.setAttribute('href', `/update_${optionLabel}/${id}`);
            btn.setAttribute('class', `update-${optionLabel}-btn ${optionLabel}-options`);
            // btn.setAttribute('onclick', 'updateCommand(this);');
            ico.setAttribute('class', 'fa fa-pencil');
    }

    btn.append(ico);
    return btn;
};