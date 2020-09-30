/*
 * 使用说明:
 * window.wxc.Pop(popHtml, [type], [options])
 * popHtml:html字符串
 * type:window.wxc.xcConfirm.typeEnum集合中的元素
 * options:擴展對象
 * 用法:
 * 1. window.wxc.xcConfirm("我是弹窗<span>lalala</span>");
 * 2. window.wxc.xcConfirm("成功","success");
 * 3. window.wxc.xcConfirm("請輸入","input",{onOk:function(){}})
 * 4. window.wxc.xcConfirm("自訂義",{title:"自訂義"})
 */
(function($){
	window.wxc = window.wxc || {};
	window.wxc.xcConfirm = function(popHtml, type, options) {
	    var btnType = window.wxc.xcConfirm.btnEnum;
		var eventType = window.wxc.xcConfirm.eventEnum;
		var popType = {
			info: {
				title: "信息",
				icon: "0 0",//蓝色i
				btn: btnType.ok
			},
			success: {
				title: "成功",
				icon: "0 -48px",//藍色對勾
				btn: btnType.ok
			},
			error: {
				title: "錯誤",
				icon: "-48px -48px",//红色叉
				btn: btnType.ok
			},
			confirm: {
				title: "提示",
				icon: "-48px 0",//黃色問號
				btn: btnType.okcancel
			},
			warning: {
				title: "警告",
				icon: "0 -96px",//黃色嘆號
				btn: btnType.okcancel
			},
			input: {
				title: "输入",
				icon: "",
				btn: btnType.ok
			},
			custom: {
				title: "",
				icon: "",
				btn: btnType.ok
			}
		};
		var itype = type ? type instanceof Object ? type : popType[type] || {} : {};//格式化输入的参数:彈窗類型
		var config = $.extend(true, {
			//屬性
			title: "", //自訂義標題
			icon: "", //圖標
			btn: btnType.ok, //按钮,默認單按鈕
			//事件
			onOk: $.noop,//點擊確定的按鈕回调
			onCancel: $.noop,//點擊取消的按鈕回调
			onClose: $.noop//弹窗關閉的回調,返回觸發事件
		}, itype, options);
		
		var $txt = $("<p>").html(popHtml);//弹窗文本dom
		var $tt = $("<span>").addClass("tt").text(config.title);//標題
		var icon = config.icon;
		var $icon = icon ? $("<div>").addClass("bigIcon").css("backgroundPosition",icon) : "";
		var btn = config.btn;//按钮组生成参数
		
		var popId = creatPopId();//弹窗索引
		
		var $box = $("<div>").addClass("xcConfirm");//彈窗插件容器
		var $layer = $("<div>").addClass("xc_layer");//遮罩層
		var $popBox = $("<div>").addClass("popBox");//彈窗盒子
		var $ttBox = $("<div>").addClass("ttBox");//彈窗頂部區域
		var $txtBox = $("<div>").addClass("txtBox");//彈窗内容主體區
		var $btnArea = $("<div>").addClass("btnArea");//按钮區域
		
		var $ok = $("<a>").addClass("sgBtn").addClass("ok").text("确定");//確定按鈕
		var $cancel = $("<a>").addClass("sgBtn").addClass("cancel").text("取消");//取消按钮
		var $input = $("<input>").addClass("inputBox");//输入框
		var $clsBtn = $("<a>").addClass("clsBtn");//關閉按鈕
		
		//建立按钮映射關係
		var btns = {
			ok: $ok,
			cancel: $cancel
		};
		
		init();
		
		function init(){
			//處理特殊類型input
			if(popType["input"] === itype){
				$txt.append($input);
			}
			
			creatDom();
			bind();
		}
		
		function creatDom(){
			$popBox.append(
				$ttBox.append(
					$clsBtn
				).append(
					$tt
				)
			).append(
				$txtBox.append($icon).append($txt)
			).append(
				$btnArea.append(creatBtnGroup(btn))
			);
			$box.attr("id", popId).append($layer).append($popBox);
			$("body").append($box);
		}
		
		function bind(){
			//點擊按鈕確認
			$ok.click(doOk);
			
			//enter鍵觸發按鈕事件
			$(window).bind("keydown", function(e){
				if(e.keyCode == 13) {
					if($("#" + popId).length == 1){
						doOk();
					}
				}
			});
			
			//點擊取消按鈕
			$cancel.click(doCancel);
			
			//點擊關閉按鈕
			$clsBtn.click(doClose);
		}

		//確認按鈕事件
		function doOk(){
			var $o = $(this);
			var v = $.trim($input.val());
			if ($input.is(":visible"))
		        config.onOk(v);
		    else
		        config.onOk();
			$("#" + popId).remove(); 
			config.onClose(eventType.ok);
		}
		
		//取消按钮事件
		function doCancel(){
			var $o = $(this);
			config.onCancel();
			$("#" + popId).remove(); 
			config.onClose(eventType.cancel);
		}
		
		//關閉按鈕事件
		function doClose(){
			$("#" + popId).remove();
			config.onClose(eventType.close);
			$(window).unbind("keydown");
		}
		
		//生成按钮组
		function creatBtnGroup(tp){
			var $bgp = $("<div>").addClass("btnGroup");
			$.each(btns, function(i, n){
				if( btnType[i] == (tp & btnType[i]) ){
					$bgp.append(n);
				}
			});
			return $bgp;
		}

		//重生popId,防止id重複
		function creatPopId(){
			var i = "pop_" + (new Date()).getTime()+parseInt(Math.random()*100000);//彈窗索引
			if($("#" + i).length > 0){
				return creatPopId();
			}else{
				return i;
			}
		}
	};
	
	//按钮類型
	window.wxc.xcConfirm.btnEnum = {
		ok: parseInt("0001",2), //確定按鈕
		cancel: parseInt("0010",2), //取消按鈕
		okcancel: parseInt("0011",2) //確定&&取消
	};
	
	//觸發事件類型
	window.wxc.xcConfirm.eventEnum = {
		ok: 1,
		cancel: 2,
		close: 3
	};
	
	//彈窗類型
	window.wxc.xcConfirm.typeEnum = {
		info: "info",
		success: "success",
		error:"error",
		confirm: "confirm",
		warning: "warning",
		input: "input",
		custom: "custom"
	};

})(jQuery);