const addItemToTable = (element) => {
    const containerDiv = element.parentElement.parentElement;
    const forms = containerDiv.getElementsByTagName('form');
    
    if (forms.length > 0) {
        const instruction1 = (forms[0].style.display === "block") ? forms[0].style.display = "none" : forms[0].style.display = "block";
        const instruction2 = (element.innerHTML === `<i class="fa fa-plus-square"></i>`) ? element.innerHTML = `<i class="fa fa-minus-square"></i>` : element.innerHTML = `<i class="fa fa-plus-square"></i>`;
        return (instruction1) && (instruction2);
    }
};


const autoGrow = (element) => {
    const body = document.getElementsByTagName('body')[0];
    const bodyFontSize = window.getComputedStyle(body, null).getPropertyValue("font-size");
    element.style.height = bodyFontSize;
    element.style.height = (element.scrollHeight) + "px";
};


const addExamplesToCommand = (element) => {
    const forms = document.getElementsByTagName('form');
    
    if (forms.length > 0) {
        const instruction1 = (forms[1].style.display === "block") ? forms[1].style.display = "none" : forms[1].style.display = "block";
        const instruction2 = (element.innerHTML === `<i class="fa fa-plus-square"></i>`) ? element.innerHTML = `<i class="fa fa-minus-square"></i>` : element.innerHTML = `<i class="fa fa-plus-square"></i>`;
        return (instruction1) && (instruction2);
    }
};


const addLinksToCommand = (element) => {
    const forms = document.getElementsByTagName('form');
    
    if (forms.length > 0) {
        const instruction1 = (forms[2].style.display === "block") ? forms[2].style.display = "none" : forms[2].style.display = "block";
        const instruction2 = (element.innerHTML === `<i class="fa fa-plus-square"></i>`) ? element.innerHTML = `<i class="fa fa-minus-square"></i>` : element.innerHTML = `<i class="fa fa-plus-square"></i>`;
        return (instruction1) && (instruction2);
    }
};


const noneToBlock = (arr) => {
    arr.forEach(element => {
        return (element.style.display === "block") ? element.style.display = "none" : element.style.display = "block";
    });
};
