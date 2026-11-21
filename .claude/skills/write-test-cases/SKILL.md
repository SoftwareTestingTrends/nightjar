---
name: write-test-cases
description: Plans how to test a user story before it is built, and writes the result as test cases in a document for review. Use whenever someone is getting ready to test a story, ticket or set of acceptance criteria, however they put it: test cases, test ideas, scenarios, edge cases, risks, what to check, a checklist, test design or coverage, even if they never say "test cases". Not for automated tests, test code or test data.
---

# Write test cases from a story

Here, test cases are a document a tester reviews with Product before development starts. They are not automated tests. If the user asks for automated tests or test code, this skill doesn't apply.

## Who reads this, and why it matters

A tester and a product owner read this document together, line by line, in one meeting, before any code exists. The rules below follow from that.

- Aim for 2 to 5 cases per acceptance criterion. A review that runs past an hour loses the people it's for, so choose the cases most likely to find a bug: the boundaries, the time zone and daylight-saving edges, the empty state.
- When two cases differ only in their data, make them one case and list the data values in it. The reader learns nothing new from the second row.
- Give every open question a proposed answer. Product can accept or change a proposal in a minute; a bare question stalls the meeting.
- Work only from the story and the documents it links to, not `src/` or `tests/`. The code may be missing or wrong, and the test cases are there to check it, not to copy it.

## Steps

1. Read the story and every document it links to. If the story file doesn't exist or has no acceptance criteria, stop: say what you looked for and ask which story is meant. Don't invent one.
2. Write the cases to `docs/test-cases/<story-id>.md`. Create the folder if it doesn't exist.
3. Start the file with the test data you'll reuse: the user, their time zone, the dates and the "now" each case assumes.
4. Write one table per acceptance criterion, plus one for any non-functional requirement. Use the columns ID (`TC-<story number>-<n>`), Condition, Steps and Expected result. Give concrete data: dates, times and time zones.
5. Test both sides of every number in the story. Consider:
   - dates and times around midnight
   - a change of time zone
   - daylight saving in America/Toronto and Europe/London
   - no data, and the minimum data
   - any text the user sees passing the claims check (`docs/claims.md`)
6. Every expected result must come from the story or the documents it links to. If they don't say, add an open question instead of guessing.
7. End the file with "Open questions" as a table: #, Question, Cases affected, Proposed answer, Who decides. Product owns the stories; Regulatory & Brand owns the claims register.
8. Reply with the file path, the number of cases per acceptance criterion, and the open questions.

## Example rows

| ID | Condition | Steps | Expected result |
|---|---|---|---|
| TC-116-8 | A 00:15 bedtime counts for the previous date | 1. Log standard nights for 12 and 13 Nov. 2. Log a night with bed 00:15 on Sun 15 Nov, wake 07:45. 3. Now = Thu 19 Nov 10:00 Toronto. | The night is the night of Sat 14 Nov and is counted in the window. |

| # | Question | Cases affected | Proposed answer | Who decides |
|---|---|---|---|---|
| 1 | A mean exactly halfway between two 5-minute steps (442.5 min): round up or down? | TC-116-29 | Round half up: 7 h 25 min. | Product |
