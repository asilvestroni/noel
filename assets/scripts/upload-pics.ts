import * as FilePond from 'filepond';
import FilePondPluginImageTransform from 'filepond-plugin-image-transform';
import FilePondPluginImageResize from 'filepond-plugin-image-resize';

const filepondWrapper = document.getElementById('filepond-wrapper');
const uploadButton: HTMLButtonElement | null = document.getElementById('pics_upload') as HTMLButtonElement;

let pond: any = null;

function beforeAddFileHandler(item: any) {
    const files = pond.getFiles();
    const file = files.find((file: any) => (file.filename === item.filename) && (file.id !== item.id));
    return !!!file;
}

function beforeRemoveFileHandler(item: any) {
}

function setButtonState(state: boolean) {
    uploadButton!.disabled = !state;
    if (state) {
        uploadButton!.classList.remove('disabled');
    } else {
        uploadButton!.classList.add('disabled');
    }
}

function updateButtonState() {
    const count = pond.getFiles().length;
    setButtonState(count > 10);
}

function addFileHandler() {
    updateButtonState();
}

function removeFileHandler() {
    updateButtonState();
}

if (filepondWrapper) {
    FilePond.registerPlugin(FilePondPluginImageResize);
    FilePond.registerPlugin(FilePondPluginImageTransform);
    pond = FilePond.create({
        allowMultiple: true,
        allowRevert: false,
        maxFiles: 30,
        required: true,
        maxParallelUploads: 5,
        name: 'filepond',
        instantUpload: false,
        server: {
            process: {
                url: '/manage-pics/',
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.$csrf,
                },
                timeout: 7000
            },
            fetch: null,
            revert: null,
        },
        labelIdle: 'Trascina qui le tue foto oppure <span class="filepond--label-action"> Sfoglia </span>',
        imageResizeTargetWidth: 1024,
        imageResizeTargetHeight: 1024,
    });
    pond.beforeAddFile = beforeAddFileHandler;
    pond.beforeRemoveFile = beforeRemoveFileHandler;
    pond.on('addfile', addFileHandler);
    pond.on('removefile', removeFileHandler);

    filepondWrapper.appendChild(pond.element);
    uploadButton!.addEventListener('click', async () => {
        setButtonState(false);
        filepondWrapper.classList.add('drop-disabled');
        pond.allowDrop = false;
        pond.allowPaste = false;
        await pond.processFiles();
        window.location.href = '/socials'
    });
}
