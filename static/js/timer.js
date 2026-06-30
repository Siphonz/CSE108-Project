//Starts a 15 second timer for each question.
let timeLeft = 15;

const timerText = document.getElementById("timer");
const quizForm = document.getElementById("quiz-form");
const secondsLeftInput = document.getElementById("seconds-left");
const selectedAnswerInput = document.getElementById("selected-answer");

//Run a second down each second
const timer = setInterval(function () {
    timeLeft = timeLeft - 1;
    timerText.textContent = timeLeft;

    //Save the current time in the hidden input.
    secondsLeftInput.value = timeLeft;

    //Submit the form automatically when time runs out.
    //If no answer is sent, the player gets 0 points for that question.
    if (timeLeft <= 0) {
        clearInterval(timer);
        secondsLeftInput.value = 0;
        quizForm.submit();
    }
}, 1000);

quizForm.addEventListener("submit", function (e) {
    // Don't delay automatic timeout submission.
    if (!e.submitter) {
        clearInterval(timer);
        secondsLeftInput.value = 0;
        return;
    }

    clearInterval(timer);
    secondsLeftInput.value = Math.max(0, timeLeft);
    selectedAnswerInput.value = e.submitter.value;

    // Do not let the player select another answer before the form is sent.
    document.querySelectorAll(".answer").forEach(button => {
        button.disabled = true;
    });
});
