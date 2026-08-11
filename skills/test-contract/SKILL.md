---
name: test-contract
description: SPEC.mdの要求・受け入れ条件から、完成判定に必要なObservable、Test Scenario、Evidence、Proof Obligationを定義する。TDD実装前に何を証明するかと品質条件を固定し、品質制約を保ったまま実装範囲・探索空間・変更量を最適化する時に使う。
---

# Test Contract デザイナー

要求を直接テストコードへ変換する前に、何を観測できれば完成と判定できるかを固定する。成果物は原則として `TEST_CONTRACT.md`、または既存方針に従った `SPEC.md` 内の Test Contract セクションとする。

このスキルは本番コードを実装せず、Red-Green-Refactorも実行しない。責務は次の変換である。

```text
Requirement
  -> Observable
  -> Scenario / Expected Result
  -> Evidence Requirement
  -> Gate
  -> Proof Obligation
```

## ポータブル実行ルール

- 現在のユーザー依頼、利用中クライアントの権限規則、リポジトリ内の指示を優先する。特定製品の呼び出し構文、サブエージェント、モデル、ディレクトリ構成を前提にしない。
- `SPEC.md` があれば Requirement、受け入れ条件、固定要件の正典として読む。ユーザーが固定した Requirement を技術的判断だけで変更しない。
- Standalone利用では、ユーザーがファイル更新を依頼していなければ契約案を報告として返す。SDLC内または明示された変更作業では、プロジェクト方針に従って `TEST_CONTRACT.md` か `SPEC.md` を更新する。
- ユーザーが明示的に依頼しない限り、`git add`、`git commit`、`git push`、デプロイ、外部書き込み、破壊的操作を行わない。
- 既存の未コミット変更を保全し、Test Contract作成に不要なファイルを編集しない。
- Requirementが矛盾、不明確、または観測不能で、結果を変えずに解消できない場合は推測で補わず `BLOCKED` または `MISSING_CONTEXT` とする。

## 1. 品質制約下の最適化

品質はコストとのトレードオフ対象ではなく、先に満たす Hard Constraint である。

```text
All Required Observables = PASS
AND Fixed Requirements are preserved
AND Required Regression Tests = PASS
AND Required Security / Reliability Gates = PASS
```

Hard Constraintを満たす解の中でだけ、変更範囲、変更LOC、読み込むコード、コンテキスト、LLM Call、トークン、テスト時間、修復回数を小さくする。Required TestまたはRequired Observableを、トークン・時間・実装量の削減を理由に省略してはならない。

目標は単純な最小コードではなく、次の Minimum Sufficient Change である。

> 指定されたProof Obligationを満たすために必要十分であり、かつ既存契約を破壊しない最小の変更。

可読性、保守性、安全性を壊す過剰圧縮や、LOC削減だけを目的とした共通化は最適解とみなさない。

## 2. 契約の重さを選ぶ

| 区分 | 例 | 必要な契約 |
|---|---|---|
| Lightweight | typo、文言、単純な局所バグ | Expected behavior、Observable、Verification command |
| Standard | 新機能、API、複数ファイル、状態変更 | Requirement、Observable、Scenario、Evidence、Proof Obligationを明示 |
| High Risk | 認証、認可、金銭、個人情報、永続化、移行、破壊操作、外部副作用、本番、高負荷 | 詳細な制約、失敗条件、Security / Reliability / Outer Gateを必須化 |

すべての観点を機械的に追加しない。Requirementの性質、影響、失敗時の被害に必要なObservableだけをRequiredにする。

## 3. Requirementを固定する

1. ユーザー依頼、`SPEC.md`、設計記録からRequirementを列挙する。
2. 各Requirementへ安定したIDを付け、出典と原文を保持する。
3. 固定要件、禁止変更、スコープ外を分離する。
4. Requirement間の矛盾、測定不能な表現、欠けた閾値を検出する。
5. 曖昧さが結果を変える場合は質問または `MISSING_CONTEXT` とし、実装しやすい意味へ読み替えない。

