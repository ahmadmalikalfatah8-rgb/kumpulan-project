function sum (operator) {
  var a = Number(document.getElementById('a').value);
  var b = Number(document.getElementById('b').value);
  var result;

  if (operator === '+') result = a + b;
  if (operator === '-') result = a - b;
  if (operator === '*') result = a * b;
  if (operator === '/') result = b === 0 ? 'Cant divide by zero' : a / b;

  document.getElementById('result').textContent = result;
}