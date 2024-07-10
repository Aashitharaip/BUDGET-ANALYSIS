document.addEventListener('DOMContentLoaded', (event) => {
    let responses = {};

    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', (event) => {
            let question = event.target.getAttribute('data-question');
            let answer = event.target.getAttribute('data-answer');
            responses[question] = answer;

            document.querySelectorAll(`#${question} .btn`).forEach(btn => btn.classList.remove('selected'));
            event.target.classList.add('selected');
        });
    });

    window.nextQuestion = function(current) {
        if (current === 1) {
            let name = document.getElementById('input-name').value;
            if (name) {
                responses[`question${current}`] = name;
                localStorage.setItem(`question${current}`, name);
                document.getElementById(`question${current}`).classList.remove('active');
                document.getElementById(`question${current + 1}`).classList.add('active');
            } else {
                alert('Please enter your name before proceeding.');
            }
        } else {
            if (responses[`question${current}`]) {
                localStorage.setItem(`question${current}`, responses[`question${current}`]);
                document.getElementById(`question${current}`).classList.remove('active');
                document.getElementById(`question${current + 1}`).classList.add('active');
            } else {
                alert('Please select an answer before proceeding.');
            }
        }
    }

    window.previousQuestion = function(current) {
        document.getElementById(`question${current}`).classList.remove('active');
        document.getElementById(`question${current - 1}`).classList.add('active');
    }

    window.submitSurvey = function() {
        if (responses[`question5`]) {
            localStorage.setItem(`question5`, responses[`question5`]);
            fetch('/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: responses['question1'],
                    spendOn: responses['question2'],
                    homeStatus: responses['question3'],
                    sneakyExpenses: responses['question4'],
                    debt: responses['question5']
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    document.querySelectorAll('.question').forEach(q => q.classList.remove('active'));
                    document.getElementById('thankyou').style.display = 'block';
                } else {
                    alert('There was an error submitting the survey.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('There was an error submitting the survey.');
            });
        } else {
            alert('Please select an answer before submitting.');
        }
    }
});
