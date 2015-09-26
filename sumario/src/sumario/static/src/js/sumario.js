function getElemById(id) {
    return document.getElementById(id);
}

function getAttr(elem, name) {
    return elem.getAttribute(name);
}

function getAttrById(id, name) {
    return getAttr(getElemById(id), name);
}

function setAttr(elem, name, value) {
    elem.setAttribute(name, value);
}

function setAttrById(id, name, value) {
    setAttr(getElemById(id), name, value);
}

function addClass(elem, klass) {
    elem.classList.add(klass);
}

function addClassById(id, klass) {
    addClass(getElemById(id), klass);
}

function removeClass(elem, klass) {
    elem.classList.remove(klass);
}

function removeClassById(id, klass) {
    removeClass(getElemById(id), klass);
}

function showModal(id) {
    addClassById(id, "is-active");
}

function hideModal(id) {
    removeClassById(id, "is-active");
}

function showElem(id) {
    removeClassById(id, "is-hidden");
}

function hideElem(id) {
    addClassById(id, "is-hidden");
}

function selectTab(id) {
    addClassById(id, "is-active");
}

function toggleValue(id, defaultValue, useDefault) {
    elem = getElemById(id);
    if (useDefault) {
        elem.readOnly = true;
        elem.previousValue = elem.value || "";
        elem.value = defaultValue;
    }
    else {
        elem.value = elem.previousValue || "";
        elem.readOnly = false;
    }
}

function addOnLoadFn(onLoadFn) {
    if (typeof window.onload != 'function') {
        window.onload = onLoadFn;
    }
    else {
        var previousOnLoadFn = window.onload;
        window.onload = function() {
            if (previousOnLoadFn) {
                previousOnLoadFn();
            }
            onLoadFn();
        }
    }
}
