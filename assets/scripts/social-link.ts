import axios from "axios";

function allowSessionProcessing(sesId: string) {
    const btn = document.getElementById('start-button');
    btn.addEventListener('click', function () {
        window.location = "/sessions/" + sesId
    });
    btn.disabled = false
    btn.classList.remove('cursor-not-allowed');
}

async function saveToken(response: { authResponse: { accessToken: string } }) {
    const token = response.authResponse.accessToken ? response.authResponse.accessToken : false;
    if (!token) return;
    const csrf: string = (document.getElementsByName("csrfmiddlewaretoken")[0] as HTMLInputElement).value;
    const result = await axios.put('/socials/fb_token', {}, {params: {token}, headers: {'X-CSRFToken': csrf}});
    if (result.data) {
        allowSessionProcessing(result.data);
    }
}

window.saveToken = saveToken;
