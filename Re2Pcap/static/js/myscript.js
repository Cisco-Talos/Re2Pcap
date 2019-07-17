var placeholder = 'POST /index.html HTTP/1.1\nHost: 10.10.10.1:8080\nUser-Agent: Mozilla\n\nHello World! \n\nOR\n\nHTTP/1.1 200 OK\nServer: nginx\n\nHello World! ';
$('#inputText').attr('placeholder', placeholder);

$('#submit').prop('disabled', true);
$('#inputText').on({
    'focusout': handleInput,
    'input': handleInput,
    'focus': handleInput,
    'keyup': handleInput
});

function handleInput() {
    var text = $('#inputText').val().split('\n')[0];
    var re = /^(HTTP\/\d{1}\.\d{1}|GET|POST|HEAD|PUT|DELETE|CONNECT|OPTIONS|TRACE|PATCH)\ .*$/;
    var is_valid = re.test(text);
    if(is_valid) {
        $('#submit').prop('disabled', false);
    }
    else {
        $('#submit').prop('disabled', true);
    }
}