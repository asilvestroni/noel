import axios, {AxiosPromise} from 'axios';

const progressBarElement = document.getElementById('session-progress-bar');
const statusElements = document.getElementsByClassName('session-status');
const loadingIndicators = document.getElementsByClassName('loading-indicator');
const cardPics = document.getElementsByClassName('card-pic');

let bar: Element | null = null;
let percentage: Element | null = null;

function findCardPic(givenId: number): Element | null {
    for (const id in cardPics) {
        const cardId = parseInt(cardPics[id].getAttribute('data-picture-id') || '-1');
        if (cardId === givenId) {
            return cardPics[id];
        }
    }
    return null;
}

function setAsLoading(value: boolean) {
    for (let i = 0; i < loadingIndicators.length; i++) {
        const indicator = loadingIndicators[i];
        if (value) {
            indicator.classList.add('loading');
        } else {
            indicator.classList.remove('loading');
        }
    }
}

async function updateProgress(sessionId: string) {
    setAsLoading(true);
    const result = (await axios.get(`/sessions/${sessionId}/data`)) as {
        data:
            { progress: number, status: string, id: string, pictures: { [k: number]: { id: number, status: string, data: string } } }
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
        percentage.innerText = progress.toFixed(0);
        if (progress < 100) {
            bar.classList.add('animate');
        } else {
            bar.classList.remove('animate');
        }
    }

    for (const id in result.data.pictures) {
        const pic = findCardPic(parseInt(id));
        if (pic) {
            const id = parseInt(pic.getAttribute('data-picture-id') || '0');
            const img = pic.getElementsByTagName('img')[0];
            const newData = result.data.pictures[id].data;
            const statusIndicator = pic.getElementsByClassName('card-pic-status-indicator')[0];

            if (img.src !== newData) {
                img.src = newData;
                let statusClass = 'bg-transparent';
                switch (result.data.pictures[id].status) {
                    case 'extracted':
                        statusClass = 'bg-success';
                        break;
                    case 'processing':
                        statusClass = 'bg-warning';
                        break;
                    case 'error':
                        statusClass = 'bg-alert';
                        break;
                    default:
                        statusClass = 'bg-transparent';
                }
                statusIndicator.classList.remove('bg-success', 'bg-alert', 'bg-warning', 'bg-transparent');
                statusIndicator.classList.add(statusClass);
            }
        }
    }

    setTimeout(() => {
        setAsLoading(false);
    }, 1000);
}

if (progressBarElement) {
    bar = progressBarElement.getElementsByClassName('bar')[0];
    percentage = progressBarElement.getElementsByClassName('percentage')[0];
    const attribute = progressBarElement.attributes.getNamedItem('data-session-id');

    const sessionId = attribute ? attribute.value : '';
    setInterval(updateProgress, 3000, sessionId);
}