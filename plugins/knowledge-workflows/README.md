# Knowledge Workflows

日本語の要約、根拠に基づく執筆、編集、ビジネス文書化、対話型学習をまとめたChatGPT / Codex向けプラグインです。

## 収録スキル

| Skill | Purpose |
|---|---|
| `make-clear-summary` | 複雑な素材を、短時間で意味がつかめる段階的な要約へ変える |
| `make-1-3-1-summary` | 1文の要旨・最大3点・必要なら1つの注意点で素早く整理する |
| `summarize` | 指定文字数の中で、読み手に伝わる要約を作る |
| `write-from-evidence` | 根拠と主張の対応を保ち、事実・解釈・仮説・提案を分けて書く |
| `write-clear-business-docs` | 会話やメモを、第三者に伝わる日本語ビジネス文書へ変える |
| `edit-speech-transcripts` | 発話内容を保ちながら、日本語の音声書き起こしを校正する |
| `edit-with-editing-engineering` | 編集工学の方法で、文章の関係・構成・価値を再設計する |
| `learn-quiz` | 質問と理解度チェックを通して、素材を能動的に学ぶ |

## インストール

```bash
codex plugin marketplace add nob-git-dev/agent-skills --ref main
codex plugin add knowledge-workflows@agent-skills
```

インストール後にChatGPTデスクトップアプリを再起動し、プラグインを有効にしてください。

## 呼び出し例

```text
$knowledge-workflows:make-clear-summary この資料を短時間で理解できるように要約してください。
$knowledge-workflows:make-1-3-1-summary この議事録を1-3-1形式で整理してください。
$knowledge-workflows:write-from-evidence この根拠資料から報告書を作成してください。
$knowledge-workflows:write-clear-business-docs このメモをビジネス文書として整理してください。
```

自然な日本語で依頼しても、内容に合うスキルが選ばれます。形式を固定したい場合は、上記のようにスキル名を明示してください。

## ライセンス

リポジトリ直下の [LICENSE](../../LICENSE) と [LICENSE-COMMERCIAL.md](../../LICENSE-COMMERCIAL.md) が適用されます。
