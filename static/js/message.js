document.addEventListener("DOMContentLoaded", function () {
  var msg = document.getElementById("message");
  var timer;
  function startFadeOut() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      msg.style.opacity = "0";
      msg.style.height = "0";
      setTimeout(() => {
        msg.style.display = "none";
        console.log("Done");
      }, 500);
    }, 2000);
  }

  msg.addEventListener("pointerover", function () {
    clearTimeout(timer);
    msg.style.display = "block";
    msg.style.opacity = "1";
    msg.style.height = "auto"; // Ensure the element is shown
    console.log("pointerover");
  });
  msg.addEventListener("pointerleave", function () {
    console.log("pointerleave");
    startFadeOut();
  });
  startFadeOut();
});
