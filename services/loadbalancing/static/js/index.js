(function () {
    const loadingBar = document.getElementById("loading-bar");
    const audioBox = document.getElementById("result-audio");
    const textarea = document.getElementById("textmsg");
    const submitBtn = document.getElementById("submitbtn");
    const errorText = document.getElementById("error-field");
    submitBtn.addEventListener('click', () => {
        errorText.style.display = 'none';
        loadingBar.style.visibility = 'hidden';
        console.log('YOOOOO')
        let text = textarea.value;
        if (!text) {
            errorText.style.display = 'block';
            errorText.innerHTML = "No text entered. Can't synthesize.";
            return;
        }
        submitBtn.disabled = true;
        loadingBar.style.visibility = 'visible';

        let xhttp = new XMLHttpRequest();
        xhttp.open('POST', "http://localhost:5000/getspeech", true);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.responseType = 'blob';

        xhttp.onreadystatechange = (e) => {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var blob = new Blob([xhttp.response], { type: 'audio/wav' });
                var objectUrl = URL.createObjectURL(blob);
                audioBox.src = objectUrl;
                // Release resource when it's loaded
                audioBox.onload = function (evt) {
                    URL.revokeObjectURL(objectUrl);
                }

                loadingBar.style.visibility = 'hidden';
                audioBox.style.visibility = 'visible';
                submitBtn.disabled = false;
            }
            else if(xhttp.readyState==4){
                errorText.style.display = 'block';
                errorText.innerHTML = "Something went wrong. Server maybe down or unavailable.";
                submitBtn.disabled = false;
            }

        }

        xhttp.timeout = 100000;
        xhttp.send(JSON.stringify({ "text_message": text }));

    });

})();