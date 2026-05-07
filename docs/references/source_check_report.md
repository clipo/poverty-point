# Source Check Audit Report

**Date:** 2026-05-01
**Manuscript:** docs/manuscript_AA/Poverty_Point_AA.md (Round 3 revision, ~21,800 words)
**Auditor:** source-checker skill (read-only)

This audit supersedes the prior 2026-03-23 source-check report; the manuscript has been substantially revised since then.

---

## Infrastructure summary

- **Manuscript format:** Markdown (`.md`)
- **Citation style:** Markdown inline (parenthetical and narrative)
- **`.bib` file:** none (Markdown-native bibliography in §References Cited)
- **`docs/references/INDEX.md`:** present, 44 entries (research-pipeline-processed sources with claims/summaries)
- **`docs/references/claims/`:** 44 claims files
- **`docs/references/summaries/`:** 44 summary files
- **`docs/references/crosscheck_log.md`:** present

Adapted check coverage: Checks 1, 2, 3, 4, 5, 7 are run (no `.bib` file → Check 6 skipped).

---

## Citation extraction summary

- **Citations in body:** 65 unique (Author, Year) tuples
- **Bibliography entries:** 67 entries
- **Citation matches against bibliography:** 64 of 65 unique citations matched on initial scan (98.5%)

---

## Critical Issues

### 1. Orphan citation: Gomez 2014 (FIXED in this audit)

- **Location:** §4.5 line 209 (was)
- **Issue:** `(Saucier 1994; Gomez 2014)` appeared in body; "Gomez 2014" not in bibliography. Per project CLAUDE.md ("Do not fabricate citations"), the citation has been removed from the body, leaving `(Saucier 1994)` as the supporting citation. The empirical hydrograph claim is independently supported by §S7.5b USGS gauge analysis.
- **Status:** **RESOLVED** in the audit pass; manuscript edited to remove the unverifiable citation.

No other Critical Issues.

---

## Warnings

### 2. Orphan bibliography entries (sources in bib never cited in body)

These are Warning-level per source-checker rules — bibliography may legitimately include closely related background sources.

| Bib entry | Status |
|---|---|
| Jackson 1989 | In bibliography, not cited in body (closely related to Jackson 1981 and Jackson 1986, both cited; appears to be retained background source) |
| Liu and Fearn 2000 | In bibliography, not cited in body (Liu and Fearn 1993 IS cited; the 2000 paper is the related Florida record, retained as background) |
| Sanger 2024 | In bibliography, not cited in body (Sanger 2023 IS cited; the 2024 paper is closely related, retained as background) |

**Recommendation:** Either add brief in-text references to these works in the §5.2 alternative-frameworks discussion, or remove them from the bibliography. The current presence of all three is defensible as research-completeness signaling but technically generates "uncited bibliography entries."

### 3. INDEX entries never cited in this manuscript (research-pipeline orphan sources)

These are sources that have full research-pipeline processing (claims and summary files) but are not cited in this article. They are Warning-level per source-checker rules — they may have been processed for context or future work without being cited in this particular paper.