Test Contractは既存実装からではなくRequirementから導出する。内部実装方法は、要求自体が固定している場合を除き契約へ持ち込まない。

## 4. Required Observableを導出する

Observableは、要求を満たしたと判定するために観測可能でなければならない事実である。可能な限り入力、操作、事前状態、出力、事後状態、時間、件数、副作用として表す。

悪い例:

```text
安全に処理できる
```

良い例:

```text
無効な拡張子を送るとHTTP 422を返す
同じidempotency keyを2回送ってもDBレコードは1件である
1000件を30秒以内かつ3試行以内で処理する
30秒で処理を中断できる
```

各Observableには最低限、次を定義する。

- IDと対応Requirement
- 観測対象とScenario
- Expected Result
- Test Level
- 必要なEvidence
- Inner LoopまたはOuter Gate
- RequiredかOptionalか

## 5. 完全性をリスクベースで検査する

次のレンズを使い、該当するのに欠けているObservableがないか確認する。

| レンズ | 検討する観点 |
|---|---|
| Functional | 正常系、異常系、境界値、不正入力、状態遷移、回帰 |
| Data / Persistence | 保存、読込、schema、atomicity、corruption、concurrency、single writer |
| Side Effect | retry、retry上限、idempotency、duplicate prevention |
| Execution | timeout、cancel、output size、process / OS isolation |
| Security | auth、authorization、validation、path traversal、injection、filesystem / environment / network boundary |
| Load / Performance | item count、latency、duration、attempt count、concurrency |

適用しない観点は無理にObservableへせず、Standard / High Riskで判断が重要なら対象外の理由を短く残す。

## 6. Proof Obligationへ分解する

Proof Obligationは、Required ObservableをPASSにするために現在の実装が満たすべき最小単位の検証責務である。

```text
R-001 Upload contract
  O-001 valid PDF returns 200       -> PO-001
  O-002 invalid extension returns 422 -> PO-002
  O-003 over 10MB returns 413       -> PO-003
```

原則として1つのPOは1つの主要Observableを対象とする。複数Observableが不可分なら、結合理由と同じEvidenceで証明できる根拠を記録する。POを実装方法やファイル単位で定義しない。

TDDへはシステム全体の完成要求ではなく、未達POごとに次を渡す。

```yaml
proof_obligation:
  id: PO-003
requirement:
  id: R-001
observable:
  id: O-003
  expected: "10MBより大きいファイルは413"
current_evidence:
  status: fail
  command: "pytest ..."
  failure: "returned 200"
constraints:
  tests_are_fixed: true
  api_contract_is_fixed: true
allowed_scope:
  - src/upload.py
related_context:
  - src/upload.py
  - tests/test_upload.py
target:
  required_status: pass
```

`allowed_scope` は根拠なく狭く固定しない。既知の関連範囲を記載し、範囲外が必要になった場合は理由を示して契約または計画を再確認する。

## 7. Inner LoopとOuter Gateを分ける

- Inner Loop: Unit、API contract、小さな状態遷移、pure function、validationなど、Red-Green-Refactorで高速に回す検証。
- Outer Gate: Integration、E2E、Browser、OS sandbox、durability、load、security、external systemなど、高コストまたは環境依存の検証。

Outer Gateを各小ループへ無条件に入れない。一方、Required Outer Gateを省略したまま最終PASSにしてはならない。実行不能なら `UNVERIFIED` または `BLOCKED` とする。

## 8. EvidenceとVerdictを定義する

「テスト済み」という自然言語だけをEvidenceにしない。利用可能な範囲で次を要求する。

- 実行コマンドとexit code
- test / harness名
- actual resultと観測値
- timestampとenvironment
- covered observable
- 失敗分類または制約事項

EvidenceがそのObservableを本当に証明するかを、実装工程と分離したJudge責務で評価できる形にする。別エージェントは必須ではないが、Test Designer、TDD Implementer、Judgeの責務は混ぜない。

状態は `PASS`、`FAIL`、`UNVERIFIED`、`BLOCKED`、`INVALID_EVIDENCE` を使う。Required Observableが一つでもPASS以外なら、Requirement全体をPASSにしない。一般テストスイートが成功していても、必要なObservableを覆わなければ `UNVERIFIED` である。

