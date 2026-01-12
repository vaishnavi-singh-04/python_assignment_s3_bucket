// const API = "http://localhost:8000/s3";
// const output = document.getElementById("output");

// function show(data) {
//     output.textContent = JSON.stringify(data, null, 2);
// }

// // BUCKET
// async function listBuckets() {
//     const res = await fetch(`${API}/buckets`);
//     show(await res.json());
// }

// async function createBucket() {
//     const name = document.getElementById("createBucketName").value;
//     const res = await fetch(`${API}/create-bucket`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ bucket_name: name, region: "us-east-1" })
//     });
//     show(await res.json());
// }

// async function deleteBucket() {
//     const name = document.getElementById("deleteBucketName").value;
//     const res = await fetch(`${API}/bucket/${name}`, { method: "DELETE" });
//     show(await res.json());
// }

// // FOLDER
// async function createFolder() {
//     const bucket = document.getElementById("folderBucket").value;
//     const folder = document.getElementById("folderName").value;

//     const res = await fetch(`${API}/create-folder`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ bucket_name: bucket, folder_name: folder })
//     });
//     show(await res.json());
// }

// // FILE
// async function uploadFile() {
//     const bucket = document.getElementById("uploadBucket").value;
//     const folder = document.getElementById("uploadFolder").value;
//     const file = document.getElementById("fileInput").files[0];

//     const fd = new FormData();
//     fd.append("file", file);
//     if (folder) fd.append("folder_name", folder);

//     const res = await fetch(`${API}/upload-file/${bucket}`, {
//         method: "POST",
//         body: fd
//     });
//     show(await res.json());
// }

// async function deleteFile() {
//     const bucket = document.getElementById("deleteFileBucket").value;
//     const file = document.getElementById("deleteFileName").value;
//     const folder = document.getElementById("deleteFileFolder").value;

//     const url = new URL(`${API}/delete-file/${bucket}`);
//     url.searchParams.append("file_name", file);
//     if (folder) url.searchParams.append("folder_name", folder);

//     const res = await fetch(url, { method: "DELETE" });
//     show(await res.json());
// }

// // COPY / MOVE
// async function copyFile() { await copyMove("copy-file"); }
// async function moveFile() { await copyMove("move-file"); }

// async function copyMove(endpoint) {
//     const payload = {
//         bucket_name: document.getElementById("cmBucket").value,
//         file_name: document.getElementById("cmFile").value,
//         source_folder: document.getElementById("cmSource").value,
//         destination_folder: document.getElementById("cmDest").value
//     };

//     const res = await fetch(`${API}/${endpoint}`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify(payload)
//     });
//     show(await res.json());
// }


const API = "http://localhost:8000/s3";
const output = document.getElementById("output");

// Utility to display response safely
async function showResponse(res) {
    try {
        const data = await res.json(); // try parse JSON
        output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        // fallback to plain text or status
        const text = await res.text();
        output.textContent = text || `Status: ${res.status}`;
    }
}

// --- BUCKET OPERATIONS ---
async function listBuckets() {
    const res = await fetch(`${API}/buckets`);
    await showResponse(res);
}

async function createBucket() {
    const name = document.getElementById("createBucketName").value;
    const res = await fetch(`${API}/create-bucket`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bucket_name: name, region: "us-east-1" })
    });
    await showResponse(res);
}

async function deleteBucket() {
    const name = document.getElementById("deleteBucketName").value;
    const res = await fetch(`${API}/bucket/${name}`, { method: "DELETE" });
    await showResponse(res);
}

// --- FOLDER OPERATIONS ---
async function createFolder() {
    const bucket = document.getElementById("folderBucket").value;
    const folder = document.getElementById("folderName").value;

    const res = await fetch(`${API}/create-folder`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bucket_name: bucket, folder_name: folder })
    });
    await showResponse(res);
}

async function deleteFolder() {
    const bucket = document.getElementById("deleteFolderBucket").value;
    const folder = document.getElementById("deleteFolderName").value;

    const res = await fetch(`${API}/delete-folder`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bucket_name: bucket, folder_name: folder })
    });
    await showResponse(res);
}

// --- FILE OPERATIONS ---
async function uploadFile() {
    const bucket = document.getElementById("uploadBucket").value;
    const folder = document.getElementById("uploadFolder").value;
    const file = document.getElementById("fileInput").files[0];

    if (!file) {
        output.textContent = "Please select a file to upload";
        return;
    }

    const fd = new FormData();
    fd.append("file", file);
    if (folder) fd.append("folder_name", folder);

    const res = await fetch(`${API}/upload-file/${bucket}`, {
        method: "POST",
        body: fd
    });
    await showResponse(res);
}

async function deleteFile() {
    const bucket = document.getElementById("deleteFileBucket").value;
    const file = document.getElementById("deleteFileName").value;
    const folder = document.getElementById("deleteFileFolder").value;

    const url = new URL(`${API}/delete-file/${bucket}`);
    url.searchParams.append("file_name", file);
    if (folder) url.searchParams.append("folder_name", folder);

    const res = await fetch(url, { method: "DELETE" });
    await showResponse(res);
}

// --- COPY / MOVE FILE ---
async function copyFile() {
    await copyMove("copy-file");
}

async function moveFile() {
    await copyMove("move-file");
}

async function copyMove(endpoint) {
    const payload = {
        bucket_name: document.getElementById("cmBucket").value,
        file_name: document.getElementById("cmFile").value,
        source_folder: document.getElementById("cmSource").value,
        destination_folder: document.getElementById("cmDest").value,
    };

    const res = await fetch(`${API}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    await showResponse(res);
}