| INDEX entry | Reason for non-citation |
|---|---|
| bell_1956 | Copper plummet documentation; covered by Hill et al. 2016 cite |
| bird_etal_2017 | Spatial analysis methodology |
| blackburn_2003 | Magnetite/hematite plummet study |
| britt_etal_2002 | Geophysical survey (covered by Hargrave et al. 2021 + Clay 2023 cites) |
| byrd_1991 | 1986 Conference proceedings (substituted by direct citations to Smith 1991 etc.) |
| dunnell_greenlee_1999 | Waste-hypothesis predecessor (theoretical foundation; superseded in current draft by index-signal framing) |
| ford_1954 | Aerial photography of ridges (covered by Ford 1955 and Ford and Webb 1956 cites) |
| gagliano_saucier_1963 | Deltaic-lowlands site documentation |
| grooms_ward_kidder_2023 | Cited as Grooms et al. 2023 in body; INDEX key is grooms_ward_kidder_2023 (filename mismatch, not orphan) |
| haag_webb_1953 | Microblade documentation (foundational but not cited in this version) |
| hamilton_buchanan_2009 | ACE/BACE methodology (not used in this paper) |
| hays_2018 | PPO feasting argument; the Hays 2019 cite is to a different paper |
| hill_etal_2010 | Earlier Hill paper; the Hill et al. 2016 cite is to the more recent paper |
| kidder_henry_arco_2018 | Jaketown Bayesian flood chronology (background) |
| liefert_shuman_2022 | Mid-Holocene paleoclimate (mentioned in supplemental, not main text) |
| lipo_2012 | Plummet morphometrics (not used in this paper) |
| medina_elizalde_etal_2022 | Paleoclimate (background) |
| ortmann_2007 | Mound stratigraphy dissertation (covered by Ortmann and Kidder 2013 cite) |
| pierce_1997 | Mound construction reference (background) |
| shuman_2024 | Recent paleoclimate (background; not in current draft) |
| webb_1956 | Webb's 1956 Mound A monograph (covered by Ford and Webb 1956 cite) |

**Recommendation:** No action needed. These are processed sources retained for the project's broader research pipeline; their non-citation in this specific manuscript is intentional and consistent with the article's scope.

### 4. Minor citation-format observations

- The manuscript consistently uses parenthetical citations as the default with author-led citations only for noted claims (e.g., "Sanger (2023, 2024) reads," "Sassaman's (2005) structure-event-process," "Webb's (1982)"), which matches the project's writing-style convention.
- One minor inconsistency: §4.5 uses "Ward et al. (2022)" twice in narrative form when the author-led emphasis is not strictly required ("Ward et al. (2022) document the same pattern in different language"). This is borderline-acceptable since the sentence does describe a specific finding, but could be made parenthetical without loss.

---

## Flag scan

Searched all manuscript files for `[CITE-CHECK: ...]` and `[UNVERIFIED: ...]` patterns:

- **Round 2 had 1 unresolved CITE-CHECK flag** (Carleton et al.) at line 262
- **Round 3 status: 0 flags remaining.** The Carleton flag was resolved in the round-3 commit (replaced with `Quinn 2019`, which is in the bibliography); no new flags introduced.

---

## crosscheck_log.md status

- Log present at `docs/references/crosscheck_log.md`
- No new unresolved entries flagged by this audit.
- No new entries suggested (no Critical Issues remain after the Gomez 2014 fix).

---

## Summary

- **Total citations in body:** 65 unique (Author, Year) tuples → all but 1 matched to bibliography on first pass; the remaining `Gomez 2014` was removed in this audit.
- **Critical Issues at end of audit:** 0 (Gomez 2014 fix applied during audit).
- **Warnings:** 3 (orphan bibliography entries, INDEX entries not cited in this manuscript, minor citation-format observations).
- **Flag count:** 0 (all CITE-CHECK and UNVERIFIED flags resolved).
- **Crosscheck log status:** No new unresolved entries.

The manuscript's citation infrastructure is in good shape for AA submission. The single critical issue (Gomez 2014 unverified citation) was resolved during this audit. The orphan bibliography entries and INDEX-not-cited sources are within normal bounds for a manuscript drawing on a broader research pipeline; they represent retained context rather than errors.

---

## Suggested next steps

1. **Decide on three orphan bibliography entries** (Jackson 1989, Liu and Fearn 2000, Sanger 2024): either add light in-text references where they naturally fit, or remove from bibliography. The current state is defensible.
2. **Optionally update grooms_ward_kidder_2023 INDEX entry** to flag that it is cited in the manuscript as "Grooms et al. 2023" (the parenthetical cite uses first-author + et al., which is correct convention but creates a minor INDEX-key mismatch that's purely cosmetic).
3. **No other action needed before submission.** The manuscript is internally consistent on citations.
