/*
global
alertify: false
*/

/**
 * Update link to the docs.
 * @param {url} url - URL pointing to the right page of the docs.
 */
function doc(url) { // eslint-disable-line no-unused-vars
  $('#doc-link').attr('href', url);
}

/**
 * Show modal.
 * @param {name} name - Modal name.
 */
function showModal(name) { // eslint-disable-line no-unused-vars
  $(`#${name}`).modal('show');
}

/**
 * Reset form and show modal.
 * @param {name} name - Modal name.
 */
function resetShowModal(name) { // eslint-disable-line no-unused-vars
  $(`#${name}-form`).trigger('reset');
  $(`#${name}`).modal('show');
}

/**
 * Returns partial function.
 * @param {function} func - any function
 * @return {function}
 */
function partial(func, ...args) { // eslint-disable-line no-unused-vars
  return function() {
    return func.apply(this, args);
  };
}

/**
 * Capitalize.
 * @param {string} string - Word.
 * @return {capitalizedString}
 */
function capitalize(string) { // eslint-disable-line no-unused-vars
    return string.charAt(0).toUpperCase() + string.slice(1);
}

/**
 * jQuery Ajax Call.
 * @param {url} url - Url.
 * @param {callback} callback - Function to process results.
 */
function call(url, callback) { // eslint-disable-line no-unused-vars
  $.ajax({
    type: 'POST',
    url: url,
    success: function(results) {
      if (!results) {
        alertify.notify('HTTP Error 403 – Forbidden', 'error', 5);
      } else if (results.failure) {
        alertify.notify(results.error, 'error', 5);
      } else {
        callback(results);
      }
    },
  });
}

/**
 * jQuery Ajax Form Call.
 * @param {url} url - Url.
 * @param {form} form - Form.
 * @param {callback} callback - Function to process results.
 */
function fCall(url, form, callback) { // eslint-disable-line no-unused-vars
  if ($(form).parsley().validate()) {
    $.ajax({
      type: 'POST',
      url: url,
      data: $(form).serialize(),
      success: function(results) {
        if (!results) {
          alertify.notify('HTTP Error 403 – Forbidden', 'error', 5);
        } else if (results.failure) {
          alertify.notify(results.error, 'error', 5);
        } else {
          callback(results);
        }
      },
    });
  }
}

/**
 * Delete object.
 * @param {type} type - Node or link.
 * @param {id} id - Id of the object to delete.
 */
function deleteInstance(type, id) { // eslint-disable-line no-unused-vars
  call(`/delete/${type}/${id}`, function(result) {
    table.row($(`#${id}`)).remove().draw(false);
    alertify.notify(`${type} '${result.name}' deleted.`, 'error', 5);
  });
}