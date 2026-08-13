# Clear Summary Patterns

Read this reference when the source is long, mixed, technical, contradictory, or difficult to structure. Select one primary pattern and borrow from another only when the source genuinely combines types.

## Contents

- Source Pattern Matrix
- Relationship Vocabulary
- Output Selection
- Compression Order
- Final Read Test

## Source Pattern Matrix

| Source type | Meaning spine | Keep first | Common distortion to avoid |
| --- | --- | --- | --- |
| Explanation | subject → definition → mechanism → significance | Core concept and how it works | Replacing explanation with a list of topics |
| Argument or opinion | claim → reasons → evidence → counterpoint → conclusion | Claim and strongest support | Presenting opinion as established fact |
| Research or report | question → method or basis → result → interpretation → limitation | Result plus evidence strength | Omitting population, period, method, or uncertainty |
| Meeting notes | issue → decision → reason → owner and date → unresolved item | Decisions and commitments | Mixing discussion with decisions |
| Proposal | problem → proposed response → expected effect → requirement → risk | Problem and proposal | Stating projected effects as achieved results |
| Procedure | goal → prerequisites → essential sequence → completion condition → warning | Goal and critical steps | Removing order, conditions, or safety constraints |
| News | event → verified facts → significance → response → unresolved question | What happened and current status | Treating speculation or early reports as confirmed |
| Transcript or interview | topic → speaker positions → reasons or experience → convergence or disagreement | Speaker-attributed main ideas | Erasing who said what or creating false consensus |
| Technical design | problem → constraints → chosen design → tradeoffs → operational effect | Decision and why it was chosen | Listing components without dependencies or tradeoffs |
| Comparison | decision question → criteria → meaningful differences → conditions → conclusion | Criteria and decisive differences | Declaring a universal winner when choice is conditional |

## Relationship Vocabulary

Use explicit connecting language when supported by the source:

- Cause: 「〜のため」「その結果」
- Condition: 「〜の場合に限り」「ただし」
- Contrast: 「一方で」「これに対して」
- Sequence: 「まず」「その後」「最終的に」
- Evidence: 「〜が根拠として示されている」
- Example: 「たとえば」「これは〜の一例」
- Scope: 「この結論は〜の範囲に限られる」
- Uncertainty: 「現時点では〜とみられる」「確認されていない」

Do not insert a connector when the relationship is only inferred from adjacency.

## Output Selection

### One clear message

Return one to three sentences. Include the subject, central message, and one necessary condition.

### Several related points

Use the standard `5秒でわかる` and `30秒でわかる` sections. Order the bullets so each one prepares the next.

### Complex system or long report

Add `全体のつながり` before detailed points. Prefer a short textual chain such as:

```text
背景 → 問題 → 対応 → 結果 → 残る課題
```

Replace the labels with actual content. Keep the chain to three through six nodes.

### Conflicting sources or speakers

Use this pattern:

```markdown
## 5秒でわかる
[一致している事実と、対立している中心点]

## 立場の違い
- [主体A]: [主張と根拠]
- [主体B]: [主張と根拠]

## 現時点で言えること
- [確認済みの範囲]
- [未確認・未決の範囲]
```

### Decision-oriented material

Use this pattern when the user must act on the summary:

```markdown
## 結論
[決定または選択肢]

## 判断材料
- [重要な根拠]
- [主要な条件・トレードオフ]

## 未決事項
- [決定前に確認すべきこと]
```

Keep recommendations outside the factual summary unless they are present in the source or the user explicitly asks for analysis.

## Compression Order

When the summary is too long, remove information in this order:

1. Repeated wording and rhetorical flourishes
2. Secondary examples
3. Background already implied by the central message
4. Supporting details that do not change confidence or interpretation
5. Lower-priority branches unrelated to the user's goal

Do not remove source boundaries, decisive evidence, exceptions, uncertainty, or facts that reverse the apparent meaning.

## Final Read Test

Read only the first section. It must identify the subject and central message without depending on later sections. Then read all sections once. The logic should be understandable without returning to the source, while the summary remains visibly shorter and simpler than that source.
