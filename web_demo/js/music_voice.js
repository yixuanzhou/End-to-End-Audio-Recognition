/**
 * Created by Mihaly on 04/07/2017.
 */

function getRecognizedResultM3U8(m_url){
    if(m_url === "")
        alert('请输入正确的地址!');
    var status_box = document.getElementById("status_box");
    status_box.style.display='block';
    status_box.innerHTML = '开始下载。<br/>正在下载。(0S)<br/>';
    var text_status_box = document.getElementById("text_status_box");
    text_status_box.style.display='none';
    var d = new Date();
    var stt = d.getTime();
    var upt = setInterval(function(){
        var d1 = new Date();
        status_box.innerHTML = status_box.innerHTML.replace(/正在下载。\(\d+/, '正在下载。(' + ((d1.getTime() - stt) / 1000).toFixed(0));
    }, 0);
    $.ajaxSetup({
        async : true,
        timeout : 1800000,
        error : function (x, e) {
            clearInterval(upt);
            alert(x + e)
        }
    });
    var url = 'http://121.40.161.184:8216/m3u8_download?' + 'url=' + m_url;
    $.getJSON(url, function (data) {
        if(data.code === 0) {
            clearInterval(upt);
            var filename = data.file_name;
            getRecognizedResult(filename);
        }
        else{
            status_box.innerHTML += '下载失败。<br/>';
            alert(data.msg)
        }

    });
}

function getRecognizedResult(file_name){
    if(file_name === ""){
        alert("请选择正确的文件！");
        return
    }

    var status_box = document.getElementById("status_box");
    status_box.style.display='block';
    var text_status_box = document.getElementById("text_status_box");
    text_status_box.style.display='none';
    if(status_box.innerHTML.match(/处理/))
        status_box.innerHTML = '';
    status_box.innerHTML += '开始处理。<br/>正在处理。(0S)</br>';
    var d = new Date();
    var stt = d.getTime();
    var upt = setInterval(function(){
        var d1 = new Date();
        status_box.innerHTML = status_box.innerHTML.replace(/正在处理。\(\d+/, '正在处理。(' + ((d1.getTime() - stt) / 1000).toFixed(0));
    }, 0);
    $.ajaxSetup({
        async : true,
        timeout : 1800000,
        error : function (x, e) {
            clearInterval(upt);
            alert(x + e)
        }
    });
    var rec_type = '';
    var rec_types = document.getElementsByName('rec_type');
    for(var i=0;i<rec_types.length;i++) {
        if (rec_types[i].checked) {
            rec_type = rec_types[i].value;
        }
    }
    var url = 'http://121.40.161.184:8216/audio_recognize?' + 'file=' + file_name + '&rec_type=' + rec_type;
    $.getJSON(url, function (data) {
        if(data.code === 0) {

            var filename = data.file_name;
            var rec_result = data.rec_result;
            document.getElementById("wav_file_name").innerHTML = filename;
            document.getElementById("player").setAttribute('src', 'http://121.40.161.184:8216/music/' + filename);
            createResultTable(rec_result, data.duration);
            clearInterval(upt);
            status_box.innerHTML += '处理完成。<br/>';

            document.getElementById("player_div").style.display = 'block';
        }
        else{
            status_box.innerHTML += '处理失败。<br/>';
            alert(data.msg)
        }

    });
}

function createResultTable(rec_result, duration){

    var current = 0;
    var result = [];
    for (var i = 1; i < rec_result.length; i++){
        if(rec_result[current] !== rec_result[i]){
            result.push([current * 8, i * 8, rec_result[current]]);
            current = i;
        }
    }
    result.push([current * 8, duration, rec_result[current]]);
    var table = document.getElementById("rec_result");
    table.innerHTML = '';
    var count = result.length;
    for(var k = 0; k < count; k++){
        var tr = document.createElement("tr");
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        td1.innerHTML = formatSeconds(result[k][0]) + '-' + formatSeconds(result[k][1]);
        if(result[k][2] === 1){
            td2.style.color = '#00FDFE';
            td2.innerHTML = '语音';
        }
        else{
            td2.innerHTML = '音乐';
        }
        td2.setAttribute('onclick', 'playFromTo(' + result[k][0] + ', ' + result[k][1] + ')')
        tr.appendChild(td1);
        tr.appendChild(td2);
        if(k === 0){
            var td3 = document.createElement("td");
            var to_text_button = document.createElement("input");
            to_text_button.setAttribute('type', 'button');
            to_text_button.setAttribute('onclick', 'getTextResult()');
            to_text_button.setAttribute('style', "width:140px; height:25px; background-color:transparent; font-family:'Arial Normal', 'Arial'; font-weight:400; font-style:normal; font-size:13px; text-decoration:none; color:#FFFFFF; text-align:center;")
            to_text_button.setAttribute('value', '语音转文字');
            td3.setAttribute('rowspan', String(count));
            td3.appendChild(to_text_button);
            tr.appendChild(td3);
        }
        table.appendChild(tr);
    }
}

function getTextResult(){
    var status_box = document.getElementById("text_status_box");
    status_box.style.display='block';
    if(status_box.innerHTML.match(/转语音/))
        status_box.innerHTML = '';
    status_box.innerHTML += '开始转语音。<br/>正在转语音。(0S)</br>';
    var d = new Date();
    var stt = d.getTime();
    var upt = setInterval(function(){
        var d1 = new Date();
        status_box.innerHTML = status_box.innerHTML.replace(/\d+/, String(((d1.getTime() - stt) / 1000).toFixed(0)));
    }, 10);
    var text_result_field = document.getElementById("text_result");
    text_result_field.innerHTML = '';
    text_result_field.style.display = 'none';
    $.ajaxSetup({
        async : true,
        timeout : 1800000,
        error : function (x, e) {
            clearInterval(upt);
            alert(x + e)
        }
    });
    var url = 'http://121.40.161.184:8216/audio_to_text?' + 'file=' + document.getElementById('wav_file_name').innerHTML;
    $.getJSON(url, function (data) {
        if(data.code === 0) {
            clearInterval(upt);
            status_box.innerHTML += '转语音成功。';
            var text_result = data.text;
            for(var i = 0; i < text_result.length; i++){
                text_result_field.innerHTML += "<p>语音" + (i + 1) + ": " + text_result[i] + '</p><br/>';
            }
            text_result_field.style.display = 'block';
        }
        else{
            alert(data.msg);
            status_box.innerHTML += '转语音失败。';
        }

    });
}

function formatSeconds(value) {
    var h = String(Math.floor(value/3600));
    var m = String(Math.floor(value%3600/60));
    var s = String(Math.floor(value%3600%60));
    if(m.length === 1)
        m = '0' + m;
    if(s.length === 1)
        s = '0' + s;
    return h + ':' + m + ':' + s;
}
var auto_pause;

function playFromTo(stt, edt) {
    if(auto_pause !== null)
        clearInterval(auto_pause);
    var player = document.getElementById('player');
    player.currentTime = stt;
    player.play();
    auto_pause = setInterval(function(){
        if(player.currentTime > edt)
            player.pause();
    }, 0);
}