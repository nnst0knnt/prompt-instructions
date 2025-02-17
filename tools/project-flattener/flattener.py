import os
import shutil
from pathlib import Path
from typing import Set, List, Pattern
import re
import argparse


class Flattener:
    def __init__(
        self, source_dir: str, output_dir: str, exclude_patterns: List[str] = None
    ):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.gitignore_patterns = self._load_gitignore()
        self.exclude_patterns = [
            re.compile(pattern) for pattern in (exclude_patterns or [])
        ]

    def _load_gitignore(self) -> Set[str]:
        """
        .gitignoreファイルを読み込んでパターンのセットを返す
        """
        gitignore_path = self.source_dir / ".gitignore"
        patterns = set()

        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # **/ のような形式を.*/ に変換
                        line = line.replace("**/", ".*/")
                        # *.ext の形式を .* に変換
                        line = line.replace("*", ".*")
                        patterns.add(line)

        return patterns

    def _is_ignored(self, path: str) -> bool:
        """
        パスが以下のいずれかに該当する場合に除外:
        - .gitignoreのパターンにマッチ
        - 除外パターンにマッチ
        """
        # .gitignoreパターンのチェック
        for pattern in self.gitignore_patterns:
            if re.search(pattern, path):
                return True

        # 除外パターンのチェック
        for pattern in self.exclude_patterns:
            if pattern.search(path):
                return True

        return False

    def _get_filename(self, file_path: Path) -> str:
        """
        出力先のファイル名を生成
        index.**系のファイルはディレクトリ名を使用
        """
        if file_path.name.startswith("index."):
            # index.tsなどの場合、親ディレクトリ名を使用
            parent_dir = file_path.parent.name
            return f"{parent_dir}{file_path.suffix}"
        return file_path.name

    def _prepare_output_dir(self) -> Path:
        """
        出力ディレクトリを準備する
        """
        if self.output_dir.name == "knowledge":
            # 出力先がknowledgeディレクトリの場合
            target_dir = self.output_dir
            if target_dir.exists():
                # 既存のファイルをすべて削除
                for item in target_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            else:
                target_dir.mkdir(parents=True)
        else:
            # knowledgeディレクトリを作成する場合
            target_dir = self.output_dir / "knowledge"
            if target_dir.exists():
                # 既存のファイルをすべて削除
                for item in target_dir.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
            else:
                target_dir.mkdir(parents=True)

        return target_dir

    def _generate_tree(
        self, start_path: Path = None, prefix: str = "", is_last: bool = True
    ) -> List[str]:
        """
        ディレクトリ構造をツリー形式で生成
        """
        if start_path is None:
            start_path = self.source_dir

        tree_lines = []
        contents = sorted(list(start_path.iterdir()))

        for i, item in enumerate(contents):
            is_last_item = i == len(contents) - 1
            current_prefix = "└── " if is_last_item else "├── "
            next_prefix = "    " if is_last_item else "│   "

            # 除外パターンのチェック
            if self._is_ignored(str(item.relative_to(self.source_dir))):
                continue

            tree_lines.append(f"{prefix}{current_prefix}{item.name}")

            if item.is_dir():
                tree_lines.extend(
                    self._generate_tree(item, prefix + next_prefix, is_last_item)
                )

        return tree_lines

    def flatten(self):
        """
        プロジェクトをフラット化する
        """
        # 出力ディレクトリを準備
        target_dir = self._prepare_output_dir()

        # ツリー構造を生成
        tree_lines = [".", *self._generate_tree()]

        # ツリー構造をファイルに保存
        tree_file_path = target_dir / "ディレクトリ構造.txt"
        with open(tree_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(tree_lines))

        # プロジェクト内のファイルを走査
        for root, _dirs, files in os.walk(self.source_dir):
            rel_path = os.path.relpath(root, self.source_dir)

            # 除外パターンのチェック
            if self._is_ignored(rel_path):
                continue

            for file in files:
                file_path = Path(root) / file
                rel_file_path = file_path.relative_to(self.source_dir)

                # 除外パターンのチェック
                if self._is_ignored(str(rel_file_path)):
                    continue

                # 出力先のファイル名を決定
                target_filename = self._get_filename(file_path)
                target_path = target_dir / target_filename

                # ファイルをコピー
                shutil.copy2(file_path, target_path)
                print(f"Copied: {rel_file_path} -> {target_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="プロジェクトのファイルをフラット化します"
    )
    parser.add_argument("source_dir", help="ソースディレクトリのパス")
    parser.add_argument("output_dir", help="出力先ディレクトリのパス")
    parser.add_argument(
        "-e",
        "--exclude-patterns",
        nargs="+",
        help="除外するパスのパターンのリスト（正規表現）",
        default=[],
    )

    args = parser.parse_args()

    try:
        flattener = Flattener(
            args.source_dir, args.output_dir, exclude_patterns=args.exclude_patterns
        )
        flattener.flatten()
    except re.error as e:
        print(f"Error: 無効な正規表現パターンが指定されました: {e}")
        exit(1)


if __name__ == "__main__":
    main()
