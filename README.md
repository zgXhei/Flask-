# Flask-
这是个通过Flask框架开发的问答平台
问答平台系统
  技术栈：Flask+MySQL+Python+HTML
  使用Flask框架开发，实现问答平台系统，可以发表评论、提出问题，完成登录验证和注册功能。
  优化用户体验，提升网站性能，为学习者提供便捷高效的讨论平台

项目蓝图在blueprints
  1.auth.py实现用户登录和注册的功,还有邮箱验证码的发送
  2.qa.py实现首页和问答页面的功能
  3.forms.py是实现表单验证
  
models.py是存放三个数据库模型
comfig.py是数据库和邮箱的配置,为了不泄露隐私我选择删除，如果需要使用请自行填写
app.py是主入口
