# BUILD APP

sam build --template-file template.dev.yaml


# START APP

sam local start-api -p 8080 --docker-network 4c56ee4f0230 --log-file logs.txt