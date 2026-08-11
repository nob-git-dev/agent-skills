---
name: tdd
description: Test Contractまたは受け入れ条件からProof Obligationを選び、Red-Green-RefactorでMinimum Sufficient Changeを実装する。Required ObservableをEvidence付きでPASSへ変え、回帰防止と検証可能な実装を進める時に使う。
---

# Contract-Driven TDD スペシャリスト

Test Contractで固定された「何を証明するか」を、Proof Obligation単位の小さなRed-Green-Refactorへ変換する。TDDの作業単位はシステム全体ではなく、原則として1つの未達Proof Obligationである。

## ポータブル実行ルール

- 現在のユーザー依頼、利用中クライアントの権限規則、リポジトリ内の指示を優先する。特定のエージェント製品、呼び出し構文、サブエージェントを前提にしない。
- ユーザーが明示的に依頼しない限り、`git add`、`git commit`、`git push`、デプロイ、外部書き込み、破壊的操作を実行しない。
- 固定のタスク管理方法、ホームディレクトリ、ポート、モデル、コンテナ、サービス名を仮定しない。環境依存情報は実際の設定と観測で確認する。
- 固定Requirement、Required Observable、Required Test、公開契約を実装都合で変更しない。変更が必要ならTDDを停止し、理由と影響を報告する。
- 未コミット変更をユーザーの作業として保全し、選択したPOに不要なファイルを編集しない。

## 1. 入力契約を選ぶ

次の優先順位で入力を決める。

1. `TEST_CONTRACT.md`、または `SPEC.md` 内にTest Contractがある場合は、それをRequired Observable、Proof Obligation、Evidence要件、固定制約の正典として使う。
2. Test Contractがなく、`test-contract` スキルを利用できる場合は、本番コードへ着手する前にその工程を実行する。ファイル更新が許可されていなければ、結果を一時的な入力契約として保持する。
3. `test-contract` を利用できない場合は後方互換モードを使う。`SPEC.md` の受け入れ条件、または現在の依頼から、最低限の Requirement、Observable、Expected Result、Verification、Proof Obligationを内部生成して従来のTDDを継続する。

Test Contractがないことだけを理由に、既存の `SPEC.md -> acceptance criteria -> TDD` フローを停止しない。ただしRequirementが矛盾する、期待結果が観測不能である、または結果を変える情報が欠ける場合は `MISSING_CONTEXT` または `BLOCKED` とする。

## 2. 品質制約とMinimum Sufficient Change

次は最適化対象ではなくHard Constraintである。

```text
Required Observable = PASS
AND Fixed Requirements are preserved
AND Required Regression Tests = PASS
AND Required Security / Reliability Gates = PASS
```

Greenで行うのはMinimum Sufficient Changeである。

> 現在のProof Obligationを満たすために必要十分であり、かつ既存契約を破壊しない最小の変更。

変更ファイル数、LOC、コンテキスト、テスト時間、再試行を小さくするのは、Hard Constraintを満たす範囲に限る。トークンや時間の削減を理由にRequired Testを省略しない。

## 3. 最初に確認すること

1. `SPEC.md` とTest Contractを読み、Requirement、固定要件、スコープ外を確認する。
2. Required ObservableとPOの対応が追跡可能か確認する。
3. 既存テスト規約、テスト環境、対象コードの設計パターンを確認する。
4. 未達POを1つ選び、現在Evidenceと期待結果を確認する。
5. POに必要な最小コンテキストと編集候補を、参照・呼出し関係などの根拠から特定する。

リポジトリ全体を無制限に探索・編集しない。範囲外の依存が必要と分かった場合は、理由と影響を示して関連コンテキストまたは許可範囲を更新する。

## 4. TDDの三法則

1. 失敗するテストを書くまで、本番コードを書かない。
2. 失敗を示すのに必要な量を超えてテストを書かない。コンパイルエラーも失敗とみなす。
3. 現在失敗しているテストを通すのに必要な量を超えて本番コードを書かない。

既存の失敗テストや再現コマンドがPOを直接証明する場合、それをRedのEvidenceとして利用できる。意味のない重複テストは追加しない。

## 5. Proof Obligation単位の実行フロー

```text
[1] SPEC / Test Contractを読む
  -> [2] Required Observablesを確認
  -> [3] 未達Proof Obligationを1つ選ぶ
  -> [4] 必要最小コンテキストを特定
  -> [5] Redを実行し、期待した理由でFAILすることを確認
  -> [6] Minimum Sufficient Changeを実装
  -> [7] 対象テストを実行してGreenを確認
  -> [8] 必要な場合だけ小さくRefactorし、Greenを再確認
  -> [9] Evidenceを記録
  -> [10] Observable状態を更新
  -> [11] Stop Conditionを評価
  -> [12] 次の未達POへ進む
  -> [13] Required Outer Gateを実行
  -> [14] Acceptance MatrixとVerdictを確定
```

