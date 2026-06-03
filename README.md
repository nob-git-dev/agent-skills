# claude-skills

> **AI にコードを「書かせる」ためではなく、AI と「規律をもって開発する」ための Claude Code 拡張集。**

AI エージェントはコードを速く書けます。しかしその速さは、放っておくと**そのまま事故の速さ**になります。
このリポジトリは、AI の実行力を活かしながら、**品質・安全・保守性を人間が握り続ける**ための
スキル・サブエージェント・フックを提供します。

---

## なぜ作ったか — Vibe Coding の先にある課題

「AI に頼めば動くものができる」——この体験（**Vibe Coding**）は、開発の敷居を劇的に下げました。
エンジニアでなくてもアイデアをソフトウェアにできる。これは「**床を上げた**」と言えます。

しかし、本番で使えるソフトウェアには別の規律が要ります。Andrej Karpathy はこれを
**Agentic Engineering**——「失敗しうるエージェントを調整し、品質・セキュリティ・保守性を
保ちながら**天井を上げる**専門的規律」——と整理しました。その本質は、エージェントに丸投げせず、
**仕様・計画・検証・権限・レビュー・理解を人間が握り続けること**です。

このリポジトリの開発者自身、AI に開発を任せる中で**本番データベースの全消失を短期間に 2 回**
経験しました。`CLAUDE.md` にルールを書いても、メモリに記録しても、防げませんでした。

そこで得た結論はシンプルです:

> **ルールを「書いて渡す」のではなく、プロセスを「守らざるを得ない構造」にする。**

「守ろうと思う」だけでは、人も AI も忘れます。だから構造で強制します。

---

## 3 つの柱

### 1. Supervisor — 常駐する「最初の窓口」

スキルは**呼ばれなければ何もしません**。Supervisor はすべての発言を受け取り、意図を分類し
（開発か / 質問か / 危険な操作か）、危険信号（削除・本番・マイグレーション等）を手前で止め、
**承認なしには次に進みません**。「気づいたら実行されていた」を構造的に防ぎます。

### 2. SDLC オーケストレーション — 仕様書が開発を駆動する

`SPEC.md`（仕様書）を唯一の真実（Single Source of Truth）とし、
`仕様 → 設計 → 実装 → レビュー → デプロイ` を**品質ゲート**で進めます。
各フェーズは `context: fork` で隔離実行され、引き継ぎは SPEC.md と git だけを経由します。
完了は「動いた」ではなく、**受け入れ条件を一つずつ照合して**判断します。

### 3. 行動の憲法 — 失敗から確立した判断軸（全 12 条）

ルールの羅列ではなく、**「なぜ守るか（経緯と本質）」を保持する上位原則**です。
実プロジェクトの失敗から条文化されました。一部を挙げると:

- **検証した事実だけに従う** — 表示・記憶・未実行の結果は「主張」。検証した値だけを事実とする
- **リスクに比例して検証を厚くする** — 読むだけは速く、消す / 本番に触れるほど段数を増やす
- **権威ある定義元を当たる** — 手探りや記憶でなく、一次情報（ソース・定義・実データ）を先に読む
- **借り物の解は適用条件を照合する** — 「少量向け」の手法を本番規模で検算せずに使わない
- **本番影響は能動的に壊しにいって検証する** — 「動く」ではなく「壊せない」を確かめてから出す

ほかに、全層を掃いて完了する / 対症でなく根治へ / 公式の継ぎ目を尊重する / 判断を外在化する /
agent-native に作る——など、計 12 条。詳細は
[`sdlc-skills/docs/work-constitution.md`](sdlc-skills/docs/work-constitution.md)。

---

## 思想の系譜

| 源流 | 受け継いだもの |
|---|---|
| Andrej Karpathy "Agentic Engineering" | 天井を上げる規律。仕様・検証・レビュー・理解を人間が握る |
| 古典的ソフトウェア工学 | Uncle Bob（TDD 三法則）/ Kent Beck / Fowler（リファクタリング）/ Evans（DDD）/ Google SRE |
| 実プロジェクトの失敗 | 本番事故から条文化した「行動の憲法」（経緯と本質を保持） |

設計判断の詳細: [`sdlc-skills/docs/design-decisions.md`](sdlc-skills/docs/design-decisions.md)

---

## 収録スキルセット

各スキルセットは独立したサブディレクトリに収録されています。

| ディレクトリ | 内容 |
|---|---|
| **[sdlc-skills/](sdlc-skills/)** | SDLC を仕様書中心に規律正しく進めるスキルセット。12 スキル（`/sdlc` `/spec` `/architect` `/tdd` `/review` `/security` `/deploy` ほか）+ 4 サブエージェント + 3 フック + 行動の憲法。**まずここを参照してください** |
| **[learning-skills/](learning-skills/)** | 完了したプロジェクトから AI 自身の挙動を学習し、**人間のゲートを通して**改善する自己改善パイプライン。3 スキル（`/post-project-learning-engine` `/skill-proposal-engine` `/skill-regression-checker`）。`観測 → 抽出 → 提案 → 回帰検査` の多段ゲートで、学習の暴走（過剰一般化・肥大化・回帰）を防ぐ。sdlc-skills と合わせて「やる → やり方を直す」の閉ループになる |
| [dgx-update-check/](dgx-update-check/) | **特定ハードウェア向け運用スキルの実例**。DGX Spark（GX10）のシステムアップデートを、ブラウザ・ダッシュボードのボタンを押す **前に**「何が来ているか」を **副作用ゼロ・read-only** で覗き見る単体スキル。`apt update` の体験を DGX OTA 文脈で再現。決定的なデータ層と判断層の二層分離で安全を構造的に担保。ARM64 / Ubuntu 24.04 / DGX Spark 専用。sdlc-skills の SDLC オーケストレーションで開発された応用例でもある |

---

## クイックスタート

```bash
git clone https://github.com/nob-git-dev/claude-skills.git
cd claude-skills/sdlc-skills
./scripts/install.sh
```

インストール後、`~/.claude/settings.json` に Supervisor とフックを追加します
（テンプレートと詳細は [sdlc-skills/README.md](sdlc-skills/README.md)）。
次回 `claude` 起動時から Supervisor が常駐し、開発タスクを自動的に `/sdlc` へ誘導します。

### 特定のスキルセットだけ取得（sparse-checkout）

```bash
git clone --no-checkout https://github.com/nob-git-dev/claude-skills.git
cd claude-skills
git sparse-checkout init --cone
git sparse-checkout set sdlc-skills
git checkout main
cd sdlc-skills
./scripts/install.sh
```

> **`install.sh` は `skills/` `agents/` `hooks/` のみを `~/.claude/` に展開し、
> あなたの `CLAUDE.md` や憲法ファイルは一切上書きしません。** 判断の原則・行動の憲法の導入は
> 内容を確認のうえ手動で行います（各スキルセットの README 参照）。

---

## ライセンス

各スキルセットのディレクトリ内の `LICENSE` を参照してください。
いずれのスキルセットも、個人・研究・非営利は **CC BY-NC-SA 4.0**（無償）、営利利用は**商用ライセンス**（要申請）です。
ライセンス本文: [sdlc-skills](sdlc-skills/LICENSE) / [learning-skills](learning-skills/LICENSE) / [dgx-update-check](dgx-update-check/LICENSE)。
