/**
 * Created by Mihaly on 19/07/2017.
 * @return {null}
 */

function GetQueryString(name)
{
    var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    return r ? decodeURIComponent(r[2]) : null;
}
function search() {
    var s = GetQueryString('s');
    if (s !== null){
        $.getJSON('http://121.40.161.184:8216/search?s=' + s, function (data) {
            if(data["code"] ===0){
                data = data["data"];
                var result = document.getElementById('result');
                result.style.display = 'block';
                var l = document.getElementById('count');
                l.innerHTML = '共有' + data.length.toString() + '条有关' + s + '的记录';
                var table = result.getElementsByTagName('table')[0];
                var m_url = 'http://121.40.161.184:8216/music/';
                for (var i = 0; i < data.length; i++){
                    var tr = document.createElement('tr');
                    tr.innerHTML += '<td>' + data[i]["name"] + '</td>';
                    tr.innerHTML += '<td style="max-width:500px">' + data[i]["value"] + '</td>';
                    tr.innerHTML += '<td><audio src="' + m_url + data[i]["name"] + '" controls="controls" style="width: 400px"></audio></td>';
                    table.appendChild(tr);
                }
                highLight(s)
            }
        })
    }
}

function highLight(s){
    var ym=document.getElementById('result').getElementsByTagName('table')[0].innerHTML;//ss是要高亮的区域，div的id值
    document.getElementById('result').getElementsByTagName('table')[0].innerHTML=ym.replace(new RegExp(s,'gm'), "<span style='color: red; font-weight: bold'>" +s+"</span>") ;
}

