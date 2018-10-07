# python-myapp

## Usage

    # コンテナをビルドする.
    docker-compose build

    # タスク一覧を表示する.
    docker-compose run app invoke -l

    # Web アプリケーションを起動する.
    docker-compose run -p 10080:80 app uwsgi --yaml uwsgi.yml
    curl localhost:10080

