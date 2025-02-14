# fish 用ツールの作成

## プロジェクト概要

ターミナル上で動作する各種ツールの開発プロジェクト。fish shell をベースに、実用的で使いやすいツールを作成します。

## 基本方針

### 設計原則

1. コマンドラインツールの標準的な作法に従う

   - ヘルプオプション（-h, --help）の提供
   - 一貫性のあるオプション形式（短縮形と完全形）
   - 明確なエラーメッセージ

2. fish shell 特有の考慮事項
   - argparse を活用したオプション解析
   - fish 関数として実装（~/.config/fish/functions/に配置）
   - fish のワイルドカード解釈への対応

### UI/UX 指針

1. 視覚的な分かりやすさ

   - カラー出力の活用（set_color コマンド）
   - 適切な空行による可読性の確保
   - 絵文字やアイコンの効果的な使用

2. 出力形式
   - デフォルトは最も一般的な使用ケースに対応
   - 必要に応じて複数の出力形式を提供（simple, detail, tree など）
   - 整列やフォーマットの一貫性

### 機能設計

1. 柔軟性

   - 複数の入力形式のサポート（ファイル、ディレクトリ）
   - 除外パターンなどのフィルタリング機能
   - オプションによる動作のカスタマイズ

2. エラーハンドリング
   - 明確なエラーメッセージ
   - 不正な入力への適切な対応
   - 存在しないファイル/ディレクトリへの警告

## 開発フロー

1. 要件の明確化
2. 基本機能の実装
3. エッジケースの検証
4. UI/UX の改善
5. ドキュメントの整備

## Tips

- fish 関数の配置場所: `~/.config/fish/functions/`
- オプション解析には `argparse` を優先的に使用
- カラー出力: `set_color` を使用（normal, red, green, yellow, blue, cyan など）
- 出力の整形: `printf` を活用した綺麗な整列
- エラー処理: 適切なステータスコードでの終了（`return 1` など）

## 参考

- [fish shell documentation](https://fishshell.com/docs/current/index.html)
- [GNU core utilities](https://www.gnu.org/software/coreutils/)
- [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
