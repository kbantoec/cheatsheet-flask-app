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

    // for (let i = 0; i < tds.length; i++) {
    //     tds[i].innerHTML = tds[i].innerText;
    //     if (i % 2 !== 0) {
    //         addModalBtn(tds[i]);
    //     }
    // }

    for (let i = 0; i < tds.length; i++) {  
        tds[i].innerHTML = tds[i].innerText;      
        if (i % 2 !== 0) {
            // Appends the modal button if it is a cell of the second column in the table
            const btn = `<button data-modal-target="#modal" class="modalBtn"><span><i class="fa fa-info-circle"></i></span></button>`;
            tds[i].innerHTML += btn;
        }
    }
};


const getBaseUri = () => {
    return document.getElementsByClassName('main-title')[0].firstChild["baseURI"];
};


// const addModalBtn = (element) => {
//     const btn = `<button data-modal-target="#modal" class="modalBtn"><span><i class="fa fa-info-circle"></i></span></button>`;
//     element.innerHTML = element.innerText + "&nbsp;" + btn;
// };