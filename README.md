#NDC API

This repo contains the scaffolding for a new REST API for the National Digital Catalog. It exposes all of the data functionality built through the [ndc-pipeline](https://github.com/nggdpp/ndc-pipeline) and leverages functions from the [pynggdpp](https://github.com/nggdpp/pynggdpp) package. It is built with the Flask RestPlus framework to provide Swagger documentation. A live deployment of the API will be determined based on where we can spin up this environment. All of the data connections require environment variables indicating where the infrastructure is located and how it can be accessed.