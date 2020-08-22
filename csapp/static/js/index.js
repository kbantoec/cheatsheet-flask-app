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

    const form = document.createElement('FORM');
    form.setAttribute('action', '/');
    form.setAttribute('method', 'POST');
    form.appendChild(input);
    form.appendChild(submit);

    const a = document.createElement('a');
    a.appendChild(form);

    let numberItems = container.children.length
    container.insertBefore(a, container.children[numberItems - 1]);
};