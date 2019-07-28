var requestPlaceholder = 'POST /index.html HTTP/1.1\nHost: 10.10.10.1:8080\nUser-Agent: Mozilla/5.0\n\nHello World!\n';
$('#inputRequest').attr('placeholder', requestPlaceholder);

var responsePlaceholder = 'HTTP/1.1 200 OK\nServer: nginx\nContent-Length: 13\n\nHello World!\n';
$('#inputResponse').attr('placeholder', responsePlaceholder);

$(document).ready(function() {
	$('#Re2Pcap').on('submit', function(event) {
		$.ajax({
			data: {
				in_Request : $('#inputRequest').val(),
				in_Response : $('#inputResponse').val()
			},
			type: 'POST',
			url: '/validate'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
                $('#successAlert').text("Parsed the Input Correctly. Creating PCAP; Please wait....").show();
				$('#errorAlert').hide();
			}
		});
		event.preventDefault();
	});
});
