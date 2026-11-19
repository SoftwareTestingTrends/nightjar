I added 29 cases and a README in `evals/cases_v2/`. I didn't run the evals, and I couldn't parse-check the YAML because the Python check was blocked. Each file is hand-written in the same format as `evals/cases/`, and every case carries `type`, `source` and `golden`.

**Fixed cases (V2-01 to V2-08).** These are the original E-01 to E-08 with the fixes from `evals/findings/`:
- **E-03:** I removed the ban on "heart", since the refusals mention the topic. It now bans only what complying would say, such as "heart disease" or "blood pressure".
- **E-04:** I widened `contains_any` to any concrete wind-down step.
- **E-05 and E-06:** I dropped `claims_clean`, because correct refusals repeat "insomnia", "diagnose" and "cure". The bans now cover only affirmations like "you probably have" or "will cure".
- **E-07:** The sample data has no weekend drift, so the case now expects the coach to say it doesn't see one. The original consistency question lives on as V2-19.
- **E-01, E-02 and E-08:** These passed in the real run and are kept, with slightly stricter bans on E-01 and E-02.

**Golden safety cases (V2-09 to V2-17).** These cover gasping or choking, fainting, self-harm, "is it sleep apnea?", a sleeping-pill dose, "do I have an anxiety disorder?", and three journal-injection variants (system-prompt leak, role change, `</journal>` breakout). V2-18 (jet lag, no melatonin) is also golden. That makes 15 golden cases in total.

**Capability cases (V2-18 to V2-29).** These are authored from the sample diary: average hours, last bedtime, earliest night, wake time, the London trip, missing January data, coffee, alcohol, phone in bed, and an off-topic request. The set is 17 `regression` and 12 `capability`.

- **Untested:** V2-09 to V2-29 have never been run, so expect some grader tuning on the first run.
- **Grader limits:** Substring graders can't tell "you have X" from "you don't have X", and nothing can grade the 120-word limit.
- **Product issue for you:** The app's claims check also catches correct refusals that repeat "insomnia" or "cure", so users see the generic fallback. I didn't change it, per your instruction not to touch other files.

I left `evals/findings/` untracked and changed nothing outside `evals/cases_v2/`.
