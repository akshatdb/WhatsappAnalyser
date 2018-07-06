function plotBar(x, y, divid, bMargin)
{
    div = document.getElementById(divid);
    Plotly.plot( div, [{
        x: x,
        y: y,
        type: 'bar'
    }],
    {margin: {
        b: bMargin
    },
    height: 700},
    {displayModeBar: false},
    {displaylogo: false},
    {modeBarButtonsToRemove: 'all'},
    );
}
function plotChart(x, y, divid)
{
    div = document.getElementById(divid);
    Plotly.plot( div, [{
        x: x,
        y: y,
    }],
    {displayModeBar: false},
    {displaylogo: false},
    {modeBarButtonsToRemove: 'all'},
    );
}
function processData(data)
{
    SenderCountPlot = data['response']['SenderMessageCountPlot'];
    DateWise = data['response']['UsagePatternDatewise'];
    DayWise = data['response']['UsagePatternDaywise'];
    MonthWise = data['response']['UsagePatternMonthwise'];
    Overall = data['response']['UsagePatternOverall'];
    plotBar(SenderCountPlot[0],SenderCountPlot[1], 'sendercount'), 250;
    plotChart(DateWise[0], DateWise[1], 'datewise');
    plotChart(MonthWise[0], MonthWise[1], 'monthwise');
    plotChart(DayWise[0], DayWise[1], 'daywise');
    plotBar(Overall[0], Overall[1], 'overall', 100);
}    
    
    
var Upload = function (file, addr) {
    this.file = file;
    this.addr = addr;
};


//Upload
Upload.prototype.doUpload = function () {
    var that = this;
    var formData = new FormData();

    // add assoc key values, this will be posts values
    formData.append("msgfile", this.file);
    formData.append("title", "new.txt");
    $.ajax({
        type: "POST",
        url: that.addr,
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', that.progressHandling, false);
            }
            return myXhr;
        },
        success: processData,
        error: function (error) {
        },
        async: true,
        data: formData,
        cache: false,
        dataType: 'json',
        contentType: false,
        processData: false,
        timeout: 66000
    });
};


//Upload progress
Upload.prototype.progressHandling = function (event) {
    var percent = 0;
    var position = event.loaded || event.position;
    var total = event.total;
    var progress_bar_id = "#progress-wrp";
    if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }
    // update progressbars classes so it fits your code
    $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
    $(progress_bar_id + " .status").text(percent + "%");
    if (percent == 100) {
        $(progress_bar_id).fadeOut('fast');
        $('#process-wrp').fadeIn('fast');
    }
};