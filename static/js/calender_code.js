//#http://www.mikesmithdev.com/fullcalendar-jquery-ui-modal/
$(document).ready(function() 
{
	$('#calendar').fullCalendar(
	{
		header: 
		{
			left:'today',
			center: 'prev title next',
			right: 'month,basicWeek,basicDay,year'
			//right: 'month,basicWeek,basicDay,year'
		},
		navLinks: false,
		editable: false,
		eventLimit: true, // allow "more" link when too many events
		//timezone:'America/New_York',
		displayEventTime: false,
		events:function(start, end, timezone,callback) 
		{
			var cal_date = $('#calendar').fullCalendar('getDate');
			cal_date = cal_date.format('YYYY/MM/DD');
			var dataString = "date="+cal_date;
			$.ajax(
			{
				url: '/calendar_data/',
				dataType:'json',
				type: 'GET',
				contentType: 'application/json',
				data:dataString,
				beforeSend:function(xhr,settings)
				{
					var csrftoken = $('meta[name=csrf-token]').attr('content');
					//if (!/^(GET|HEAD|OPTIONS|TRACE|POST)$/i.test(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}
				},
				success: function(resp)
				{
					var events = [];
					for (i =0; i < resp.data.length; i++)
					{
							events.push({
							title: resp.data[i].title,
							start: resp.data[i].start+'T00:00:00', // will be parsed
							end: resp.data[i].end+'T23:59:59'
							});
					}
					$('#calendar-warning').hide();
					callback(events);
				},
				error: function()
				{
					$('#calendar-warning').show();
				}
			});//ajax end
			
	      	}//events end
	
		//start event render
  		,eventRender: function(event, element) 
		{
			element.attr('href', 'javascript:void(0);');
			element.click(function() 
			{
				$("#title").html(event.title);
		            	$("#startTime").html(moment(event.start).format('MMMM Do YYYY'));
		            	$("#endTime").html(moment(event.end).format('MMMM Do YYYY'));
		            	//$("#eventContent").dialog({ modal: true, title: event.title, width:350});
				$("#eventContent").dialog({ modal: false,  width:350});
        		});

  		}
		//stop event render
	});
	
});

