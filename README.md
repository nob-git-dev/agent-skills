# Agent Skills

> AIにコードを「書かせる」だけでなく、AIエージェントと規律をもって開発・学習・編集するための、独立したAgent Skills集。

全体ポートフォリオ: [AI Agent Engineering Portfolio](https://github.com/nob-git-dev/ai-agent-portfolio)

このリポジトリは、各スキルを `skills/<skill-name>/` の1フォルダ単位で公開します。すべてのスキルは [Agent Skills specification](https://agentskills.io/specification) に沿った `SKILL.md` を持ち、対応するエージェントクライアントへ1つずつ導入できます。

特定のマシンやローカル環境を整備するスキルは含めていません。ホームディレクトリ、ポート、モデル、サービス構成など、利用者固有の環境を前提にしない構成です。

## 収録スキル

### Software delivery

| Skill | Purpose |
|---|---|
| [sdlc](skills/sdlc/) | リスクに応じて仕様・設計・実装・レビュー・デプロイを統制する |
| [spec](skills/spec/) | 目的、振る舞い、受け入れ条件、固定要件を仕様へ落とす |
| [architect](skills/architect/) | 境界、依存方向、影響範囲、ADRを設計する |
| [ddd](skills/ddd/) | ユビキタス言語、コンテキスト、集約を設計する |
| [tdd](skills/tdd/) | 受け入れ条件をテストへ変換し、Red-Green-Refactorで実装する |
| [ui](skills/ui/) | UI/UX、React、アクセシビリティ、操作検証を扱う |
| [review](skills/review/) | 正確性、セキュリティ、性能、保守性、テストをレビューする |
| [security](skills/security/) | 脅威、アクセス制御、依存関係、シークレット、濫用を検証する |
| [deploy](skills/deploy/) | 段階リリース、ヘルスチェック、中断、ロールバックを設計・実行する |
| [observe](skills/observe/) | ログ、メトリクス、トレース、アラートを設計する |
| [sre](skills/sre/) | SLI/SLO、エラーバジェット、障害対応、トイルを扱う |
| [refactor](skills/refactor/) | 振る舞いを保ちながらコード構造を改善する |

### Agent learning

| Skill | Purpose |
|---|---|
| [post-project-learning-engine](skills/post-project-learning-engine/) | 完了案件から次回の行動ルール候補を抽出する |
| [skill-proposal-engine](skills/skill-proposal-engine/) | 複数の学習候補を評価し、適切な反映先とSkill Patchを提案する |
| [skill-regression-checker](skills/skill-regression-checker/) | Skill Patchの回帰、矛盾、過剰一般化、副作用を検査する |

### Writing and editing

| Skill | Purpose |
|---|---|
| [edit-speech-transcripts](skills/edit-speech-transcripts/) | 日本語音声認識の誤りを直し、発話を保った読みやすい記録へ整える |
| [edit-with-editing-engineering](skills/edit-with-editing-engineering/) | 編集工学のアプローチで日本語テキストの関係・構成・価値を再設計する |
| [write-clear-business-docs](skills/write-clear-business-docs/) | 会話や断片情報を第三者に伝わる日本語ビジネス文書へ変換する |

### LLM evaluation

| Skill | Purpose |
|---|---|
| [jlmb](skills/jlmb/) | Japanese LLM Benchmarkを安全かつ再現可能に実行・比較する |

合計19スキルです。

## 設計方針

- **1 skill = 1 directory**: 必要なスキルだけを個別に取得・更新できる
- **Portable core**: 特定エージェント製品のコマンド、フック、サブエージェント構文を必須にしない
- **Safe by default**: コミット、デプロイ、破壊的操作、外部書き込みを暗黙に実行しない
- **Evidence over memory**: 変わり得る環境情報は、記憶ではなく現在の設定と観測で確認する
- **Progressive disclosure**: 長い基準、テンプレート、スクリプトは各スキルの `references/`、`assets/`、`scripts/` に分ける

## インストール

まずリポジトリを取得します。

```bash
git clone https://github.com/nob-git-dev/agent-skills.git
cd agent-skills
```

利用するクライアントのスキル導入方法に従い、必要な `skills/<skill-name>/` ディレクトリだけを登録またはコピーしてください。フォルダ名を変える場合は、`SKILL.md` の `name` も同じ名前に合わせます。

例として、Gitの sparse-checkout なら1スキルだけ取得できます。

```bash
git clone --filter=blob:none --no-checkout https://github.com/nob-git-dev/agent-skills.git
cd agent-skills
git sparse-checkout init --cone
git sparse-checkout set skills/security
git checkout main
```

クライアントが `agents/openai.yaml` を使わない場合、そのファイルは無視して構いません。ポータブルな指示本体は `SKILL.md` です。

## SkillとPluginの違い

Skillは、1つの仕事を行うための独立した指示・参照資料・スクリプトです。Pluginは、複数のSkillやツールをまとめて配布するためのパッケージです。

このリポジトリでは再利用しやすいSkillを1つずつ公開します。必要に応じて、利用するクライアント側で複数スキルをPluginとして束ねられます。

## 安全性

スキルはエージェントの判断を支援しますが、実行環境の権限規則やユーザー承認を置き換えません。特に、削除、データ移行、本番変更、外部送信、長時間の資源占有では、対象・影響・可逆性を確認してください。

JLMBの補助スクリプトはローカルのループバックアドレスを既定とし、APIキーを環境変数から読みます。実行前にコードと依存関係を確認してください。

## ライセンス

個人・研究・非営利利用は [CC BY-NC-SA 4.0](LICENSE) です。営利企業内での利用や商用サービスへの組み込みは [Commercial License](LICENSE-COMMERCIAL.md) を確認してください。
