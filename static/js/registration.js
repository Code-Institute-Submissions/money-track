const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const passwordToggle = document.querySelector(".passwordToggle");
const submitBtn = document.querySelector(".submitBtn")


const handleToggle = (e) => {
    if (passwordToggle.textContent === "SHOW") {
        passwordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        passwordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }

};

passwordToggle.addEventListener("click", handleToggle);


emailField.addEventListener("keyup", (e) => {

    const emailVal = e.target.value;

    emailField.classList.remove('is-invalid');
    emailFeedbackArea.style.display = "none";

    if (emailVal.length > 0) {
        fetch("/authentication/authenticate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.email_error) {
                    emailField.classList.add('is-invalid');
                    emailFeedbackArea.style.display = "block";
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                    submitBtn.disabled = true;
                } else submitBtn.removeAttribute("disabled");
            });
    }
});

usernameField.addEventListener("keyup", (e) => {

    const usernameVal = e.target.value;

    usernameField.classList.remove('is-invalid');
    feedbackArea.style.display = "none";

    if (usernameVal.length > 0) {
        fetch("/authentication/authenticate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.username_error) {
                    usernameField.classList.add('is-invalid');
                    feedbackArea.style.display = "block";
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                    submitBtn.disabled = true;
                } else submitBtn.removeAttribute("disabled");
            });
    }
});