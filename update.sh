ps -ax |grep python3|awk '{print $1}'|xargs kill -9
git pull
nohup python3 manage.py runserver 0.0.0.0:8888 > log/run.log 2>&1 &
