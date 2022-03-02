var byId = function (id) {
    return document.getElementById(id);
};

let webhook_url = document.cookie
    .split("; ")
    .find((row) => row.startsWith("webhook_url"))
    .split("=")[1];

let webhook_username = byId("webhook_username"),
    webhook_avatar_url = byId("webhook_avatar_url"),
    webhook_message = byId("webhook_message"),
    webhook_file = byId("webhook_file"),
    avatar_preview = byId("avatar_preview"),
    open_avatar_preview = byId("open_avatar_preview"),
    error_message = byId("error_message"),
    show_selected_file = byId("show_selected_file");
submit_message = byId("submit_message");

function sendMessage() {
    if ((webhook_message.value != "") | (webhook_file.files.length != 0)) {
        var formData = new FormData();
        const request = new XMLHttpRequest();
        request.open("POST", webhook_url);
        formData.append("username", webhook_username.value);
        formData.append("avatar_url", webhook_avatar_url.value);
        formData.append("content", webhook_message.value);

        if (webhook_file.files.length > 0) {
            formData.append("file", webhook_file.files[0]);
        }

        request.send(formData);
        webhook_message.value = "";
        remove_selected_file();
        submit_message.innerHTML = "<b>Message Sent</b>";
        setTimeout(function () {
            submit_message.innerHTML = "";
        }, 3000);
    }
}

function show_avatar_preview() {
    if (webhook_avatar_url.value.length == 0) {
        avatar_preview.style.display = "none";
        error_message.style.display = "none";
    } else if (webhook_avatar_url.value.length != 0) {
        avatar_preview.style.display = "block";
        error_message.style.display = "none";
        avatar_preview.src = webhook_avatar_url.value;
        open_avatar_preview.href = webhook_avatar_url.value;
    }
}

function image_error() {
    avatar_preview.style.display = "none";
    error_message.innerHTML = "This File is Not Supported or The Link Is Broken";
    error_message.style.display = "block";
}

function show_selected_file_name() {
    show_selected_file.innerHTML = `File Selected: "${webhook_file.files.item(0).name}"`;
    show_selected_file.style.display = "block";
}

function remove_selected_file() {
    webhook_file.value = "";
    show_selected_file.innerHTML = "No File Selected";
    show_selected_file.style.display = "none";
}

function change_webhook() {
    document.cookie = "webhook_url=; Max-Age=0";

    submit_message.innerHTML = "<b>Discord Webhook Removed</b> &nbsp &nbsp &nbsp &nbsp Redirecting...";
    setTimeout(function () {
        window.location = "webhook_url.html";
    }, 1500);
}
