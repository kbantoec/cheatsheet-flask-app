document.addEventListener("DOMContentLoaded", () => {
    buildToc();
    reinterpretTextAsHTML();
});

const buildToc = () => {
    // Get all the TOC items
    const tocItems = document.getElementsByClassName('toc-item');

    // Get the TOC list
    const ol = document.getElementById('toc-list');

    // Add the items to the list
    for (let i = 0; i < tocItems.length; i++) {
        const li = document.createElement('li');
        li.innerHTML = tocItems[i].innerText;
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
        tds[i].innerHTML = tds[i].innerText;
    }
};