// 按钮触发
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
        type: "get",
        data: {"word": search_str},
        success: function callbackFun(data) {
            // 开始处理 处理数据
            // console.log('ok')
            // 转义html 防止注入
            var newData = data.replace(/</g,'&lt;').replace(/>/g,'&gt;');
            // 
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
        console.log(dataInfo);
        // 拼接
        var tbody_content = "";
        for (var i = 0; i < dataInfo.length; i++) {
            tbody_content += 
            `<div class="panel panel-default"><div class="panel-heading"><div class="panel-name"><p>`
            + dataInfo[i].name +
            `</p></div></div><div class="panel-body panel-content"><div class="panel-content"><p>`
            + dataInfo[i].content +
            `</p></div></div><div class="panel-footer panel-localtime"><div class="panel-localtime"><p>`
            + dataInfo[i].localtime +
            `</p></div></div></div>`
        }
        $("#msg-body").html(tbody_content);
    }else{
        clearDate();
    }
}

