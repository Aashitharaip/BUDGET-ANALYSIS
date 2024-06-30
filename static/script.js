document.addEventListener('DOMContentLoaded', (event) => {
    let responses = {};

    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', (event) => {
            let question = event.target.getAttribute('data-question');
            let answer = event.target.getAttribute('data-answer');
            responses[question] = answer;

            document.querySelectorAll(`#${question} .btn`).forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
        });
    });

    window.nextQuestion = function(current) {
        if (responses[`question${current}`]) {
            localStorage.setItem(`question${current}`, responses[`question${current}`]);
            document.getElementById(`question${current}`).classList.remove('active');
            document.getElementById(`question${current + 1}`).classList.add('active');
        } else {
            alert('Please select an answer before proceeding.');
        }
    }

    window.previousQuestion = function(current) {
        document.getElementById(`question${current}`).classList.remove('active');
        document.getElementById(`question${current - 1}`).classList.add('active');
    }

    window.submitSurvey = function() {
        if (responses[`question4`]) {
            localStorage.setItem(`question4`, responses[`question4`]);
            document.querySelectorAll('.question').forEach(q => q.classList.remove('active'));
            document.getElementById('thankyou').style.display = 'block';
        } else {
            alert('Please select an answer before submitting.');
        }
    }
});
