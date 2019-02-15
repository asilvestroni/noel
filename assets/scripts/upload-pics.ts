import * as FilePond from 'filepond';

const filepondWrapper = document.getElementById('filepond-wrapper');
const uploadButton: HTMLButtonElement | null = document.getElementById('pics_upload') as HTMLButtonElement;

// const validExtensions = ['jpeg', 'jpg', 'gif', 'png'];
//
// function checkFiles(input: HTMLInputElement) {
//     return () => {
//         if (selectButton && uploadButton) {
//             const files = input.files ? input.files : [] as FileList;
//
//             if (files.length < 10) {
//                 selectButton.textContent = 'Sono necessari almeno 10 file';
//                 uploadButton.disabled = true;
//                 return;
//             }
//
//             if (files.length > 30) {
//                 selectButton.textContent = 'Selezionare al massimo 30 file';
//                 uploadButton.disabled = true;
//                 return;
//             }
//
//             for (const file of files) {
//                 const ext = file.name.split('.').pop();
//                 if (validExtensions.indexOf(ext) < 0) {
//                     selectButton.textContent = 'Estensione non valida';
//                     uploadButton.disabled = true;
//                     return;
//                 }
//             }
//             selectButton.textContent = files.length + ' file selezionati';
//             uploadButton.disabled = false;
//         }
//     }
// }

// const selectButton = document.getElementById('pics_select');
// const input = document.getElementById('id_pics');

// if (input) {
//      input.onchange = checkFiles(input as HTMLInputElement);
// }
let pond: any = null;

function beforeAddFileHandler(item: any) {
    const files = pond.getFiles();
    const file = files.find((file: any) => (file.filename === item.filename) && (file.id !== item.id));
    return !!!file;
}

function beforeRemoveFileHandler(item: any) {
}

function setButtonState(state: boolean) {
    uploadButton!.disabled = state;
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
    pond = FilePond.create({
        allowMultiple: true,
        allowRevert: false,
        maxFiles: 30,
        required: true,
        maxParallelUploads: 3,
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
        }
    });
    pond.beforeAddFile = beforeAddFileHandler;
    pond.beforeRemoveFile = beforeRemoveFileHandler;
    pond.on('addfile', addFileHandler);
    pond.on('removefile', removeFileHandler);

    filepondWrapper.appendChild(pond.element);
    uploadButton!.addEventListener('click', async () => {
        await pond.processFiles();
    });
}
