document.getElementById('sendButton').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;
    fetch('http://localhost:5000/api/run_prototype', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({userInput: userInput}),
    })
    .then(response => response.json())
    .then(data => {
        var category = data.category;
        document.getElementById(category).value += userInput + '\n';
    });
});