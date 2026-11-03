# 他のAIで使う

## 入口を渡す

リポジトリを読めるAIには、次のように依頼できます。

> https://github.com/nob-git-dev/agent-skills のSKILLS.mdを読み、私の依頼に合う最小限のスキルを選んでください。選んだSKILL.mdを全文読み、必要な参照ファイルを読んで作業してください。今回は［目的と対象］をお願いします。

機械的に探索する場合はskills-index.jsonのskills[].descriptionで候補を絞り、entrypointを読みます。directoryは同梱ファイルを含む単位、aliasesは同じスキルの別配布先です。パスの基準はリポジトリのルート。全スキルの内容を最初から読み込む必要はありません。

同一作業では同じブランチまたはコミットのファイルを参照してください。再現が必要なときはコミットを固定します。APIやブラウザで直接読む際も相対リンクを元ファイル基準で解決します。リンク先を読めないAIには、フォルダまたは統合版を渡してください。

## スキルを導入できるAI

必要なskills/<name>/をフォルダごとコピー・登録します。SKILL.mdのみのコピーでは参照資料が欠けます。nameとdescriptionが発見の入口で、SKILL.mdの本文が作業手順です。referencesは必要に応じて読む同梱知識です。

| 環境 | 共通して渡すもの | 環境側で必要なこと |
|---|---|---|
| Codex | スキルフォルダ一式 | 利用中クライアントのスキル登録方法に従う |
| Claude Code等、同形式を読むエージェント | 同じフォルダ一式 | 各製品のスキル配置・読込方法に従う |
| 独自エージェント／ローカルLLM | description索引、選んだSKILL.md、必要な参照資料 | 呼び出し側が選択とファイル読込を行う |
| ファイルを読み分けないチャット | 統合Markdown | 今回の指示・資料としてコンテキストに渡す |

agents/openai.yamlは対応製品の表示用補助情報です。対応しないAIは無視できます。特定モデル、APIキー、Figma、MCP、ChatGPT内のファイルIDは、このスキルの必須条件にしていません。導入できることと、異なるモデルで同じ判断品質が得られることは別なので、実際に使うAIでも代表課題で確認してください。

## UI設計スキルの読み分け

- 入口：skills/design-ui-from-patterns/SKILL.md
- 世界観・文字・色・優先順位・HUD：references/visual-design.md
- 待ち時間・入力・初期導線・ヘルプ：references/interaction.md
- 調整・プレビュー・支援：references/settings-accessibility.md
- 作品名から探す：references/case-index.md
- 提案後の確認：references/review.md
- 発言へ戻る：references/source.mdから校正版・原文・対応記録を読む

上記のreferencesへのパスはスキルのフォルダを基準とします。原稿の解説と、編者が加えた応用・確認方法を区別してください。画像・動画を同梱していないため、作品の正確な画面再現をこの資料だけで済ませたとしないでください。

React等の実装が必要なら、設計の採用案・例外・受け入れ条件をskills/uiへ渡せます。設計だけなら実装用のスキルまで強制的に読み込む必要はありません。

## 統合版を作る・更新する

正本はスキルのフォルダです。Python 3.9以降の標準ライブラリだけで生成できます。

~~~bash
python3 skills/design-ui-from-patterns/scripts/export_portable.py --output dist/design-ui-from-patterns.md
python3 skills/design-ui-from-patterns/scripts/export_portable.py --include-source --output dist/design-ui-from-patterns-with-source.md
~~~

通常版は設計の本文・全パターン・事例・確認・出典の案内を含みます。原稿付き版は校正版228行も含みます。原文と詳細な校正記録はフォルダ側に保持します。通常版から原稿を直接引用したり、原文を照合済みとしたりしないでください。

内部リンクは統合文書内のアンカーへ変換されます。収録しない監査資料へのリンクは、正本内の任意資料であることを示す文言になります。各部分には生成元の相対パスと内容ハッシュを記録します。

統合版を直接手直しせず、元ファイルを修正して再生成します。既存ファイルが最新かだけを確認する場合は上の各コマンドに--checkを付けます。

## スキルを追加したとき

~~~bash
python3 scripts/build_skill_catalog.py
python3 scripts/build_skill_catalog.py --check
python3 skills/design-ui-from-patterns/scripts/validate_package.py
~~~

索引は現在のSKILL.mdのname・description・pathから生成します。新規の同名スキルは自動的に別物と扱わず、エラーとして確認します。メタデータは単純文字列または複数行ブロックを使い、複雑なYAML構造は加えないでください。

スキルの内容を変更した場合は、形式だけでなく代表的な依頼で使い方も確認してください。[今回の試行条件](../evals/design-ui-from-patterns/cases.json)と[結果](../evals/design-ui-from-patterns/results.md)は、他のAIで再確認する出発点になります。
