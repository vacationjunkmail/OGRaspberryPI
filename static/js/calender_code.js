$(document).ready(function() 
{
	$('#calendar').fullCalendar(
	{
		header: 
		{
			left:'prev,next today',
			center: 'title',
			right: 'month,basicWeek,basicDay,year'
		},
		navLinks: true,
		editable: true,
		eventLimit: true, // allow "more" link when too many events
		events:function(start, end, timezone,callback) 
		{
			var cal_date = $('#calendar').fullCalendar('getDate');
			cal_date = cal_date.format('YYYY/MM/DD');
			//console.log(cal_date);
			var dataString = "date="+cal_date;
			
			console.log($('#calendar').fullCalendar());
			
			$.ajax(
			{
				url: '/calendar_data/',
				dataType:'json',
				type: 'GET',
				contentType: 'application/json',
				data:dataString,
				success: function(resp)
				{
					var events = [];
					for (i =0; i < resp.data.length; i++)
					{
						//console.log(resp.data[i].title);
						events.push({
							title: resp.data[i].title,
							start: resp.data[i].start // will be parsed
						});
					}
					//console.log(events);
					callback(events);
				
				},
				error: function()
				{
					$('#calendar-warning').show()
				}
			});
			
      	}
	});
	
});
