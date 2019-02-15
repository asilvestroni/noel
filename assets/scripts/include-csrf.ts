const csrfList = document.getElementsByName('csrfmiddlewaretoken');
let csrfElement: null | HTMLInputElement = null;
if (csrfList.length > 0) {
    csrfElement = csrfList[0] as HTMLInputElement;
}

if (csrfElement) {
    window.$csrf = csrfElement.value;
}