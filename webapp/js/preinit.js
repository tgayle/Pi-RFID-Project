const findCardBtn = $("#lookforcard");
const cardIDText = $("#card_found_p");
const waitingForCard = $("#waiting_for_card");
const request_console = $("#command_output");
const cardOptionsDiv = $("#cardopts");
const navBarCardInfo = $("#navbar_card_status");

const ERROR_CARD = "Error connecting to reader.";
const NO_CARD_DET = "No card detected...";
var lastConsoleMessage = "";
var currentCardOnScanner;
var safeCardId;
var currentCardName;

//https://stackoverflow.com/questions/1144783/how-to-replace-all-occurrences-of-a-string-in-javascript
function replaceAll(str, search, replacement) {
    str = str.split(search);
    return str.join(replacement);
}

function formDateFromTimestamp(dateInstance) {
    const month = dateInstance.getMonth() + 1 + "";
    const day = dateInstance.getDate() + "";
    const year = dateInstance.getYear() + 1900 + "";

    const date = month.padStart(2, "0") + "-" + day.padStart(2, "0") + "-" + year.padStart(4, "0");

    const hour = dateInstance.getHours() + "";
    const minutes = dateInstance.getMinutes() + "";
    const seconds = dateInstance.getSeconds() + "";

    const time = hour.padStart(2, "0") + ":" + minutes.padStart(2, "0") + ":" + seconds.padStart(2, "0");
    return date + " " + time;
}

/**
 * Prints to the on screen log but only if forceLog is true or the previous message
 * printed is not the same as the current.
 * @param str Message to print.
 * @param forceLog: optionaltrue to print regardless of whether the last message was the same
 */
function addToTextConsole(str, forceLog) {
    forceLog = forceLog || false;

    if (forceLog || str !== lastConsoleMessage) {
        var message = formDateFromTimestamp(new Date()) + ": " + str;
        // request_console.html(request_console.html() + message + "<br>");
        request_console.append(formDateFromTimestamp(new Date()) + " ");
        request_console.append(str);
        request_console.append("<br>");
        console.log(message);
        lastConsoleMessage = str;

        request_console.scrollTop = request_console.scrollHeight;
        //TODO: Keep console scrolled to bottom.
    }
}

function changeElementTitle(element, newTitle) {
    element.prop("title", newTitle);
}

var onFailure = function () {
    if (waitingForCard.html() !== ERROR_CARD) {
        waitingForCard.html(ERROR_CARD);
        addToTextConsole(ERROR_CARD, true);
    }
};

function updateCardDetected() {
    $.get("htmlapi/ping_for_card", function (response) {
        if (response.length === 0) {
            onFailure();
            return;
        }
        const jsonRsp = response;

        if (jsonRsp.uid !== null) {
            cardOptionsDiv.toggle(true);
            var cardName = (jsonRsp.name === null) ? "Unnamed Card" : jsonRsp.name;
            var cardText = jsonRsp.uid + " (" + cardName + ")";

            cardIDText.html("Card found!");
            cardOptionsDiv.toggle(true);

            addToTextConsole("Card found: " + cardText);
            changeElementTitle(navBarCardInfo, "ID: " + jsonRsp.uid);
            navBarCardInfo.html("Editing: " + cardName);
            waitingForCard.html(cardText);
            currentCardOnScanner = jsonRsp.uid;
            safeCardId = replaceAll(currentCardOnScanner, " ", "");
            currentCardName = cardName;
        } else {
            currentCardOnScanner = null;
            safeCardId = null;
            currentCardName = null;
            cardIDText.html(NO_CARD_DET);
            navBarCardInfo.html(NO_CARD_DET);
            changeElementTitle(navBarCardInfo, "");
            waitingForCard.html("Waiting...")
        }

    }).fail(onFailure);
}