document.addEventListener('DOMContentLoaded', (event) => {
    let responses = {};

    // Event listener for selecting answers
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', (event) => {
            let question = event.target.getAttribute('data-question');
            let answer = event.target.getAttribute('data-answer');
            responses[question] = answer;

            // Remove 'selected' class from all buttons in the current question and add it to the clicked button
            document.querySelectorAll(`#${question} .btn`).forEach(btn => btn.classList.remove('selected'));
            event.target.classList.add('selected');
        });
    });

    // Function to proceed to the next question
    window.nextQuestion = function(current) {
        if (current === 1) { // Check if it's the first question
            let name = document.getElementById('input-name').value.trim();
            if (name) {
                responses[`question${current}`] = name;
                localStorage.setItem(`question${current}`, name);
                document.getElementById(`question${current}`).classList.remove('active');
                document.getElementById(`question${current + 1}`).classList.add('active');
            } else {
                alert('Please enter your name before proceeding.');
            }
        } else { // For other questions, check if the current question is answered
            if (responses[`question${current}`]) {
                localStorage.setItem(`question${current}`, responses[`question${current}`]);
                document.getElementById(`question${current}`).classList.remove('active');
                document.getElementById(`question${current + 1}`).classList.add('active');
            } else {
                alert('Please select an answer before proceeding.');
            }
        }
    }

    // Function to go back to the previous question
    window.previousQuestion = function(current) {
        document.getElementById(`question${current}`).classList.remove('active');
        document.getElementById(`question${current - 1}`).classList.add('active');
    }

    // Function to submit the survey
    window.submitSurvey = function() {
        // Check if all questions are answered before submitting
        if (responses['question1'] && responses['question2'] && responses['question3'] &&
            responses['question4'] && responses['question5']) {
            
            // Prepare data for submission
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
                    // Hide all questions and show the thank you message
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
            alert('Please answer all questions before submitting.');
        }
    }
});
