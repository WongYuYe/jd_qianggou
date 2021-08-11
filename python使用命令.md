### 导出所有依赖
pip freeze > requirements.txt

### 安装
pip install -r requirements.txt


### pyinstaller使用

-F 表示生成单个可执行文件；

-D  –onedir 创建一个目录，包含exe文件，但会依赖很多文件（默认选项）。

-w 表示去掉控制台窗口，这在GUI界面时非常有用。不过如果是命令行程序的话那就把这个选项删除吧！；

-c  –console, –nowindowed 使用控制台，无界面(默认)；

-p 表示你自己自定义需要加载的类路径，一般情况下用不到；

-i 表示可执行文件的图标。

pyinstaller -F -w xx.py
