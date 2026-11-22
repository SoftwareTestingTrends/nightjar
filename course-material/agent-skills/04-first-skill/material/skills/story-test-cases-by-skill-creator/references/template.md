# Document template

Copy this structure. Replace everything in angle brackets. Keep the section order: the
reviewers read top to bottom in a meeting.

````markdown
# Test cases: <S-nnn> <story title>

| Field | Value |
|---|---|
| Story | [<S-nnn>](../stories/<S-nnn>.md) |
| Traces to | <BR / PR ids from the story> |
| Status | Draft for review |
| Prepared | <date> |
| Reviewers | Tester: <name or blank> · Product: <name from the story's Owner field> |

## How to read this document

Each case has fixed starting data, steps, and one expected result. Reviewers: mark the
**Product check** line on each case as Agreed, Change (say what), or Question. Cases
whose expected result depends on an open question are marked *Proposed*. These are
written for a person to run by hand; automated tests come later.

## Coverage

| Criterion | Cases |
|---|---|
| AC1: <short paraphrase> | TC-nnn-1, TC-nnn-2 |
| AC2: ... | ... |
| Edge: ... | ... |
| Non-functional: ... | ... |

## Open questions for Product

| # | Question | Why it matters | Proposed answer | Cases affected |
|---|---|---|---|---|
| Q1 | <question> | <outcome A vs outcome B> | <proposal> | TC-nnn-4 |

## Test cases

### TC-nnn-1: <what is proven, in plain words>

- **Covers:** <AC1>
- **Type:** <Normal | Boundary | Edge | Error | Non-functional>
- **Setup:** Today is <weekday, date>. The user's time zone is <IANA zone>. The diary contains:

  | Night of | Bedtime | Wake time | Zone |
  |---|---|---|---|
  | <date> | <local time> | <local time> | <zone> |

- **Steps:**
  1. <action in the app's terms>
  2. <action>
- **Expected result:** <exact text / value / file content>. <Proposed, see Q1: only if applicable>
- **Product check:** ☐ Agreed ☐ Change: ______ ☐ Question: ______

### TC-nnn-2: ...
````

## Notes on filling it in

- **Setup tables show local times plus the "night of" date.** The "night of" column lets
  Product confirm the data matches their mental model (a 00:15 bedtime on Sunday is
  Saturday night) without doing the arithmetic themselves.
- **Keep data sets small.** Three to eight nights is usually enough. Say when a case
  needs a larger set (non-functional volume cases) and describe how to generate it rather
  than listing it.
- **Show the working** for any computed expected value in one line under the result
  ("Durations 7 h 50 min, 8 h 05 min, 7 h 40 min; mean 7 h 51 min 40 s; nearest 5 min is
  7 h 50 min"). It lets the reviewer verify the number without a calculator and makes a
  wrong expectation easy to spot.
- **Verbatim copy.** Quote messages exactly, including punctuation, from the story.
- **Volume or timing cases** state the data size, the measure, and the pass threshold from
  the story, and the machine class if the story gives one (otherwise raise a question).
