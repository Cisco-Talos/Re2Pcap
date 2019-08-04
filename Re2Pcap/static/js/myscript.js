var requestPlaceholder = 'POST /index.html HTTP/1.1\nAccept-Encoding: identity\nHost: host.example:8080\nUser-Agent: Mozilla/5.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: 23\n\ngreeting=Hello_World!\n';

$('#inputRequest').attr('placeholder', requestPlaceholder);

var responsePlaceholder = 'HTTP/1.1 200 OK\nServer: nginx\nContent-Type: text/html\nContent-Length: 13\n\nHello World!\n';
$('#inputResponse').attr('placeholder', responsePlaceholder);

$('#submit').attr('disabled', true);

$(document).ready(function(){
	$('#Re2Pcap').on('submit',function (e) {
		$('#submit').attr('disabled', true);
		$('#errorAlert').hide();
		$('#successAlert').hide();
		$('#progressAlert').text('Baking PCAP, please wait....').show();
	});
	$('#prograssAlert').hide();
	$('#submit').attr('disabled', false);
});

$('textarea[name^=input]').change(function(){
	$.ajax({
		data: {
			inputRequest : $('#inputRequest').val(),
               inputResponse : $('#inputResponse').val(),
               pcapFileName : $('#pcapFileName').val()
		},
		context: this,
		type: 'POST',
		url: '/validate'
	})
	.done(function(data) {
		if (data.error) {
			$('#errorAlert').text(data.error).show();
			$('#successAlert').hide();
			$('#progressAlert').hide();
			$('#submit').attr('disabled', true);
		}
		else {
			$('#successAlert').text(data.success).show();
			$('#errorAlert').hide();
			$('#progressAlert').hide();
			$('#submit').attr('disabled', false);
		}
       });
});
