$(document).ready(function() {
    var btn = $(".button");
    btn.click(function() {
      btn.toggleClass("paused");
      return false;
    });
});

var btn = document.getElementById("music1");

function toggleMusic() {
    if (btn.paused) {
        btn.play();
    } else {
        btn.pause();
    }
}



