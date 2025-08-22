
async function onLoginPageLoad() {
    const submit_button = document.getElementById("sign-in-btn");
    submit_button.addEventListener("click", async (e) => {
        const email_id_field = document.getElementById("email-field");
        const password_field = document.getElementById("password-field");
        const email_id = email_id_field.value;
        const password = password_field.value;
        if ((!email_id) || (!password)) {
            alert("Email or Password Field is Empty!");
            return;
        }
        const res = await login(email_id, password);
        if (!res.ok) {
            let json_data = await res.json();
            // alert(`Error while logging-in: ${json_data.error}`);
            return;
        }
        let json_data = await res.json();
        const access_token = json_data.access_token; 
        const refresh_token = json_data.refresh_token;
        localStorage.setItem("spm_access_token", access_token);
        localStorage.setItem("spm_refresh_token", refresh_token);
        console.log(access_token);
        console.log(refresh_token);
        window.location.href = "/kanban-board";
        // alert(`Message: ${json_data.message}`);
        
    });
}



async function login(email_id, password) {
    let res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            email_id: email_id,
            password: password
        }),
        credentials: "include"
    });
    return res;
}

onLoginPageLoad();