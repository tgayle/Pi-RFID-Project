var updateCardTimerId = 0;

function startUpdateTimer() {
    updateCardTimerId = setInterval(updateCardDetected, 250);
}

startUpdateTimer();

//Check if the window currently has focus and if it doesn't, stop updating the card reader. Due to limitations,
//the window has focus when it's technically visible. If this is the current tab and you Alt+Tab, it will continue
// updating, but if you switch tabs, then this will stop.
setInterval(function () {
    if (document.hidden) {
        clearInterval(updateCardTimerId);
        updateCardTimerId = 0;
    } else {
        if (updateCardTimerId === 0) {
            // startUpdateTimer();
        }
    }
}, 250);


