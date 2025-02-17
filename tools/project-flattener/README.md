# Project Flattener

ディレクトリ構造をフラット化と、ディレクトリ構造のテキストファイルを出力するツールです。

## 機能

- ディレクトリ構造をフラットな形式に変換
- `.gitignore`に記載されたファイル・ディレクトリを除外
- 正規表現パターンによるファイル・ディレクトリの除外
- `index.*`ファイルを親ディレクトリ名に基づいてリネーム（例: `components/index.ts` → `components.ts`）
- 元のディレクトリ構造を`ディレクトリ構造.txt`として出力

## 使用方法

```bash
python3 flattener.py [source_dir] [output_dir] -e 'package-lock\.json$' '\.(svg|png|gif)$'
```
