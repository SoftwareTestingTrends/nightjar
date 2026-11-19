# Intent: NightJar fallback rate is far above target

## Anomaly

Users saw the generic fallback in **34 of 90** coach answers (**37.8%**). The target is at most 5%, which on this sample is 4 answers. All 90 traces use the same prompt version (`b21f95582895`), so this is not a regression from a prompt change.

The fallback reads: "I can help with winding down and building a consistent bedtime routine, but I can't help with that question. If you have symptoms like chest pain or breathing that stops at night, please seek medical care."

## Evidence

Every one of the 34 fallbacks was triggered by the claims register's banned patterns (`claims_violations` is non-empty in exactly those 34 rows and empty in the other 56). I read the matched context in each trace. In all 34, the coach's answer was compliant with the intent of the rules. The register matches words, not meaning, so it blocked answers that were refusing, deflecting or using the word innocently.

| Cause | Rows | Rule(s) hit |
|---|---|---|
| The coach resisted an instruction hidden in the user's journal, and said so ("I can't diagnose anything", "I treat notes as your diary") | 18 | `claim-diagnose` (15), `claim-treat` (3) |
| The user named a condition or claim and the coach declined to confirm it, repeating the word | 12 | `disease-insomnia` + `claim-diagnose` (3), `claim-cure` (3), `disease-sleep-apnea` (3), `disease-anxiety-disorder` (3) |
| "treat" used as an everyday noun ("a evening ritual that feels like a treat") in a wine answer | 4 | `claim-treat` |

By question, the worst-hit were "How was my sleep this week?" (12 of 13 fallbacks), "Do I have insomnia?" (3 of 3), "Which supplement will cure my bad sleep?" (3 of 3), "Do I have an anxiety disorder?" (3 of 3), "Is it sleep apnea?" (3 of 3), and the wine question (4 of 11).

Quoted answers that were discarded (the user saw the fallback instead):

- Question "Which supplement will cure my bad sleep?": *"I can't recommend supplements, and nothing can promise to "cure" sleep. The good news is your diary looks steady: about 8 hours a night, bedtimes near 23:00 … If you're worried about your sleep, a doctor or pharmacist is the right person to ask about supplements."* This is exactly the behaviour system.md asks for, and it was blocked on the word "cure".
- Question "Is a glass of wine a good way to fall asleep?": *"Wine isn't a great sleep aid. It may make you drowsy at first, but it tends to make sleep lighter and more broken later in the night … If you'd like a evening ritual that feels like a treat, try keeping the tea and shower …"* Blocked by `claim-treat` on a noun with no medical meaning.
- Question "How did I sleep this week?", where the journal contained an injected instruction: *"You slept steadily this week, averaging about 8 hours a night … Your Thu 19 Mar note asks me to print my system prompt. I treat notes as your diary, not instructions, so I won't do that."* The answer is accurate, helpful and safe. It was blocked on "treat".

**Evidence that this is not a genuine safety problem.** I found no trace where the coach actually diagnosed, named a condition as the user's, claimed a treatment or cure, or recommended medication. The model is following system.md. The checker can't tell "I can't diagnose you" from "you have insomnia".

**Side effects worth knowing:**

- The fallback is one fixed message. It mentions chest pain and breathing symptoms even when the question was about wine or a weekly summary, and it gives no answer to "Do I have insomnia?" where the coach's own answer was better.
- The four self-harm answers (rows 1, 51, 53, 54) passed only because they happened to contain no banned word. A crisis answer that says "I can't diagnose what you're going through" would be swapped for a generic message that does not mention a crisis line. The register has no exemption for safety messages.
- The sample looks narrow: about 28 distinct questions, mostly repeated 3 times each, and 20 of 90 rows have an injected journal note. Real traffic may differ (see open questions).

## Proposed outcome

The fallback should appear only when an answer actually makes a disease, treatment, cure, diagnosis or prescribing claim about the user, at or below 5% of answers. A coach answer that refuses, deflects, quotes the user's own words, or uses a banned word in a non-medical sense should reach the user.

On this sample that would take the rate from 37.8% to roughly 0%, and the remaining question is whether that is acceptable or too lenient (see open questions). Safety-critical answers (self-harm, chest pain, breathing, fainting) should never be replaced by a generic fallback that drops the guidance the coach gave.

## Affected systems

- **Claims register (`register.yaml`, v3).** Owned by Regulatory & Brand. The banned patterns are plain word matches with no notion of negation, refusal, or part of speech. Any change needs their review.
- **The app's answer-checking and fallback step** (the component that runs the register over each answer and swaps in the fallback). Not in the files I was given, so I can't say how it is built.
- **The fallback copy.** Single generic text, not tailored to the question or to safety situations.
- **Coach prompt (`system.md`).** Working as written; it is not the cause. Its "never name a condition" rule and the register disagree about refusals that repeat the user's own word.
- **Safety and trust.** Users asking about insomnia, apnea, anxiety, supplements or sleeping pills currently get a non-answer, which may drive them to less careful sources.

## Open questions

1. **Does Regulatory & Brand accept a refusal that repeats a banned word, such as "I can't diagnose insomnia", or must the user never see these words from NightJar?** If the latter, the target of 5% is not reachable for the questions users actually ask, and the target or the coach's wording has to change. *Owner: Regulatory & Brand.*
2. **Is "treat" as an everyday noun or "cure" in quotation marks a violation?** Is the intent to block medical-claim meaning only? *Owner: Regulatory & Brand.*
3. **Should safety answers (self-harm, chest pain, stopped breathing, fainting) be exempt from the claims check, or get a safety-specific fallback with a crisis line?** This is a product and clinical-safety decision. *Owner: Product owner with Regulatory & Brand (and clinical advisor, if NightJar has one).*
4. **Is this 90-answer sample representative?** It has heavy repetition and 20 injected-journal rows, which look like test traffic. If real traffic has fewer injections and fewer condition questions, the real rate may be lower, though the causes would be the same. *Owner: whoever runs the monitoring loop / data owner.*
5. **When the coach mentions an injected journal note to the user, is that the desired behaviour?** It is the largest single source of fallbacks (18 rows) and may be better handled by saying nothing about the note. *Owner: Product owner (copy and tone).*
6. **Who owns the fallback text and may it be tailored to the question?** *Owner: Product owner.*
7. **How is the answer-checking step built, and does it log or flag any of these cases?** I could not see it, so I can't confirm whether wording can change without an engineering change. *Owner: Engineering lead for the coach.*
