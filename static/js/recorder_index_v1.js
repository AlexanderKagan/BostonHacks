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
          var response = JSON.parse(e.target.response);
          console.log(response);

          $("#character_img").attr("src", response['who_do_you_look_like']['url']);
          $("#character_name").text(response['who_do_you_look_like']['name']);

          var clarity = response['clarity'];
          if (clarity <= 5) {
            $("#clarity").text("Your clarity is below average - " + response['clarity'] + ". You need to improve it by reading books and practising every day");
          }
          if (clarity == 6) {
            $("#clarity").text("Score " + response['clarity'] + " is a great place to start. Keep practising!");
          }
          if (clarity == 7) {
            $("#clarity").text("You are almost here! " + response['clarity'] + " is usually enough to pass any exam or test. But perfectness has no limits");
          }

          if (clarity >= 8) {
            $("#clarity").text("You are just awesome. In case you want to grow further, you need to take an exam. " + response['clarity'] + " is almost maximum.");
          }

          $("#tone").text(response['tone'] + " /10");
          $("#engagement").text(response['engagement'] + " /10");

          var diversity = response['diversity'];
          if (diversity <= 5) {
               $("#diversity").text('Diversity shows your vocabulary range, ability to use advanced words and expressions. ' + response['diversity'] + " is not bad, but definitely you can become better!");
          }

          if (diversity == 6) {
               $("#diversity").text("You are on the right way! " + response['diversity'] + " is good, but not perfect. Check out our exercises to become stronger!");
          }

          if (diversity == 7) {
               $("#diversity").text("Wow! " + response['diversity'] + " is above the average! You are cool!");
          }

          if (diversity == 8) {
               $("#diversity").text("Just near the final line! One more point...");
          }

          if (diversity == 9) {
               $("#diversity").text("You are just perfect! Absolutely. Completely. " + response['diversity'] + " out of 9");
          }

          var calmness = response['calmness'];

          if (calmness <= 5) {
               $("#calmness").text("It seems like your are feeling worry to much and can not be fluent and direct when speaking. For now " + response['calmness'] + " out of 10.");
          }

          if (calmness == 6) {
               $("#calmness").text("Yor are on the right way and become calmer with each exercise. Still you need to take care of your speed. For now " + response['calmness'] + "out of 10.");
          }

          if (calmness == 7) {
               $("#calmness").text("Close to be perfect: you know how to track your speed almost during whole speech but start rushing a lot in between. For noe " + response['calmness'] + " out of 10.");
          }

          if (calmness == 8) {
               $("#calmness").text("Great! Nothing to add, just great! " + response['calmness'] + "/10");
          }

          if (calmness == 9) {
               $("#calmness").text("You are awesome! Absolutely. Perfectly. " + response['calmness'] / "10");
          }
          $('.statistics').show();
      }
    };
    var fd=new FormData();
    fd.append("audio_data",blob, filename);
    xhr.open("POST","/recorder_receiver",true);
    xhr.send(fd);
}
