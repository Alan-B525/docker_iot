document.addEventListener("DOMContentLoaded", function () {
  // Inicializar tema
  const theme = localStorage.getItem("theme") || "light";
  setTheme(theme);

  // Manejar eventos de botones de borrar
  const btnDelete = document.querySelectorAll('.btn-borrar');
  if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        if (!confirm('¿Está seguro de querer borrar?')) {
          e.preventDefault();
        }
      });
    });
  }

  // Manejar selección de comando
  document.querySelectorAll('input[name="command"]').forEach((elem) => {
    elem.addEventListener("change", function (event) {
      var item = event.target.value;
      if (item === "setpoint") {
        document.getElementById("setpoint_value").style.display = "block";
      } else {
        document.getElementById("setpoint_value").style.display = "none";
      }
    });
  });

  // Manejar selección de tema
  const themeDropdownItems = document.querySelectorAll('#themeDropdown .dropdown-item');
  themeDropdownItems.forEach(item => {
    item.addEventListener('click', function (e) {
      e.preventDefault();
      const selectedTheme = this.getAttribute('data-theme');
      setTheme(selectedTheme);
    });
  });
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
