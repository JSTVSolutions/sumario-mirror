class Sumario {
  static _getElemById(id) {
    return document.getElementById(id);
  }

  static submit(formId, actionUrl) {
    let form = this._getElemById(formId);

    if (!form.checkValidity()) {
      return;
    }

    form.action = actionUrl;
    form.submit();
  }
}
