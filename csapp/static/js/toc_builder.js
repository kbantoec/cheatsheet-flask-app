document.addEventListener("DOMContentLoaded", () => {
    // Creates the table of contents (TOC) dynamically
    // Needs:
    // - getBaseUri(): to set the href attribute of the a tags in the TOC
    buildToc();

    // Re-interprets the injected database content as HTML and adds the modal butons
    reinterpretTextAsHTML();
});

const buildToc = () => {
    // Get all the TOC items
    const tocItems = document.getElementsByClassName('toc-item');

    // Get the TOC list
    const ol = document.getElementById('toc-list');

    // Add the items to the list
    for (let i = 0; i < tocItems.length; i++) {
        const IthtocItem = 'toc-item-' + i;
        tocItems[i].setAttribute('id', IthtocItem);

        const a = document.createElement('a');
        a.setAttribute('href', getBaseUri() + '#' + IthtocItem);
        a.innerHTML = tocItems[i].innerText;
        

        const li = document.createElement('li');
        li.append(a);
        ol.append(li);
    }
};

const reinterpretTextAsHTML = () => {
    // Get all the TOC items (where insertions have been made)
    const tocItems = document.getElementsByClassName('toc-item');
    const tds = document.getElementsByTagName('td');

    for (let i = 0; i < tocItems.length; i++) {
        tocItems[i].innerHTML = tocItems[i].innerText;
    }

    for (let i = 0; i < tds.length; i++) {
        // Convert input text to HTML
        tds[i].innerHTML = tds[i].innerText;

        // Insert it in a <p> tag
        const par = document.createElement('p');
        par.innerHTML = tds[i].innerHTML;
        tds[i].innerHTML = '';
        tds[i].append(par);

        if (i % 2 !== 0) {
            // Appends the modal button if it is a cell of the second column in the table
            const btn = `<button data-modal-target="#modal" class="modalBtn"><span><i class="fa fa-info-circle"></i></span></button>`;
            tds[i].firstElementChild.innerHTML += btn;
        } else {
            const tr = tds[i].parentElement;

            const optionsDiv = document.createElement('div');
            optionsDiv.setAttribute('class', 'toggle-down-options');
            const iconBtn = document.createElement('i');
            iconBtn.setAttribute('class', 'fa fa-caret-down triangle');
            optionsDiv.append(iconBtn);

            // Delete button
            const deleteBtn = createOptionBtn('delete', 'command', tr.dataset.commandId);

            // Update button
            const updateBtn = createOptionBtn('update', 'command', tr.dataset.commandId);

            optionsDiv.append(deleteBtn);
            optionsDiv.append(updateBtn);
            tds[i].insertBefore(optionsDiv, tds[i].lastElementChild);
        }
    }
};


const getBaseUri = () => {
    return document.getElementsByClassName('main-title')[0].firstChild["baseURI"];
};
