# python-myapp

## Usage

    # コンテナをビルドする.
    docker-compose build

    # コンテナを起動する.
    docker-compose up -d

    # タスク一覧を表示する.
    docker-compose run app invoke -l

    # MySQL に接続する.
    docker-compose exec mysql mysql -umyapp -p myapp

    # hello アプリケーションを実行する.
    docker-compose run app invoke run.hello

    # webapi アプリケーションを実行する.
    docker-compose run -p 10080:80 app invoke run.webapi
    curl localhost:10080

