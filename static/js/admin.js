// 查询按钮触发
$("#search").click(function () {
    // console.log('request ...')
    search_str = $("#inputContent").val()
    if(search_str.replace(/(^\s*)|(\s*$)/g, "")){
        queryForPages(search_str);
    }else{
        // console.log('f u');
    }
});

// 请求ajax
function queryForPages(search_str) {
    $.ajax({
        url: "/search",
        type: "post",
        data: {"word": search_str},
        success: function callbackFun(data) {
            // 开始处理 处理数据
            // console.log('ok')
            var newData = data.replace(/</g,'&lt;').replace(/>/g,'&gt;');
            console.log(newData);
            // test
            var dataInfo = JSON.parse(newData);  // json转obj
            clearDate();  // 清空div
            fillTable(dataInfo);  // 填充数据
        }
    });
}

// 清空查询结果
function clearDate() {
    $("#msg-body").html("");
}

// 填充数据
function fillTable(dataInfo) {
    if (dataInfo.length > 0){
        // 拼接
        var tbody_content = "";
        for (var i = 0; i < dataInfo.length; i++) {
            tbody_content += 
            `<tr id="` + dataInfo[i].id +
            `"><th scope="row">` + dataInfo[i].localtime +
            `</th><td>` + dataInfo[i].name +
            `</td><td class="admin-msg-info">` + dataInfo[i].content +
            `</td><td class="admin-msg-info">` + dataInfo[i].ip +
            `</td><td><input type="button" onclick="del('` + dataInfo[i].id +
            `')" class="btn btn-sm btn-danger" value="Delete"></td></tr>`
        }
        $("#msg-body").html(tbody_content);
    }else{
        clearDate();
    }
}

// 获得参数 删除
function del(del_id) {
    // console.log(del_id);
    $.ajax({
        url: "/delete",
        type: "post",
        data: {"delid": del_id},
        success: function delok(data) {
            // console.log(data);
            if(data == "1"){
                jq_str = "#" + del_id
                $(jq_str).hide();
            }
        },
    });
}


