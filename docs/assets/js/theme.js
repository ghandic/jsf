var buttons = document.querySelectorAll("button[data-md-color-scheme]");

toggleThemeButton = function () {
    var attr = this.getAttribute("data-md-color-scheme");
    document.body.setAttribute("data-md-color-scheme", attr);

    buttons.forEach(function (button) {
        var state = button.getAttribute("data-md-state");
        switch (state) {
            case "hidden":
                button.setAttribute("data-md-state", "visible");
                button.style.visibility = "visible";
                button.style.display = "block";
                break;

            case "visible":
                button.setAttribute("data-md-state", "hidden");
                button.style.visibility = "hidden";
                button.style.display = "none";
                break;
        }
    });
};

buttons.forEach(function (button) {
    button.addEventListener("click", toggleThemeButton);
    button.style.visibility = button.getAttribute("data-md-state");
    if (button.getAttribute("data-md-state") === "hidden") {
        var attr = button.getAttribute("data-md-color-scheme");
        document.body.setAttribute("data-md-color-scheme", attr);
    }
});
