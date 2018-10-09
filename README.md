# python-myapp

## Usage

    # コンテナをビルドする.
    docker-compose build

    # タスク一覧を表示する.
    docker-compose run app invoke -l

    # hello アプリケーションを実行する.
    docker-compose run -p 10080:80 app invoke run.hello

    # webapi アプリケーションを実行する.
    docker-compose run -p 10080:80 app invoke run.webapi
    curl localhost:10080

