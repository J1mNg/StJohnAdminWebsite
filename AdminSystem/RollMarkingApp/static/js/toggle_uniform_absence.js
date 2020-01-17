function toggle_uniform_absence(cadet_pk) {
  checkbox_attendance = document.getElementById("attendance_".concat(cadet_pk.toString()));
  checkbox_uniform = document.getElementById("uniform_".concat(cadet_pk.toString()));
  select_absence = document.getElementById("absence_".concat(cadet_pk.toString()));
  if (checkbox_attendance.checked == true) {
    checkbox_uniform.style.display = 'initial';
    select_absence.style.display = 'none'
  } else {
    checkbox_uniform.style.display = 'none';
    select_absence.style.display = 'initial'
  }
}
