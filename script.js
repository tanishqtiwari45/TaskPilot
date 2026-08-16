let display = document.getElementById('display');
let currentValue = '';
let previousValue = '';
let operation = null;
let shouldResetDisplay = false;

function appendNumber(number) {
    if (shouldResetDisplay) {
        currentValue = number;
        shouldResetDisplay = false;
    } else {
        // Prevent multiple decimal points
        if (number === '.' && currentValue.includes('.')) {
            return;
        }
        // Prevent leading zero (except for 0.)
        if (currentValue === '0' && number !== '.') {
            currentValue = number;
        } else {
            currentValue += number;
        }
    }
    updateDisplay();
}

function appendOperator(op) {
    if (currentValue === '') {
        return;
    }

    if (previousValue !== '' && operation && !shouldResetDisplay) {
        calculate();
    }

    previousValue = currentValue;
    operation = op;
    shouldResetDisplay = true;
}

function calculate() {
    if (operation === null || previousValue === '' || currentValue === '') {
        return;
    }

    let result;
    const prev = parseFloat(previousValue);
    const current = parseFloat(currentValue);

    switch (operation) {
        case '+':
            result = prev + current;
            break;
        case '-':
            result = prev - current;
            break;
        case '*':
            result = prev * current;
            break;
        case '/':
            if (current === 0) {
                alert('Cannot divide by zero');
                clearDisplay();
                return;
            }
            result = prev / current;
            break;
        case '%':
            result = prev % current;
            break;
        case '^':
            result = Math.pow(prev, current);
            break;
        default:
            return;
    }

    // Round to avoid floating point errors
    result = Math.round(result * 100000000) / 100000000;

    currentValue = result.toString();
    operation = null;
    previousValue = '';
    shouldResetDisplay = true;
    updateDisplay();
}

function clearDisplay() {
    currentValue = '';
    previousValue = '';
    operation = null;
    shouldResetDisplay = false;
    updateDisplay();
}

function deleteLast() {
    currentValue = currentValue.toString().slice(0, -1);
    updateDisplay();
}

// Advanced operations
function squareRoot() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    if (num < 0) {
        alert('Cannot calculate square root of negative number');
        return;
    }
    currentValue = Math.sqrt(num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function square() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    currentValue = (num * num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function cube() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    currentValue = (num * num * num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function power() {
    if (currentValue === '') {
        return;
    }
    previousValue = currentValue;
    operation = '^';
    shouldResetDisplay = true;
}

function reciprocal() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    if (num === 0) {
        alert('Cannot calculate reciprocal of zero');
        return;
    }
    currentValue = (1 / num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function factorial() {
    if (currentValue === '') {
        return;
    }
    const num = parseInt(currentValue);
    if (num < 0) {
        alert('Cannot calculate factorial of negative number');
        return;
    }
    if (!Number.isInteger(num)) {
        alert('Factorial only works with integers');
        return;
    }
    let result = 1;
    for (let i = 2; i <= num; i++) {
        result *= i;
    }
    currentValue = result.toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function naturalLog() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    if (num <= 0) {
        alert('Logarithm of non-positive number is undefined');
        return;
    }
    currentValue = Math.log(num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function log10() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    if (num <= 0) {
        alert('Logarithm of non-positive number is undefined');
        return;
    }
    currentValue = Math.log10(num).toString();
    shouldResetDisplay = true;
    updateDisplay();
}

function toggleSign() {
    if (currentValue === '') {
        return;
    }
    const num = parseFloat(currentValue);
    currentValue = (-num).toString();
    updateDisplay();
}

function updateDisplay() {
    display.value = currentValue || '0';
}

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9') {
        appendNumber(e.key);
    } else if (e.key === '.') {
        appendNumber('.');
    } else if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
        appendOperator(e.key);
    } else if (e.key === 'Enter' || e.key === '=') {
        calculate();
    } else if (e.key === 'Backspace') {
        deleteLast();
    } else if (e.key === 'Escape') {
        clearDisplay();
    }
});

// Initialize display
updateDisplay();