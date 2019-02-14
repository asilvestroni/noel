import axios, {AxiosPromise} from 'axios';

const progressBarElement = document.getElementById('session-progress-bar');
const statusElements = document.getElementsByClassName('session-status');
let bar: Element | null = null;
let percentage: Element | null = null;

async function updateProgress(sessionId: string) {
    const result = (await axios.get(`/sessions/${sessionId}/data`)) as {
        data:
            { progress: number, status: string, id: string }
    };

    const progress = result.data.progress;

    for (let i = 0; i < statusElements.length; i++) {
        const status = statusElements.item(i);
        if (status) {
            status.textContent = result.data.status;
        }
    }
    if (bar && percentage) {
        bar.style.width = `${progress}%`;
        percentage.innerText = progress;
    }
}

if (progressBarElement) {
    bar = progressBarElement.getElementsByClassName('bar')[0];
    percentage = progressBarElement.getElementsByClassName('percentage')[0];
    const attribute = progressBarElement.attributes.getNamedItem('data-session-id');

    const sessionId = attribute ? attribute.value : '';
    setInterval(updateProgress, 1000, sessionId);
}