const questions = document.querySelectorAll('.question');
const modal = document.querySelector('.modal');
let currentQuestionIndex = 0;

document.addEventListener('DOMContentLoaded', function() {
    showCurrentQuestion();
    initializeModalHandlers();
});

function showCurrentQuestion() {
    questions.forEach((question, index) => {
        question.style.display = index === currentQuestionIndex ? 'block' : 'none';
    });
}
function nextQuestion() {
    if (validateCurrentQuestion()) {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            showCurrentQuestion();
        } else {
            showCompletionModal();
        }
    }
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showCurrentQuestion();
    }
}

function validateCurrentQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    const requiredInputs = currentQuestion.querySelectorAll('input[required], select[required], textarea[required]');
    
    let isValid = true;
    requiredInputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            highlightInvalidInput(input);
        } else {
            removeInvalidHighlight(input);
        }
    });
    
    return isValid;
}

function highlightInvalidInput(input) {
    input.style.borderColor = 'var(--google-red)';
    const errorMessage = input.parentElement.querySelector('.error-message');
    if (!errorMessage) {
        const message = document.createElement('div');
        message.className = 'error-message';
        message.style.color = 'var(--google-red)';
        message.style.fontSize = '0.875rem';
        message.style.marginTop = '-0.5rem';
        message.style.marginBottom = '0.5rem';
        message.textContent = 'This field is required';
        input.parentElement.insertBefore(message, input.nextSibling);
    }
}

function removeInvalidHighlight(input) {
    input.style.borderColor = '';
    const errorMessage = input.parentElement.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

function initializeModalHandlers() {
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    };
}

function showCompletionModal() {
    modal.style.display = 'block';
}

function closeModal() {
    modal.style.display = 'none';
}

function submitForm() {

    console.log('Form submitted!');
    closeModal();
}
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.hasAttribute('required')) {
                if (this.value.trim()) {
                    removeInvalidHighlight(this);
                } else {
                    highlightInvalidInput(this);
                }
            }
        });
    });
});