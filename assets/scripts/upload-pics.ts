const validExtensions = ['jpeg', 'jpg', 'gif', 'png'];

function checkFiles(input: HTMLInputElement) {
    return () => {
        if (selectButton && uploadButton) {
            const files = input.files ? input.files : [] as FileList;

            if (files.length < 10) {
                selectButton.textContent = 'Sono necessari almeno 10 file';
                uploadButton.disabled = true;
                return;
            }

            if (files.length > 30) {
                selectButton.textContent = 'Selezionare al massimo 30 file';
                uploadButton.disabled = true;
                return;
            }

            for (const file of files) {
                const ext = file.name.split('.').pop();
                if (validExtensions.indexOf(ext) < 0) {
                    selectButton.textContent = 'Estensione non valida';
                    uploadButton.disabled = true;
                    return;
                }
            }
            selectButton.textContent = files.length + ' file selezionati';
            uploadButton.disabled = false;
        }
    }
}

const input = document.getElementById('id_pics');
const uploadButton = document.getElementById('pics_upload');
const selectButton = document.getElementById('pics_select');

if (input) {
    input.onchange = checkFiles(input as HTMLInputElement);
}
