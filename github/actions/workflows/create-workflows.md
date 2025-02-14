# GitHub Actions ワークフローの作成

## プロジェクト概要

GitHub Actions を活用した効率的で安全な CI/CD ワークフローの作成のためのガイドラインです。

公式ドキュメントをベースに、実践的な設定方法とベストプラクティス、特にセキュリティリスクと実装上の注意点を詳しく解説します。

## セキュリティリスクと対策

### スクリプトインジェクション対策

**想定されるリスク**

- ユーザー入力値や環境変数を直接シェルコマンドで使用することによる任意コード実行
- GitHub イベントペイロードからの未検証データの使用による権限昇格
- 環境変数の意図しない露出

**対策実装例**

```yaml
jobs:
  build:
    runs-on ubuntu-latest
    steps:
      # 推奨されない実装
      - name Dangerous command
        run echo "${{ github.event.issue.title }}" > file.txt

      # 推奨される実装
      - name Safe command
        env
          SAFE_TITLE ${{ github.event.issue.title }}
        run |
          echo "$SAFE_TITLE" | sed 's/[&|;<>]//g' > file.txt
```

### 依存関係の脆弱性対策

**想定されるリスク**

- サプライチェーン攻撃による不正コードの実行
- 未検証のサードパーティアクションによるセキュリティ侵害
- 古いバージョンの依存関係による既知の脆弱性

**対策実装例**

```yaml
jobs:
  security:
    runs-on ubuntu-latest
    steps:
      - uses actions/checkout@v3

      # 依存関係スキャン
      - name Dependency Review
        uses actions/dependency-review-action@v3
        with
          fail-on-severity moderate
```

### シークレット管理

**想定されるリスク**

- ログへのシークレット出力
- Pull Request でのシークレットアクセス
- フォークリポジトリからのシークレット漏洩

**対策実装例**

```yaml
jobs:
  deploy:
    if github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
    runs-on ubuntu-latest
    steps:
      - name Use secrets safely
        env
          TOKEN ${{ secrets.MY_TOKEN }}
        run |
          set +x
          your_command "$TOKEN"
```

## 実装上の重要な注意点

### ワークフロー権限の制御

```yaml
# リポジトリ全体のデフォルト設定
permissions read-all

jobs:
  specific-job:
    permissions:
      # 必要な権限のみを許可
      contents read
      issues write
      packages read
```

### 環境分離とプロテクション

```yaml
jobs:
  deploy:
    environment:
      name production
      url https//prod.example.com

    # 環境保護ルールの適用
    needs [test, security-scan]
    if github.ref == 'refs/heads/main'
```

### アーティファクトの安全な処理

```yaml
jobs:
  build:
    steps:
      - name Upload artifact
        uses actions/upload-artifact@v3
        with
        name build-output
        path dist/
        retention-days 5
        if-no-files-found error
```

## セキュリティベストプラクティス

### Third-party Actions の評価基準

- メンテナンスの活発さ
- コミュニティの評価
- ソースコードの透明性
- セキュリティ更新の頻度

```yaml
jobs:
  build:
    steps:
      # バージョン固定
      - uses actions/checkout@v3

      # コミットハッシュ使用
      - uses actions/setup-node@a7ce2939025e0ab8e83e52b6b998d835d25fcc60
```

### OIDC 実装

```yaml
jobs:
  aws-deploy:
    permissions
      id-token write
      contents read

    steps:
      - name Configure AWS Credentials
        uses aws-actions/configure-aws-credentials@v4
        with
          role-to-assume arn:aws:iam::123456789012:role/my-role
          aws-region us-east-1
```

## 実装上の制限事項

### ワークフロー制限

- 実行時間 最大 6 時間
- 同時実行ジョブ数 プラン依存
- API 使用制限 レート制限あり

### ランナー制限

- メモリ 7GB (Ubuntu)
- ディスク容量 14GB
- CPU 2 コア

## トラブルシューティングとデバッグ

### デバッグログの設定

```yaml
env
ACTIONS_RUNNER_DEBUG true
ACTIONS_STEP_DEBUG true
```

### エラー処理

```yaml
jobs:
  build:
    steps:
      - name Build with error handling
        run |
        if ! make build; then
        echo "::error::Build failed"
        exit 1
        fi
        continue-on-error false
```

## 参考文献

### 主な参考文献

- [Security Hardening for GitHub Actions](https//docs.github.com/ja/actions/security-guides/security-hardening-for-github-actions)
- [Usage Limits and Billing](https//docs.github.com/ja/actions/reference/usage-limits-billing-and-administration)
- [Security Guides](https//docs.github.com/ja/actions/security-guides)

### セキュリティ関連

- [GitHub Security Lab](https//securitylab.github.com/)
- [GitHub Advisory Database](https//github.com/advisories)
- [GitHub Security Features](https//docs.github.com/ja/code-security)

### 実装ガイド

- [Actions Workflow Syntax](https//docs.github.com/ja/actions/reference/workflow-syntax-for-github-actions)
- [Contexts and Expression Syntax](https//docs.github.com/ja/actions/reference/context-and-expression-syntax-for-github-actions)
- [Environment Variables](https//docs.github.com/ja/actions/reference/environment-variables)