## 9. Context Compression by Contract

POごとに、Requirement、Observable、固定制約、現在Evidence、関連ファイルを小さな入力契約へまとめる。目的はトークン削減自体ではなく、探索空間を縮めて判断、誤変更、再探索を減らすことである。

関連ファイルは根拠を持って選ぶ。リポジトリ全体を既定入力にせず、同時に、品質を証明するために必要な依存関係をコンテキスト節約だけで除外しない。

この境界により、高性能モデルがRequirement・設計・Test Contractを定義し、ローカルまたは小規模モデルが明確なPOの実装・修復を担当できる。モデル分担は任意であり、モデル能力やコストを理由にHard Constraint、Required Evidence、最終Judgeを弱めない。

## 10. 最小論理スキーマ

ファイル形式にかかわらず、最低限次の情報を保持する。

```yaml
requirement:
  id: R-001
  source: SPEC.md
  text: ""
observables:
  - id: O-001
    description: ""
    scenario: ""
    expected: ""
    level: unit
    evidence:
      - executable_test
    gate: inner
    required: true
proof_obligations:
  - id: PO-001
    observable: O-001
```

Requirementに応じて `constraints`、`test_data`、`timeouts`、`failure_conditions`、`environment`、`security`、`reliability`、`performance` を追加する。初回導入ではYAML / JSONの厳密validationを必須にしない。

## 11. 標準成果物

```markdown
# Test Contract

## Contract Metadata
- Risk: Lightweight / Standard / High Risk
- Source: SPEC.md
- Fixed requirements:
- Forbidden changes:

## Requirement
### R-001: <要求原文>
- Source: SPEC.md#...

## Required Observables
### O-001: <観測可能な事実>
- Requirement: R-001
- Scenario:
- Target:
- Expected:
- Test Level: unit / contract / integration / e2e / harness
- Evidence:
- Gate: Inner / Outer
- Required: true

## Proof Obligations
### PO-001 -> O-001
- Current evidence: FAIL / UNVERIFIED / ...
- Allowed scope:
- Related context:
- Fixed constraints:
- Stop condition: O-001 PASS + required regression PASS + constraints preserved

## Optimization Constraints
- Allowed scope:
- Forbidden changes:
- Preferred context:

## Acceptance Matrix
| Requirement | Observable | Proof Obligation | Evidence | Status |
|---|---|---|---|---|
| R-001 | O-001 | PO-001 | pending | UNVERIFIED |
```

プロジェクトが別形式を採用している場合は形式を合わせるが、Requirement、Observable、Scenario、Expected、Evidence、Proof Obligationの対応は失わない。

## 12. 固定と変更管理

- TDD開始前にRequired ObservableとProof Obligationを固定する。
- Test Contract工程は契約案、Test Plan、新規テスト候補、Observable、POを変更できる。
- ユーザーが固定したRequirement、Fixed Requirement、既存Required Testを無断で削除・弱体化しない。
- 実装をGreenにするためにRequired Observable、Expected Result、Gateを変更しない。
- Requirement変更が必要ならTDDを止め、変更理由、影響、再承認が必要な範囲を示す。

POの停止条件は次である。

```text
Required Observable = PASS
AND Required Regression = PASS
AND Fixed Constraints = preserved
```

この条件を満たした時点で、そのPOに対する実装を止める。ついでの改善は行わず、必要なら別POまたは明示されたRefactor工程へ分ける。

## アンチパターン

- 思いつくテストを全部追加するTest explosion
- 既存実装から逆算して通しやすい契約を書くImplementation-driven Contract
- トークンや時間を理由にRequired検証を省くQuality / Cost Tradeoff
- Observable behaviorではなく内部実装を過度に固定するOver-specification
- 全案件へtimeout、load、sandbox等を機械的に課すUniversal reliability requirements
- GreenにするためRequired TestまたはExpected Resultを弱めるTest rewriting
- Evidenceの対応先を示さず、一般テスト成功だけでRequirementをPASSにする
