# BUILD APP

sam build --template-file template.test.yaml


# START APP

sam local start-api -p 8080 --docker-network 660ebda4c9a2 --log-file logs.txt