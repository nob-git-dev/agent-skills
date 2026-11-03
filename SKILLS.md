# AI向けスキル選択ガイド

このリポジトリを初めて読むAIは、ここで依頼に合う入口を選び、選んだSKILL.mdを全文読んでください。機械処理用の同じ入口は[skills-index.json](skills-index.json)です。全スキルを一括で読み込む必要はありません。

## 選び方

1. 今回の依頼の成果を特定する。例：設計案、実装、レビュー、要約、全文校正。
2. 下の表と索引のdescriptionから、最も狭く適合するスキルを選ぶ。
3. SKILL.mdを読む。そのファイルを基準に、必要な参照資料だけを開く。
4. 複数を使う場合は役割を分ける。自動的に大きな開発工程へ拡大しない。
5. 参照したファイル、判断、実施した確認を必要な範囲で結果に残す。読めなかった資料を読んだとしない。

## UIの設計と実装

| 依頼 | 選ぶ入口 | 読んだ後の動き |
|---|---|---|
| 見た目・世界観・情報の強弱・メニュー・設定・入力・多言語などの設計案やレビュー | [design-ui-from-patterns](skills/design-ui-from-patterns/SKILL.md) | 課題の参照表からパターンと事例を読み、条件・例外・確認方法を使う |
| Reactコンポーネント、画面の実装、状態・操作・アクセシビリティの実装確認 | [ui](skills/ui/SKILL.md) | 既存コードと要件に沿って実装・検証する |
| 設計から実装まで | 上記2つを必要に応じて組み合わせる | 設計の採用案と受け入れ条件を実装へ渡す。二重の確認工程を機械的に増やさない |
| UIが登場するだけの文章の要約や、バックエンドのみの修正 | 下の該当する入口 | UIスキルを語句だけで起動しない |

新スキルはゲームUIの原稿から作った24の設計パターンを収録しています。作品を見た目ごと模倣するのではなく、目的・条件・具体的な工夫・例外を合わせて使います。ペルソナ、The Last of Us Part I、スマブラ、初代バイオハザードなどは[事例索引](skills/design-ui-from-patterns/references/case-index.md)から探せます。

## ソフトウェア開発

| 依頼の中心 | 入口 |
|---|---|
| 開発全体の工程・リスク管理を依頼された | [sdlc](skills/sdlc/SKILL.md) |
| 目的・振る舞い・受け入れ条件を仕様にする | [spec](skills/spec/SKILL.md) |
| 境界・依存関係・設計判断 | [architect](skills/architect/SKILL.md) |
| 業務用語・コンテキスト・集約 | [ddd](skills/ddd/SKILL.md) |
| 要求から観測・証拠・テスト義務を定義 | [test-contract](skills/test-contract/SKILL.md) |
| テスト義務に基づいて実装を進める | [tdd](skills/tdd/SKILL.md) |
| コードの正確性・保守性等をレビュー | [review](skills/review/SKILL.md) |
| 脅威、権限、依存関係、秘密情報、濫用 | [security](skills/security/SKILL.md) |
| リリース・段階展開・ロールバック | [deploy](skills/deploy/SKILL.md) |
| ログ・メトリクス・トレース・アラート | [observe](skills/observe/SKILL.md) |
| SLO、障害対応、運用改善 | [sre](skills/sre/SKILL.md) |
| 振る舞いを保つ構造改善 | [refactor](skills/refactor/SKILL.md) |

## 日本語の知識・文章・学習

| 依頼の中心 | 入口 |
|---|---|
| 自然な長さで分かりやすく要約 | [make-clear-summary](plugins/knowledge-workflows/skills/make-clear-summary/SKILL.md) |
| 1文・最大3点・1つの注意という形式 | [make-1-3-1-summary](plugins/knowledge-workflows/skills/make-1-3-1-summary/SKILL.md) |
| 指定文字数で伝える要約 | [summarize](plugins/knowledge-workflows/skills/summarize/SKILL.md) |
| 根拠・解釈・仮説を分けて文章を書く | [write-from-evidence](plugins/knowledge-workflows/skills/write-from-evidence/SKILL.md) |
| 第三者に伝わるビジネス文書 | [write-clear-business-docs](skills/write-clear-business-docs/SKILL.md) |
| 発言と順序を残して文字起こしを全文校正 | [edit-speech-transcripts](skills/edit-speech-transcripts/SKILL.md) |
| 見方・構成・関係を組み替える編集 | [edit-with-editing-engineering](skills/edit-with-editing-engineering/SKILL.md) |
| 完成した作業を対話・問題で理解する | [learn-quiz](plugins/knowledge-workflows/skills/learn-quiz/SKILL.md) |

要約と全文校正は別の仕事です。短くする依頼がない全文校正で内容を削らないでください。

## エージェントの学習・評価

| 依頼の中心 | 入口 |
|---|---|
| 完了案件から学習候補を抽出 | [post-project-learning-engine](skills/post-project-learning-engine/SKILL.md) |
| 複数の学習候補からスキルへの反映案を選ぶ | [skill-proposal-engine](skills/skill-proposal-engine/SKILL.md) |
| 更新案の回帰・矛盾・過剰一般化を検査 | [skill-regression-checker](skills/skill-regression-checker/SKILL.md) |
| Japanese LLM Benchmarkを実行・比較 | [jlmb](skills/jlmb/SKILL.md) |

## 同名のスキル

edit-speech-transcripts、edit-with-editing-engineering、write-clear-business-docsには、独立版とknowledge-workflowsプラグイン版があります。索引では独立版を入口、プラグイン版をaliasとして示します。既に導入済みの版があればそれを使い、同名の二つを同時に起動しないでください。

## ファイルを読み分けられないAI

UI設計については[統合版](dist/design-ui-from-patterns.md)、または[校正版原稿を含む統合版](dist/design-ui-from-patterns-with-source.md)を渡せます。通常版も全24パターン・事例・確認方法を含みます。原稿の直接引用や校正判断には原稿付き版を使います。

統合版はそのAIの指示・参考資料として渡すものです。スキルの自動選択、ファイル操作、ツール実行がそのAIへ新たに実装されるわけではありません。詳しくは[他のAIでの利用方法](docs/using-with-other-agents.md)を読んでください。
