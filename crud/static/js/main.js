
const btnDelete= document.querySelectorAll('.btn-borrar');
if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('¿Está seguro de querer borrar?')){
        e.preventDefault();
      }
    });
  })
}
document.addEventListener("DOMContentLoaded", function () {
  const theme = localStorage.getItem("theme") || "light";
  setTheme(theme);
});

function setTheme(theme) {
  let themeStylesheet = document.getElementById("themeStylesheet");

  if (theme === "dark") {
    themeStylesheet.href = "https://bootswatch.com/5/darkly/bootstrap.min.css";
  } else {
    themeStylesheet.href = "https://bootswatch.com/5/cosmo/bootstrap.min.css";
  }

  localStorage.setItem("theme", theme);
}
