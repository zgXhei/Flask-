// 标志位，用于判断是否可以绑定点击事件
var isCountdownRunning = false;

// 开始倒计时的函数
function startCountdown(btnElement) {
    if (isCountdownRunning) return; // 如果正在倒计时，则不重复开始

    isCountdownRunning = true; // 设置标志位为true，表示正在倒计时
    var countdown = 60;
    var timer = setInterval(function () {
        countdown--;
        btnElement.text(countdown + '秒后重新发送'); // 更新按钮文本

        if (countdown <= 0) {
            clearInterval(timer); // 清除定时器
            btnElement.text('获取验证码'); // 重置按钮文本
            isCountdownRunning = false; // 设置标志位为false，允许重新点击
            // 如果需要，可以在这里调用发送验证码的函数
        }
    }, 1000);
}

// 绑定到id为'captcha-btn'的元素的点击事件
function bindEmailCaptcha() {
    //确保元素上只有一个你指定的点击事件处理程序，或者你想在绑定新处理程序之前先移除所有旧的处理程序
    $('#captcha-btn').off('click').on('click', function (event) {
        var $this = $(this);
        event.preventDefault();
        var email = $("input[name='email']").val();
        if (!isCountdownRunning) {
            // 开始倒计时
            startCountdown($this);

            // 发送验证码的AJAX请求（如果需要）
            $.ajax({
                url: '/auth/captcha/email?email=' + email, // 请求的URL，带有查询参数email
                method: 'GET', // 请求方法
                success: function(data) {
                    // 处理成功的逻辑（这里可能不需要做什么）
                    console.log('验证码发送成功');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // 处理错误的逻辑（例如显示错误信息）
                    console.error('验证码发送失败: ' + textStatus, errorThrown);
                    // 如果请求失败，可能需要重置倒计时状态（但通常我们不希望这样做，因为用户可能想要重试）
                    // isCountdownRunning = false; // 根据你的需求来决定是否要重置
                    $('#captcha-btn').text('获取验证码'); // 如果要重置，可以恢复按钮文本
                }
            });
        }
    });
}

$(document).ready(function () {
    bindEmailCaptcha();
});