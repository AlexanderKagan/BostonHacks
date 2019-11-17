//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream;                      //stream from getUserMedia()
var rec;                            //Recorder.js object
var input;                          //MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recording_started = false;

var recordButton = document.getElementById("recordButton");
//var evalButton = document.getElementById("evalButton");

var startTime = null;
const secondsInMinute = 60;
const secondsInHour = 60 * 60;

var seconds = document.getElementById("seconds");
var minutes = document.getElementById("minutes");

var interval = null;

var state = {
    start: "START",
    pause: "PAUSE",
}

function changeState(st){
    switch (st) {
        case state.start:
            startTimer();
            break;
        case state.pause:
            stopTimer();
            break;
        default:
            throw new Error("Unknown state")
    }
    updateActionButton();
}

function getString(n) {
    if (n < 10) {
        return "0" + String(n);
    } else {
        return String(n);
    }
}

function setTime(h, m, s) {
    minutes.innerText = getString(m);
    seconds.innerText = getString(s);
}

function updateTime() {
    var diff = Math.floor((Date.now() - startTime) / 1000);
    var hours = Math.floor(diff / secondsInHour);
    diff = diff - hours * secondsInHour;
    var minutes = Math.floor(diff / secondsInMinute);
    diff = diff - minutes * secondsInMinute;
    var seconds = diff;
    setTime(hours, minutes, seconds);
}

function getOffset(){
    var s = Number(seconds.innerText, 10);
    var m = Number(minutes.innerText, 10);
    var offset = m*secondsInMinute + s;
    var offsetInMs = offset * 1000;
    return offsetInMs;
}

function getStartTime() {
    var offset = getOffset();
    var now = Date.now();
    var sTime = now - offset;
    return sTime;
}

function resetTime(){
    seconds.innerHTML = "00";
    minutes.innerHTML = "00";
}

function startTimer() {
    startTime = getStartTime();
    interval = setInterval(updateTime, 100);
}

function updateActionButton(){
    if (interval){
        recordButton.innerText = "Stop";
    } else {
        recordButton.innerText = "Record";
    }
}

function stopTimer(){
    clearInterval(interval);
    interval = null;
    resetTime();
    updateActionButton();
}


//add events to those 2 buttons
recordButton.addEventListener("click", recording);
//evalButton.addEventListener("click", evalRecording);

function recording() {
    var constraints = { audio: true, video:false };

    console.log(recording_started);
    if (!recording_started) {
        console.log('start recording!!!!!')
        recording_started = true;

        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            if(interval){
                changeState(state.pause);
            } else {
                changeState(state.start);
            }
            console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
            audioContext = new AudioContext();

            gumStream = stream;
            input = audioContext.createMediaStreamSource(stream);
            rec = new Recorder(input, {numChannels:1});
            rec.record(); }).catch(function(err) {
               console.log("Recording was not allowed");
            });
    } else {
        recording_started = false;
        console.log("stop recording click");

        //tell the recorder to stop the recording
        stopTimer();
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
          console.log("What server sent to me");
          var response = JSON.parse(e.target.response);
          console.log(response);
      }
    };
    var fd=new FormData();
    fd.append("audio_data",blob, filename);
    xhr.open("POST","/recorder_receiver",true);
    xhr.send(fd);
}
