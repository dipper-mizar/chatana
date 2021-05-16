window.onload = function () {
    ws = new WebSocket(ws_url)
    window.s = ws;
    ws.onopen = function () {
        console.log('connect!')
        var str = '【Auto reply】' + nickname + ', 加入房间。'
        calc_count_person()
        addMsg(str)
        sendServerMsg(str)
    }
    ws.onmessage = function (e) {
        var str_and = e.data
        var nickname_ret = str_and.substr(str_and.lastIndexOf(" ") + 1)
        if (nickname_ret == nickname || str_and.includes("Auto reply")) {
            return
        }
        var str = str_and.replace(nickname_ret, "")
        var joinreg = RegExp(',加入聊天')
        var leavereg = RegExp(',离开聊天')

        if (str.match(joinreg)) {
            var person = str.substring(0, str.length - 5)
            addPerson(person)
            //calc_count_person()
            addMsg(str)

        } else if (str.match(leavereg)) {
            var person = str.substring(0, str.length - 5)
            subPerson(person)
            addMsg(str)
        } else {
            addMsg(str, "ret", nickname_ret)
        }

    }
    ws.onclose = function (e) {
        console.log("WebSocket已关闭")
    }
}

// Before refresh the page
function f() {
    if (window.s) {
        window.s.close()
    }
}

function logout() {
    var str = '【Auto reply】' + nickname + ',离开房间。'
    if (window.s) {
        sendServerMsg(str)
        window.s.close()
        console.log("WebSocket已关闭")
        window.location.href = '/user/logout/?nickname=' + nickname;
    } else {
        alert("未知错误！")
    }
}

function sendBtn() {
    var input = document.getElementsByClassName('msg')[0];
    var msg = input.value;
    var str = msg
    if (!window.s) {
        alert("WebSocket未连接！")
    } else {
        result = addMsg(str, "enter", nickname)
        if (result) {
            input.value = ''
            sendServerMsg(str, nickname)
        }
        $.ajax({
            type: 'POST',
            url: '/save/',
            data: {'text': str, 'nickname': nickname},
            async: true,
            success: function (data) {
                if (data.status == 'fail') {
                    alert("Unknown error: " + data.msg)
                }
            },
        });
    }
}

function sendShortCut(event) {
    if (event.keyCode == 13) {
        var input = event.target
        var msg = input.value
        if (event.ctrlKey) {
            //ctrl+enter
            input.value = msg + '\n'
        } else {
            //enter
            event.preventDefault()
            var str = msg
            if (!window.s) {
                alert("WebSocket未连接")
            } else {
                result = addMsg(str, "enter", nickname)
                if (result) {
                    input.value = ''
                    sendServerMsg(str, nickname)
                    $.ajax({
                        type: 'POST',
                        url: '/save/',
                        data: {'text': str, 'nickname': nickname},
                        async: true,
                        success: function (data) {
                            if (data.status == 'fail') {
                                alert("Unknown error: " + data.msg)
                            }
                        },
                    });
                }
            }
        }

    }
}

function addMsg(text, message_type, nickname) {
    var element = document.getElementsByClassName('info')[0];
    var pic = document.createElement('p')
    var msg = document.createElement('p');
    var ele = document.getElementById("msg_view")
    if (text.includes("Auto reply")) {
        msg.setAttribute("style", "text-align: center;color: grey; font-size: 10px")
        msg.innerText = text;
        element.appendChild(msg)
        return true
    } else if (message_type == "ret") {
        msg.setAttribute("style", "text-align: left")
        pic.setAttribute("style", "text-align: left; margin-right: 82px;")
        pic.innerHTML += "<img style='margin-right: 10px; height: 25px; width: 25px;' src='/static/images/default-userlogo-male.png'>" + nickname + ":"
        msg.innerHTML += "<span style='padding: 10px; max-width: 100%; height: 20px; color: white; background-color:cornflowerblue; border: 2px solid; border-radius: 25px'>" + text + "</span>";
        element.appendChild(pic)
        element.appendChild(msg)
        ele.scrollTop = ele.scrollHeight;
        return true
    } else if (message_type == "enter") {
        msg.setAttribute("style", "text-align: right")
        pic.setAttribute("style", "text-align: right; height: 30px;")
        msg.innerHTML += "<span style='padding: 10px; max-width: 100%; height: 20px; color: white; background-color:cornflowerblue; border: 2px solid; border-radius: 25px'>" + text + "</span>";
        pic.innerHTML += "<img style='margin-right: 10px; height: 25px; width: 25px;' src='/static/images/default-userlogo-male.png'>" + nickname + ":"
        element.appendChild(pic)
        element.appendChild(msg)
        ele.scrollTop = ele.scrollHeight;
        return true
    }
    msg.innerText = text;
    element.appendChild(msg)
    return true
}

// text and nickname split by " "
function sendServerMsg(text, nickname) {
    ws.send(text + " " + nickname)
}

function calc_count_person() {
    var span = document.getElementById('count')
    span.innerHTML = count
}

function addPerson(person) {
    var ele = document.createElement('li')
    ele.innerHTML = person
    document.getElementById('person').appendChild(ele)
    var span = document.getElementById('count')
    var count = span.innerText
    count = parseInt(count) + 1
    span.innerHTML = count
}

function subPerson(person) {
    var list = document.getElementById("person").getElementsByTagName("li");
    for (var i = 0; i < list.length; i++) {
        var aa = list[i].innerText
        if (aa == person) {
            list[i].remove()
        }
    }
    //在线人数
    var span = document.getElementById('count')
    var count = span.innerText
    count = parseInt(count) - 1
    span.innerHTML = count
}
