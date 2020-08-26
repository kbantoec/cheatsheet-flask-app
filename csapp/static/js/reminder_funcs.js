// const addItemToTable = () => {
//     const btn = document.getElementById("add-item-to-table");
//     return ((btn.style.display === "block") ? btn.style.display = "none" : btn.style.display = "block");
// }

const addItemToTable = (element) => {
    const containerDiv = element.parentElement.parentElement;
    const forms = containerDiv.getElementsByTagName('form');
    if (forms.length > 0) {
        return ((forms[0].style.display === "block") ? forms[0].style.display = "none" : forms[0].style.display = "block");
    }
}


const autoGrow = (element) => {
    const body = document.getElementsByTagName('body')[0];
    const bodyFontSize = window.getComputedStyle(body, null).getPropertyValue("font-size");
    element.style.height = bodyFontSize;
    element.style.height = (element.scrollHeight) + "px";
}