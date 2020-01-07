let csvRegex = new RegExp("(.*?)\.(csv)$");

function triggerValidation(el) {
  if (!(csvRegex.test(el.value.toLowerCase()))) {
    el.value = '';
    alert('Please select a .csv format file!');
  }
}