$(function() {
	//start of js
	
	$('.script_works').click(function() 
	{
		alert('asfasdfasdfadsf');
		$.ajax(
		{
			url: '/signUpUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
	
	$('.take_photo').click(function(event) 
	{
		$('#cam_row').hide();
		$('#pic_row').hide();
		$.ajax(
		{
			url: '/camera/',
            data: { take_photo: 1},//$('form').serialize(),
            type: 'GET',
            //contentType: 'application/json',
            dataType: 'json',
            success: function(response) 
            {
				photo = response.data[0].photo;
				name = response.data[1].name;
				//$("#message").text(response.data[0].photo);
				$("#message").html(name + "<br /><img src='/" + photo + "'>");
				//$("#message").html("Time Taken: "+name +" photo:" + photo + "<br /><img src='/" + photo + "'>");
				$('#cam_row').show();
				$('#pic_row').show();
            },
            error: function(error) 
            {
				//alert(error);
				console.log(error);
				$("#message").text("error");
				$('#cam_row').show();
            }
		});
		event.preventDefault();
		//return false;
	});
	
	
	//end of js
});
