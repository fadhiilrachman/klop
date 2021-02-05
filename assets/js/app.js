var json_url = '/api/analyze';

function convertToRupiah(angka)
{
	var rupiah = '';		
	var angkarev = angka.toString().split('').reverse().join('');
	for(var i = 0; i < angkarev.length; i++) if(i%3 == 0) rupiah += angkarev.substr(i,3)+'.';
	return 'Rp '+rupiah.split('',rupiah.length-1).reverse().join('');
}

function renderHasil(data) {
	if(!data) return false;
	$('.btn.btn-primary').hide();
	$('.btn.btn-danger').show();
	var html='Instagram anda memiliki potensi nilai sebesar ' + convertToRupiah(data.score), i=0;
	html+='<ol>';
	while(i < data.kriteria.length) {
		html+='<li>' + data.kriteria[i] + '</li>';
		i++;
	}
	html+='</ol>';
	$('#question-title').html('<a href="https://www.instagram.com/'+data.username+'/" target="_blank" title="See your profile"><img class="img-circle" src="'+data.profile_pic+'" width="50px" height="50px"/></a> Your Social Currency');
	$('#question-text').html(html);
}

function proses(p) {
	$('.btn.btn-primary').hide();
	$('#question-text').html('<img src="/assets/images/loading-sm.gif"> Klop sedang menganalisa&hellip;');
	$.post(json_url, {u: p}, function(res) {
		if(res.error) {
			alert('Terjadi galat: ' + res.error);
		} else {
			renderHasil(res);
		}
	});
}

$(".btn.btn-primary").click(function(){
	proses_aja();
});

function proses_aja() {
	if($("input[name='username']").val()=='' || $("input[name='username']").val()==' ') {
		alert('Terjadi galat: Masukkan username instagram anda');
	} else {
		proses($("input[name='username']").val());
	}
}

$(document).ready(function() {
	if(document.title.indexOf("Klop:")==0) {
		setTimeout(function() {
			$('#question-title,#question-button').fadeIn();
			$('.btn.btn-danger').hide();
			$('#question-text').html('<form onsubmit="proses_aja(); return false;"><div class="form-group"><input class="form-control" placeholder="Username Instagram disini..." name="username" type="text"></input></div></form>').fadeIn();
		}, 500);
	}
});