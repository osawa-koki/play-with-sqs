# play-with-sqs

💏💏💏 SQSを使ってメッセージキューイングを実装するサンプルです！  

## 開発環境の構築方法

最初にAWS CLIをインストールします。  
<https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/install-cliv2.html>  

以下のコマンドを実行して、AWS CLIのバージョンが表示されればOKです。  

```shell
aws --version
```

認証情報を設定します。  

```shell
aws configure
```

以下のように聞かれるので、適宜入力してください。

```shell
AWS Access Key ID [None]: アクセスキーID
AWS Secret Access Key [None]: シークレットアクセスキー
Default region name [None]: リージョン名
Default output format [None]: json
```

これらの情報は、AWSのコンソール画面から確認できます。  
IAMのページから指定のユーザを選択肢、アクセスキーを発行してください。  

続いて、AWS SAMをインストールします。  
こちらはサーバレスアプリケーションを構築するためのツールです。  
<https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html>  

以下のコマンドを実行して、AWS SAMのバージョンが表示されればOKです。  

```shell
sam --version
```

サーバサイドアプリケーションを開発用に実行するためには、以下のコマンドを実行します。  
ビルドにはDockerが必要です。  

```shell
sam build --use-container

cd ./src/
pip install -r ./requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 3000
# sam local start-api
```

<http://localhost:3000/api/ping>にリクエストを投げて、`{"message":"Hello World"}`が返ってくればOKです。  

各、イベントを発火させるには、以下のコマンドを実行します。  

```shell
sam local invoke --event <イベントファイルまでのパス> <関数名>

# 例
sam local invoke --event ./events/event.json LambdaFunction
```

### チェックコマンド

```shell
# `PYTHONPATH`を設定します。
export PYTHONPATH="$(pwd)/src/:$PYTHONPATH"

# テスト
python -m pytest ./tests/ -v

# Lint
python -m flake8 ./src/ ./tests/

# Formatter
python -m black ./src/ ./tests/

# Import Sort
python -m isort ./src/ ./tests/

# Type Check
python -m mypy --ignore-missing-imports ./src/ ./tests/
```

## 本番環境の準備

### GitHub Secretsの設定

| キー | バリュー |
| --- | --- |
| PROJECT_NAME | プロジェクト名(CloudFormationのスタック名) |
| AWS_ACCESS_KEY_ID | AWSのアクセスキーID |
| AWS_SECRET_ACCESS_KEY | AWSのシークレットアクセスキー |
| AWS_REGION | リージョン名 |

`v-*`の形式のタグをつけると、`GitHub Actions`が実行され、リソースのプロビジョニングが行われます。  
以下のコマンドで、デプロイされたAPIのURLを確認できます。  

```shell
aws cloudformation describe-stacks --stack-name <プロジェクト名> --query 'Stacks[].Outputs[?OutputKey==`LambdaFunctionEventApi`].OutputValue' --output text
```

---

また、以下のコマンドで手動でデプロイすることもできます。  

```shell
sam build --use-container
sam deploy --stack-name <プロジェクト名>
```

## 環境情報

| 環境 | バージョン |
| --- | --- |
| AWS CLI | 2.11.20 |
| SAM CLI | 1.83.0 |
