# Chrome 拡張機能の作成

## プロジェクト概要

Chrome 拡張機能の開発プロジェクト。TypeScript、Vite を活用し、Manifest V3 をベースとした実用的で安全な拡張機能を作成します。

## 基本方針

### 設計原則

1. Chrome 拡張機能の標準的な実装方針に従う

   - Manifest V3 形式の厳守
   - 適切な権限管理（最小権限の原則）
   - セキュリティとプライバシーへの配慮
   - Feature-based アーキテクチャの採用

2. 開発環境の最適化

   - TypeScript による型安全性の確保
   - Vite による効率的なビルドプロセス
   - ESLint によるコード品質の維持
   - モダンな開発ツールチェーンの活用

3. コンポーネント設計
   - 再利用可能な UI コンポーネント
   - 明確な責務の分離
   - 一貫性のある設計パターン
   - 効率的な状態管理

### プロジェクト構造

```
.
├── destinations/            # ビルド成果物のディレクトリ
│   ├── content/             # コンテンツスクリプト用の成果物
│   │   ├── index.js         # バンドルされたJavaScript
│   │   └── index.css        # 最適化されたCSS
│   ├── something/           # その他の機能の成果物
│   │   ├── index.js         # バンドルされたJavaScript
│   │   └── index.css        # 最適化されたCSS
│   ├── icons/               # 拡張機能アイコン
│   │   ├── 128.png          # 128x128 サイズのアイコン
│   │   ├── 16.png           # 16x16 サイズのアイコン
│   │   ├── 32.png           # 32x32 サイズのアイコン
│   │   └── 48.png           # 48x48 サイズのアイコン
│   └── manifest.json        # 拡張機能マニフェスト
├── sources/                 # ソースコードのルートディレクトリ
│   ├── components/          # 共通UIコンポーネント
│   │   ├── SomeThing/       # コンポーネント用ディレクトリ
│   │   │   └── index.ts     # コンポーネント本体
│   │   └── ...              # その他のコンポーネント
│   ├── constants/           # 定数定義
│   ├── definitions/         # 型定義
│   ├── entries/             # エントリーポイント
│   │   ├── content.ts       # content.js用のエントリーポイント
│   │   └── ...              # その他のエントリーポイント
│   ├── exceptions/          # カスタム例外クラス
│   ├── features/            # 機能単位のモジュール
│   │   └── something/       # 機能のディレクトリ
│   │       ├── components/  # 機能固有のコンポーネント
│   │       │   ├── Something/
│   │       │   │   └── index.ts
│   │       │   └── index.ts
│   │       ├── constants/   # 機能固有の定数
│   │       │   ├── index.ts
│   │       │   └── something.ts
│   │       ├── definitions/ # 機能固有の型定義
│   │       │   ├── index.ts
│   │       │   └── something.ts
│   │       ├── ...
│   │       └── index.ts      # 機能のエントリーポイント
│   └── utilities/            # ユーティリティ関数
├── eslint.config.mjs         # ESLint設定
├── package.json              # プロジェクト設定
├── tsconfig.json             # TypeScript設定
└── vite.config.ts            # Vite設定

```

### 開発指針

1. コンポーネント開発

   - 単一責務の原則に従ったコンポーネント設計
   - 適切な型定義の提供
   - コンポーネントの再利用性の確保
   - スタイリングの一貫性維持

2. 機能実装（features/）

   - 機能単位でのモジュール分割
   - 関連するコンポーネント、定数、型定義の集約
   - 明確な依存関係の管理

3. 例外処理

   - カスタム例外クラスの活用
   - 統一的なエラーハンドリング
   - ユーザーフレンドリーなエラーメッセージ
   - エラーのログ管理

4. ビルドプロセス
   - Vite による効率的なバンドル
   - 環境別の最適化設定
   - アセットの最適化
   - ソースマップの生成

## 開発フロー

1. 環境セットアップ

   ```bash
   # プロジェクトの依存関係インストール
   npm install

   # 開発サーバーの起動
   npm run dev

   # プロダクションビルド
   npm run build
   ```

2. 実装

   - コンポーネントの開発
   - 機能モジュールの実装
   - マニフェストの設定
   - TypeScript 型定義の整備

3. テスト

   - ユニットテスト

4. デプロイ
   - プロダクションビルド
   - パッケージング
   - Chrome Web Store への公開準備

## コーディング規約

1. TypeScript

   - 厳格な型チェックの有効化
   - インターフェースの適切な活用
     - 基本は`interface`ではなく、`type`で統一
   - 型推論の活用
   - 明示的な型定義の提供

2. コンポーネント

   - 機能単位での分割
   - Props 型の明示的な定義
   - 副作用の適切な管理
   - メモ化の活用

3. スタイリング
   - CSS モジュールの活用
   - テーマ変数の使用
   - レスポンシブデザインの考慮
   - アクセシビリティへの配慮

## Tips

- Chrome 拡張機能のデバッグ: chrome://extensions/
- Vite 開発サーバーの活用

## 参考資料

- [Chrome Extensions Documentation](https://developer.chrome.com/docs/extensions/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Vite Documentation](https://vitejs.dev/guide/)
- [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
