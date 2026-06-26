//Starts a 15 second timer for each question.
let timeLeft = 15;

const timerText = document.getElementById("timer");
const quizForm = document.getElementById("quiz-form");
const secondsLeftInput = document.getElementById("seconds-left");

//Run a second down each second
const timer = setInterval(function () {
    timeLeft = timeLeft - 1;
    timerText.textContent = timeLeft;

    //Save the current time in the hidden
    secondsLeftInput.value = timeLeft;

    //Submit the form automatically when time runs out
    //If no answer is sent, the player gets 0 points for that question
    if (timeLeft <= 0) {
        clearInterval(timer);
        secondsLeftInput.value = 0;
        quizForm.submit();
    }
}, 1000);

//Stop the countdown when the player clicks an answer button
quizForm.addEventListener("submit", function () {
    clearInterval(timer);

    //Makes sure we get the most recent number of seconds left
    secondsLeftInput.value = Math.max(0, timeLeft);
});
