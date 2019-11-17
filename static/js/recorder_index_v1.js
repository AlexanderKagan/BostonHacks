//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recording_started = false;

var recordButton = document.getElementById("recordButton");
//var evalButton = document.getElementById("evalButton");


//add events to those 2 buttons
recordButton.addEventListener("click", recording);
//evalButton.addEventListener("click", evalRecording);

function recording() {
    var constraints = { audio: true, video:false };

    if (!recording_started) {
        recording_started = true;

        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
            audioContext = new AudioContext();

            gumStream = stream;
            input = audioContext.createMediaStreamSource(stream);
            rec = new Recorder(input, {numChannels:1});
            rec.record(); }).catch(function(err) {
               console.log("Recording was not allowed");
            })
        } else {
        recording_started = false;
        console.log("stop recording click");

        //tell the recorder to stop the recording
        rec.stop();

        //stop microphone access
        gumStream.getAudioTracks()[0].stop();

        //create the wav blob and pass it on to createDownloadLink
        rec.exportWAV(sendAudio);
    }
}

function sendAudio(blob) {
	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();
	var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
      if(this.readyState === 4) {
          console.log("Server returned: ",e.target.responseText);
      }
    };
    var fd=new FormData();
    fd.append("audio_data",blob, filename);
    xhr.open("POST","/recorder_receiver",true);
    xhr.send(fd);
}
