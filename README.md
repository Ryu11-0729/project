

部署的时候注意防火墙设置端口放行。

前端：

```
cd web
npm install --registry=https://registry.npm.taobao.org
npm run dev
```

后端:

```
cd backend
./conf/env.example.py 文件为一份新的到 ./conf 文件夹下，并重命名为 env.py  注意设置里面mysql的配置信息
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py init
python manage.py init_area
python manage.py runserver 0.0.0.0:8000
```

需要放图片资源可以用tomcat服务器放