### Red

- ObservableのScenarioとExpected Resultへ直接対応するテストまたはHarnessを用いる。
- テストを実行し、対象挙動が未実装または壊れているためにFAILすることを確認する。
- 誤ったfixture、環境不備、無関係なエラーなら製品コードを変更せず、Evidenceを `INVALID_EVIDENCE` または `BLOCKED` とする。
- 既にPASSする場合は、そのEvidenceがObservableを十分に覆うか確認する。覆うなら不要な変更を行わない。

### Green

- 現在のPOをPASSへ変えるMinimum Sufficient Changeだけを実装する。
- Required Test、Expected Result、fixtureを都合よく弱めない。
- PO外のリファクタ、別機能、ついで修正を混ぜない。
- 固定要件を満たせない場合は代替へ黙って切り替えず、停止して報告する。

### Refactor

- Greenを保ったまま、今回の変更が生んだ重複、読みにくさ、明白な構造上の問題だけを改善する。
- 別の振る舞い、広い設計変更、契約変更が必要なら別POまたは明示されたRefactor工程へ分ける。
- Refactor後に対象テストと必要な回帰テストを再実行する。

## 6. Inner LoopとOuter Gate

Inner LoopはUnit、API contract、小さな状態挙動、pure function、validationなど、POごとに高速に回す。

Outer GateはIntegration、E2E、Browser、OS sandbox、durability、load、security、external systemなど、高コストまたは環境依存の検証に使う。各Inner Loopで無条件に全Outer Gateを実行せず、Test Contractに定義された時点と最終ゲートで実行する。

Required Outer Gateを実行できなければ、一般テストがPASSでも対象RequirementをPASSにしない。

## 7. テスト環境の分離

- テスト用リソースが本番から分離されていることを、名前だけでなく設定と観測で確認する。
- テストデータは可能な限りテスト内で作成・破棄する。
- 外部副作用、課金、通知、永続データ、権限境界へ影響するテストは、モック、sandbox、専用環境、明示承認など適切なSafety Harnessを使う。
- テスト実行自体が破壊的または本番影響を持つ場合は、実行せず必要な承認と安全条件を示す。

## 8. Evidenceを残す

各Observableについて、利用可能な範囲で次を記録する。

- 実行コマンド
- exit code
- test / harness名
- actual resultまたは観測値
- timestamp / environment
- covered observable
- statusと失敗理由

「テスト済み」という自然言語だけをEvidenceにしない。EvidenceがObservableを直接証明しない場合は `INVALID_EVIDENCE` または `UNVERIFIED` とする。

## 9. Acceptance MatrixとVerdict

```markdown
| Requirement | Observable | Proof Obligation | Evidence | Status |
|---|---|---|---|---|
| R-001 | O-001 valid PDF -> 200 | PO-001 | test_pdf_valid, exit 0 | PASS |
| R-001 | O-002 invalid ext -> 422 | PO-002 | test_invalid_ext, exit 0 | PASS |
| R-002 | O-003 cancellation | PO-003 | - | UNVERIFIED |
```

状態は `PASS`、`FAIL`、`UNVERIFIED`、`BLOCKED`、`INVALID_EVIDENCE` とする。Required Observableが一つでもPASS以外なら、対応Requirement全体をPASSにしない。全体テストスイートのPASSは、未対応Observableの代替Evidenceにならない。

Judge責務では、実装者の自己申告ではなくEvidenceと固定制約からVerdictを決める。別エージェントは必須ではないが、契約設計、実装、合否判定の論理的責務は分離する。

## 10. Stop Condition

次をすべて満たした時点で、現在のPOに対する実装を停止する。

```text
Required Observable = PASS
AND Required Regression = PASS
AND Fixed Constraints = preserved
```

停止後に追加改善を続けない。次のPOへ進むか、必要な改善を別POまたはRefactor工程として明示する。すべてのRequired ObservableとOuter GateがPASSし、固定要件が維持されて初めてRequirementを完了とする。

## アンチパターン

- 本番コードを先に書き、実装に合わせてテストを後付けする
- Redを確認せず、テストが証明能力を持つと仮定する
- GreenにするためRequired Test、Observable、Expected Resultを弱める
- 1つのPOを口実にリポジトリ全体を探索・編集する
- PO外のリファクタや別機能を混ぜる
- Required Outer Gateを速度やトークンのために省略する
- コマンド、exit code、対象Observableのない「テスト済み」をEvidenceにする
- 未検証ObservableがあるのにRequirementをPASSと判定する
