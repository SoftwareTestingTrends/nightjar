---
name: story-test-cases
description: Write test cases for a NightJar user story (docs/stories/S-*.md) as a plain-language review document that a tester and Product walk through together before development starts. Not automated tests. Use this whenever the user asks for test cases, a test plan, test scenarios, "what should QA check", acceptance test cases, or "test cases first" for a story such as S-116 or S-117, even if they don't say "document". Do not use it to write pytest, Playwright or eval code.
---

# Story test cases for review

Turn a user story and its acceptance criteria (AC) into a test case document. The
readers are a tester and someone from Product, sitting together before any code exists.
They will read it line by line, argue about it, and sign off. Nobody will run it as code.

That audience drives every choice below:

- **Product must be able to say "yes, that's what I meant" or "no" for each case.** So
  write in the story's own language, with concrete values, not code terms.
- **The tester must be able to run the case by hand later without asking anyone.** So
  every case states its starting data, the action, and one exact expected result.
- **Disagreements are the point.** The most valuable thing the document can do is expose
  places where the story is vague, before it is built. Surface them; never quietly pick
  an interpretation.

## Workflow

1. **Find the story.** The user gives an id (`S-116`) or a path. Read `docs/stories/<id>.md`,
   then the requirement it traces to (`docs/requirements/`), and `docs/claims.md` when the
   story has user-facing wording. If the story is missing or has no AC, stop and say so.
2. **Learn the shared rules, not the answer.** Read the "Things agents get wrong" and
   Conventions sections of `CLAUDE.md` and the story's *Notes*. These tell you where bugs
   hide (midnight crossing, DST, zone of the night vs. current zone). You may read
   existing behaviour the story builds on, such as how the CSV import or the usual-bedtime
   rule works, so your sample data is realistic (`data/sample_nights.csv` shows the
   format). Do **not** derive expected results from code for the new story: it doesn't
   exist yet, and the document's job is to check the code against the story, not the
   reverse.
3. **Derive cases per AC.** For each AC, write at least one case for the stated behaviour,
   then add cases for how it can break (see "What to cover"). Every case names the AC it
   covers. Non-functional lines and the story's Edge line get cases too.
4. **Work out expected results by hand, and check the arithmetic.** Medians, averages,
   rounding, offsets and "night of" dates are easy to get wrong in a document just as in
   code. Recompute each figure a second time before writing it down. If you can't
   determine the expected result from the story, don't invent one: write the case, put
   "To be decided" as the expected result, and raise a question (step 5).
5. **Collect open questions** for Product (see below) and put them in their own section
   with a proposed answer for each, so Product can simply accept or change it.
6. **Write the document** using `references/template.md` and save it to
   `docs/test-cases/<story-id>.md` (create the folder if needed). If the user names a
   different location, use theirs.
7. **Reply briefly**: the file path, number of cases, and the open questions, since those
   need a human decision. Don't paste the document back.

Do not create or edit tests, source code, or `docs/traceability.md`. The only file you
write is the test case document. Mention that the traceability table can be filled in
when the automated tests are written.

## Case ids

Use `TC-<story number>-<n>`, for example `TC-116-1`. Number in the order cases appear in
the document. Using the story number makes it easy to map to the `T-116-n` ids the
repository uses in automated test names later, but keep the `TC-` prefix so nobody
mistakes a reviewed case for an existing automated test.

## What each case contains

Keep every case small: one behaviour, one expected result. A case that checks three
things hides which one failed.

| Part | Rule |
|---|---|
| **Title** | What is being proven, in plain words ("Nights either side of midnight count as one hour apart") |
| **Covers** | The AC / Edge / Non-functional line it traces to |
| **Type** | Normal, Boundary, Edge, Error, or Non-functional |
| **Setup** | The fixed starting state: which nights are in the diary (as a small table), the user's time zone, and what "today" is. Always give absolute dates and the time zone. Never "a few nights ago" |
| **Steps** | Numbered user actions, in the app's own terms ("Open the home page") |
| **Expected result** | The exact text, number or file content the user sees. Quote copy verbatim from the story |
| **Product check** | Leave blank: a checkbox / space for the reviewer's decision |

Fixing "today" in Setup matters because the story's windows ("the seven nights before
today") are meaningless without it, and the app takes its clock as input, so the tester
can reproduce the date.

## What to cover

Cover the happy path first, then probe these areas. Skip a category only if it truly does
not apply to the story, and don't pad with near-duplicates.

- **Boundaries of every number in the story**: one below, at, and one above (e.g. 2, 3
  and 4 nights when the threshold is 3).
- **Midnight**: bedtimes before and after 00:00 in the same data set; "night of" date
  for a post-midnight bedtime.
- **Time zones**: a night logged in a different zone from the user's current one; a zone
  change inside the window. Which zone is used for "today" versus for a night.
- **Daylight saving**: a night that crosses spring-forward or fall-back, in
  America/Toronto and Europe/London, when the story touches durations or clock times.
- **Empty and minimal data**: no nights, exactly the minimum.
- **Awkward values**: rounding ties, even counts for a median, notes with commas, quotes,
  line breaks and non-English text, very long text, when the story involves data in or out.
- **Wording and policy**: when the story shows text to the user, a case that the wording
  is wellness-only per `docs/claims.md`. State which words must not appear.
- **Non-functional lines**: turn each into a measurable case (what to measure, what data
  size, what pass threshold). If the story gives no number, ask.
- **Things the story is silent on** that a user could plausibly hit. These become open
  questions, not cases with invented answers.

## Open questions

Add a question whenever two reasonable readers of the story would expect different
results, or the story says nothing about a situation a tester can easily reach. Typical
sources: rounding ties, which side of a boundary is included, ordering of ties, what is
shown when a figure can't be computed, and how two AC interact.

For each, give: the question, why it matters (the two outcomes), a **proposed answer**,
and the case ids that depend on it. A question with a proposal is quick to resolve in a
meeting; a bare question stalls. Mark dependent cases' expected results as "Proposed" so
nobody treats them as agreed.

## Style

- Plain sentences, no code, no function or file names. The reader is not a developer.
- Use tables for data and a short numbered list for steps. A reviewer scanning 15 cases
  needs to find the expected result instantly.
- Be exact with numbers and punctuation ("7 h 25 min", not "about seven and a half hours").
- Prefer fewer, sharper cases over exhaustive combinations. A review that drags loses the
  people it is for. Roughly 2 to 5 cases per AC is typical.
- Keep a **coverage table** at the top mapping each AC to its case ids, so Product can see
  at a glance that nothing is untested and a tester can see nothing is duplicated.
