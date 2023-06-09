
Django示例框架

如何测试运行：
    1.安装python（python3.8）
    2.安装该框架所有库，命令：pip install -r requirements.txt
    3.运行服务：python manage.py runserver --settings=mysite.settings_test
    4.可能会出现数据库异常等 根据配置文件里的配置调整好db设置
    5.生成数据库表,库名test要事先建好，再执行：python manage.py migrate --settings=mysite.settings_test

生产运行：建议使用uWSGI + nginx

