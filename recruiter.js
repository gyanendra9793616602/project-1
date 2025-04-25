let scannerActive = false;
const html5QrCode = new Html5Qrcode("qr-reader");

function toggleQRScanner() {
    if (scannerActive) {
        stopScanner();
    } else {
        startScanner();
    }
}

function startScanner() {
    document.getElementById("qr-reader").style.display = "block";
    html5QrCode.start(
        { facingMode: "environment" },
        {
            fps: 10,
            qrbox: { width: 250, height: 250 }
        },
        (decodedText) => {
            document.getElementById("searchInput").value = decodedText;
            stopScanner();
            performSearch(decodedText);
        },
        (errorMessage) => {
            console.warn(`QR Code scanning error: ${errorMessage}`);
        }
    ).catch((err) => {
        console.error(`Unable to start QR scanner: ${err}`);
    });
    scannerActive = true;
}

function stopScanner() {
    html5QrCode.stop().then(() => {
        document.getElementById("qr-reader").style.display = "none";
        scannerActive = false;
    }).catch((err) => {
        console.error(`Unable to stop QR scanner: ${err}`);
    });
}

function performSearch(query) {
    if (query) {
        window.location.href = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
    }
}

document.getElementById("searchInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        performSearch(e.target.value);
    }
});