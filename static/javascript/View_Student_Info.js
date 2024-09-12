function editField(fieldId) {
    document.getElementById(`edit-${fieldId}-form`).style.display = 'block';
    document.getElementById(fieldId).style.display = 'none';
}

function saveField(fieldId) {
    const newValue = document.querySelector(`#edit-${fieldId}-form [name="new_value"]`).value;
    fetch('/update_student_info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            field: fieldId,
            value: newValue
        })
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              document.getElementById(fieldId).innerText = newValue;
              cancelEdit(`edit-${fieldId}-form`);
          } else {
              alert('Failed to update the field.');
          }
      });
}

function cancelEdit(formId) {
    const form = document.getElementById(formId);
    const fieldId = formId.replace('edit-', '').replace('-form', '');
    form.style.display = 'none';
    document.getElementById(fieldId).style.display = 'inline-block';
}
