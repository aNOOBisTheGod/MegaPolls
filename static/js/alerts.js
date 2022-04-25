const Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.addEventListener("mouseenter", Swal.stopTimer);
    toast.addEventListener("mouseleave", Swal.resumeTimer);
  },
});

function showToast(icon, title) {
  Toast.fire({
    icon: icon,
    title: title,
    background: "rgba(0, 0, 0, 0.9)",
    color: "white",
  });
}

function showAlert(icon, message){
  Swal.fire({
    position: 'top-end',
    icon: icon,
    title: message,
    background: "rgba(0, 0, 0, 0.9)",
    showConfirmButton: false,
    timer: 1500,
    color: 'white'
  })
}