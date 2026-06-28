//Starts a 15 second timer for each question.
let timeLeft = 15;

const timerText = document.getElementById("timer");
const quizForm = document.getElementById("quiz-form");
const secondsLeftInput = document.getElementById("seconds-left");

const selectedAnswerInput = document.getElementById("selected-answer");
const correctSound = document.getElementById("correctSFX");
const wrongSound = document.getElementById("incorrectSFX");

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

quizForm.addEventListener("submit", function (e) {

    // Don't delay automatic timeout submission.
    if (!e.submitter) {
        clearInterval(timer);
        secondsLeftInput.value = 0;
        return;
    }

    e.preventDefault();

    clearInterval(timer);
    secondsLeftInput.value = Math.max(0, timeLeft);

    selectedAnswerInput.value = e.submitter.value;

    document.querySelectorAll(".answer").forEach(button => {
        button.disabled = true;
    });

    const chosenAnswer = e.submitter.value;
    const correctAnswer = quizForm.dataset.correct;

    if (chosenAnswer === correctAnswer) {
        correctSound.play();
    } else {
        wrongSound.play();
    }

    setTimeout(() => {
        quizForm.submit();
    }, 1000);
});
