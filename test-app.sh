# BUILD APP

sam build --template-file template.dev.yaml


# START APP

sam local start-api -p 8080 --docker-network c675d3b2f109 --log-file logs.txt