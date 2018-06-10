# python-app

## Usage

    docker-compose build
    docker-compose run app invoke -l

    docker-compose run -p 10080:80 app uwsgi --yaml uwsgi.yml
    curl localhost:10080

