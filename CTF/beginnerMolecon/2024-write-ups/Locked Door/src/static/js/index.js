const inputs = document.querySelectorAll('.digits input');
inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        if (input.value.length === 1 && index < inputs.length - 1) {
            inputs[index + 1].focus();
        }
    });
});

function clearDigits() {
    inputs.forEach(input => {
        input.value = '';
    });
    inputs[0].focus();
}