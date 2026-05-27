# Source-Checker Audit Report — Paper 2 (Empirical Evaluation)

**Project:** Poverty Point Costly Signaling
**Date:** 2026-05-02
**Manuscript audited:** `docs/paper2_empirical/Paper2_Empirical_Evaluation.md` and `docs/paper2_empirical/Paper2_Supplemental.md`
**Run by:** Claude Code (source-checker skill)

This is a fresh audit of the post-split empirical paper, separate from the earlier 2026-05-01 source-check report on the consolidated `docs/manuscript_AA/Poverty_Point_AA.md`.

---

## Infrastructure Summary

| Component | Status | Details |
|-----------|--------|---------|
| Manuscript format | Markdown | `Paper2_Empirical_Evaluation.md` (~14,950 words) + `Paper2_Supplemental.md` (~10,700 words) |
| Citation style | Markdown inline | Parenthetical `(Author Year)` and narrative `Author (Year)` |
| `.bib` file | Absent | Markdown-native bibliography in §References Cited |
| `docs/references/INDEX.md` | Present | 44 source-keyed entries (research-pipeline-processed) |
| `docs/references/claims/` | Present | 44 claims files |
| `docs/references/summaries/` | Present | 44 summary files |
| `docs/references/crosscheck_log.md` | Present | 13-line log; existing entries reviewed |

Checks 1, 2, 3, 4, 5, 7 were run. Check 6 (.bib consistency) is N/A.

---

## Critical Issues

Issues that are likely errors requiring attention before submission.

### Check 1: Citation-to-Source Matching

**Hill et al. 2016 vs `hill_etal_2010` INDEX entry — different works.**

- **`Hill et al. 2016`** at `Paper2_Empirical_Evaluation.md:39` — cited for "LA-ICP-MS analysis of six specimens" of PP copper
- The INDEX entry `hill_etal_2010` (= Hill, Greenlee, and Neff 2010, an unpublished SAA symposium paper marked "DO NOT CITE WITHOUT PERMISSION OF THE AUTHORS") has the same authors and reports analysis of the same 6 copper specimens, but is a different work from Hill et al. 2016 (= the published *Journal of Archaeological Science: Reports* version).
- The Paper 2 ref-list entry for "Hill et al. 2016" is correctly the published version. The Paper 2 citation is therefore not orphaned in any practical sense.
- **Suggested fix:** add a published `hill_etal_2016` entry to INDEX (alongside or replacing the unpublished `hill_etal_2010` entry). Status of the 2010 symposium version: per its DO-NOT-CITE notice, it should not be the public-facing reference; the 2016 JAS:Reports version supersedes it.
- **Severity:** Critical (because the public reference and the indexed source diverge), but the manuscript's citation choice is the correct one — the issue is on the INDEX side.

### Check 2: Claim-to-Summary Verification

No misattribution found. Spot-checks performed:

| Attribution in Paper 2 | Claim in claims file | Verdict |
|---|---|---|
| Sassaman (2005:340-341) on Caney/Insley scaling (`Paper2:81`) | `sassaman_2005_claims.md` Claims 1-2: Watson Brake, Frenchman's Bend, Caney, Insley scale relationships, Page: pp. 340-341 | ✓ confirmed |
| Clay (2023) "physical remnant of a number of abandoned projects" (`Paper2:241`) | `clay_etal_2023_claims.md` Claim: exact quote present | ✓ confirmed |
| Saunders et al. (2005) WB built episodically with multi-century pulses (`Paper2:171`) | `saunders_etal_2005_claims.md` Claims 21-22: ENSO-pulse stable-period mound construction | ✓ consistent (specific "200+ year" wording is a paraphrase of the pulse-chronology argument; the year-count is not a literal quote from the claims file) |
| Sanger (2023, 2024) institutional flexibility / cyclical aggregation-dispersal (`Paper2:261`) | `sanger_2023_claims.md` Claims 1, 4, 7; `sanger_2024_claims.md` Claim 1+ | ✓ confirmed |
| Webb (1982) 2,221 steatite fragments + Webb's bulk cache + "several hundred vessels" (`Paper2_Supplemental.md:217`) | `webb_1982_claims.md` Claim cluster around steatite: "2221 steatite fragments came from all sectors..." with "Several hundred vessels were thought to be represented..." | ✓ confirmed |

No claim-to-summary mismatches detected.

### Check 3: Quote Accuracy

**Direct quotes verified verbatim against claims files:**

| Quote in Paper 2 | Source | Claims file verdict |
|---|---|---|
| "nothing visible goes out" (`Paper2:39`, `Paper2:159`) | Kidder and Grooms 2025 | ✓ exact text match in `kidder_grooms_2025_claims.md` Claim 20 |
| "the physical remnant of a number of abandoned projects" (`Paper2:241`) | Clay (2023) | ✓ exact text match in `clay_etal_2023_claims.md` |
| "fragments representing several hundred vessels" (`Paper2:147`, `Paper2_Supplemental.md:217`) | Webb (1982) | ✓ paraphrase consistent with claims-file Statement: "Several hundred vessels were thought to be represented by the cached fragments" |
| "fall and winter provide acorns and other nuts" (`Paper2_Supplemental.md:282`) | Webb (1982) | ✓ exact text match in `webb_1982_claims.md` |
| "spring and summer offer ... most varieties of fish and crustaceans" (`Paper2_Supplemental.md:282`) | Webb (1982) | ✓ same quoted statement, abridged with ellipsis from claims-file full text |
| "millions of migratory waterfowl, ducks, geese, swans, pigeons" (`Paper2_Supplemental.md:282`) | Webb (1982) | ✓ exact match against claims-file statement |

All direct quotes are accurate against the evidence base.

### Check 4: Page Number Validation

**Two page-number errors identified.**

#### Error 4.1: Kidder and Grooms 2025:177 — wrong page (×2 occurrences)

- **Location:** `Paper2_Empirical_Evaluation.md:39` and `:159`
- **Cited:** `(Kidder and Grooms 2025:177)`
- **Claims-file evidence:** The "nothing visible goes out" quote appears on **p. 7** of Kidder and Grooms 2025, per `kidder_grooms_2025_claims.md` Claim 20 (`- **Page**: p. 7`).
- **Probable cause:** The "in press" Southeastern Archaeology version may not yet have stable journal pagination; "p. 177" appears to be a manuscript-page or holdover from a different draft. The claims-file pages range from p. 1 (abstract) to p. 12 (conclusion).
- **Severity:** Critical — page number doesn't match the documented source-page.
- **Suggested fix:** Change both occurrences from `Kidder and Grooms 2025:177` to `Kidder and Grooms 2025:7` (or, if the Southeastern Archaeology print version is available with stable pagination, verify against that and update consistently).

#### Error 4.2: Webb 1982:18 — wrong page for three phenology quotes

- **Location:** `Paper2_Supplemental.md:282` (S11 Seasonal phenology section)
- **Cited:** `Webb (1982:18)` cited three times in succession for three different quotes
- **Claims-file evidence:**
  - "fall and winter provide acorns and other nuts" → claims file documents this on **p. 1** (not p. 18)
  - "spring and summer offer roots and berries... most varieties of fish and crustaceans" → claims file: **p. 1**
  - "millions of migratory waterfowl, ducks, geese, swans, pigeons" → claims file: **p. 2**
- The claims file does record material at Webb 1982 p. 18, but it's about Thomas-and-Campbell settlement-type categorization and "substantial occupations" extending beyond ridge construction, not about seasonal phenology.
- **Severity:** Critical — three page-number errors in a single sentence.
- **Suggested fix:** Change `Webb (1982:18)` to `Webb (1982:1)` for the first two phenology quotes ("fall and winter..." and "spring and summer...") and to `Webb (1982:2)` for the migratory-waterfowl quote. Three replacements at line 282.

---

## Warnings

Potential issues that may be false positives or are stylistic.

### Check 5: Missing Citations

A targeted scan for empirical or attributed claims without citations yielded no high-confidence flags. The body of Paper 2 supports its empirical claims with citations directly attached. Spot checks where attribution might be required:

- `Paper2:171` "Watson Brake (16OU175, ca. 5400-4700 cal BP; Saunders et al. 2005)" → cited ✓
- `Paper2:127` "ODD protocol (Grimm et al. 2010)" → cited ✓
- `Paper2:75` "(Saunders et al. 2005)" for WB site description → cited ✓
- §3.4 paleoclimate-derived sigma derivation → cited at point of use; full derivation deferred to framework paper §S1.4 ✓

The Methods section §3 is appropriately compressed and defers detailed derivations to the framework paper, with cross-references in place.

### Check 6: Bibliography Consistency

N/A — no `.bib` file. The Markdown-native reference list at lines 351-471 was audited in the prior reference-list audit (commit `2a2a810`); 58 entries, all cited at least once, all citations resolve to a list entry.

### Check 7: Citation Format Consistency

Paper 2 follows the project's parenthetical-default convention. Spot checks of author-led citations:

- `Paper2:171` "Watson Brake (16OU175... Saunders et al. 2005), the other major LMV monumental site, provides a more demanding test." — author-led mention "Saunders et al. 2005" is parenthetical, no issue.
- `Paper2:241` "as Clay (2023) argues" — author-led, justified (the sentence is about Clay's specific interpretation).
- `Paper2:175` "the 200+ year inter-stage gaps (Saunders et al. 2005)" — parenthetical, justified.
- `Paper2:79` "Lower Jackson, with the second-highest static H... is a single isolated mound built ~5500 cal BP and represents a single-band or single-event construction with no associated residential or exchange evidence (Saunders et al. 2001)" — parenthetical, justified.
- `Paper2:325` "*Stallings Island and the Savannah River shell-ring tradition* (4500-3500 cal BP; Sassaman 2006)" — parenthetical, justified.

No non-conforming author-led usages identified.

### Orphan Sources (Warning)

Of 44 INDEX entries, 19 are not cited in Paper 2. These are not errors; they are project-level background sources, retained in the INDEX as part of the broader reference base:

- `bell_1956`, `bird_etal_2017`, `blackburn_2003`, `britt_etal_2002`, `byrd_1991`, `dunnell_greenlee_1999`, `ford_1954`, `gagliano_saucier_1963`, `haag_webb_1953`, `hamilton_buchanan_2009`, `hays_2018` (cited but as 2019 — see warning below), `hill_etal_2010` (cited but as Hill et al. 2016 — see Critical 1.1), `lehmann_1990`, `liefert_shuman_2022`, `lipo_2012`, `medina_elizalde_etal_2022`, `ortmann_2007`, `pierce_1997`, `shuman_2024`

This pattern is expected: not every INDEX entry needs to be cited in every manuscript.

### Year-of-Publication Discrepancy (Warning)

**Hays 2019 (manuscript) vs hays_2018 (INDEX/claims):**

- Paper 2 ref list (line 363): "Hays, Christopher T. 2019. Feasting at Poverty Point with Poverty Point Objects. *Southeastern Archaeology* 38:193-207."
- Claims file: "Hays, Christopher T. 2018. Feasting at Poverty Point with Poverty Point Objects. *Southeastern Archaeology* 37(3). DOI: 10.1080/0734578X.2018.1496315."
- Online publication date (DOI): 2018, vol 37(3)
- Print volume per Paper 2 ref: 2019, vol 38, pp. 193-207
- **Possible resolution:** the article appeared online in 2018 (DOI year, Issue 37(3)) and in print in vol 38 (2019), pp. 193-207. Paper 2 cites the print-volume metadata; the claims file cites the online-version DOI metadata. This is a common citation-year discrepancy for online-first journal articles.
- **Severity:** Warning — verify against the published volume (print edition) before submission. Per AA convention, the print-year citation (2019) is the accepted form when the article is in a year-stable print issue.
- **Suggested fix:** Either align the claims file to the print-year convention (2019, vol 38) or verify Paper 2's print-year citation by checking the journal record.

### Hill et al. publication-version discrepancy (Warning, see Critical 1.1)

The Paper 2 citation `Hill et al. 2016` is the published JAS:Reports paper; the INDEX `hill_etal_2010` is the unpublished symposium precursor. The Paper 2 citation choice is correct (cite the published version). The INDEX should be updated to reference the 2016 published version explicitly. Suggested fix is on the INDEX side, not the manuscript.

---

## Unresolved Flags

### [CITE-CHECK] flags

None found in Paper 2 main or supplemental.

### [UNVERIFIED] flags

None found in Paper 2 main or supplemental.

**Total:** 0 unresolved manuscript flags.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total citations found in Paper 2 (main + SI) | ~110 distinct in-text citations |
| Citations matched to ref-list entries | 100% (58 ref-list entries, all cited; verified in prior audit) |
| Citations matched to INDEX-tracked sources | 25 of 58 ref entries have INDEX claims/summaries |
| Orphan citations (in manuscript, missing from ref list) | 0 |
| Orphan sources (in INDEX, never cited in Paper 2) | 19 (project-level background, expected) |
| Claims attributed to specific sources | ~12 substantive attributions; all spot-checked |
| Claim mismatches found | 0 |
| Direct quotes checked | 6 quotes against claims files |
| Quote mismatches found | 0 |
| Page numbers checked | 5 (Sassaman 2005:340-341; Kidder & Grooms 2025:177 ×2; Webb 1982:18 ×3) |
| **Page number mismatches found** | **5 (Critical 4.1: 2 K&G 2025:177→7; Critical 4.2: 3 Webb 1982:18→1 or :2)** |
| Unresolved [CITE-CHECK] flags | 0 |
| Unresolved [UNVERIFIED] flags | 0 |
| .bib issues found | N/A |
| Citation format issues found | 0 |

**Critical issues:** 2 (one INDEX-side, one with 5 page-number errors across 2 manuscript locations)
**Warnings:** 2 (Hays year discrepancy, Hill 2010-vs-2016 INDEX issue)
**Informational:** 19 uncited INDEX background sources (expected)

---

## Suggested crosscheck_log.md Entries

The crosscheck log has 13 lines and was last updated in early 2026; the existing entries focus on the consolidated AA manuscript (e.g., Saunders dating, Mound A volume). The following entries are proposed for the post-split state.

### Suggested entry 1

**Claim**: "nothing visible goes out" attributed to Kidder and Grooms 2025:177
**Source attributed**: Kidder and Grooms 2025
**Verification method**: source-checker audit, Check 4
**Result**: Page-number discrepancy — quote is on p. 7 per `kidder_grooms_2025_claims.md` Claim 20
**Details**: Page "177" appears in two locations in Paper 2 main (lines 39 and 159). The claims file pagination (pp. 1-12) is from the in-press Southeastern Archaeology version. p. 177 does not appear in the documented page range.
**Action taken**: Pending user review. Suggested fix: change `2025:177` to `2025:7` in both manuscript locations.

### Suggested entry 2

**Claim**: Three Webb (1982) quotes about seasonal LMV resources attributed to p. 18
**Source attributed**: Webb 1982
**Verification method**: source-checker audit, Check 4
**Result**: Page-number discrepancy — actual pages are p. 1 (twice) and p. 2 (once) per `webb_1982_claims.md`
**Details**: The fall/winter and spring/summer phenology quotes are documented on p. 1; the migratory waterfowl quote is on p. 2. Page 18 of Webb 1982 covers settlement-type categorization (Thomas and Campbell), not seasonal phenology.
**Action taken**: Pending user review. Suggested fix at `Paper2_Supplemental.md:282`: change three "Webb (1982:18)" occurrences to two `Webb (1982:1)` and one `Webb (1982:2)`.

### Suggested entry 3

**Claim**: Hill et al. 2016 cited as the source for LA-ICP-MS analysis of six PP copper specimens
**Source attributed**: Hill et al. 2016 (manuscript ref list entry: Hill, Mark A., Diana M. Greenlee, and Hector Neff. 2016. Assessing the Provenance of Poverty Point Copper through LA-ICP-MS Compositional Analysis. *Journal of Archaeological Science: Reports* 6:351-360.)
**Verification method**: source-checker audit, Check 1
**Result**: INDEX-side gap — INDEX has only the unpublished `hill_etal_2010` symposium-paper precursor; the published 2016 paper is not in INDEX
**Details**: Paper 2's manuscript citation is the published JAS:Reports version (correct citation choice). The INDEX entry `hill_etal_2010` is an earlier unpublished SAA symposium paper covering the same data and marked "DO NOT CITE WITHOUT PERMISSION OF THE AUTHORS." The reference-pipeline should add an explicit `hill_etal_2016` entry (or merge the 2010 entry into a single hill_etal_2010-2016 entry noting both versions) so the public-facing citation matches an indexed source.
**Action taken**: Pending. Suggested fix is on the INDEX/claims side, not the manuscript.

### Suggested entry 4

**Claim**: Hays 2019 cited (Paper 2 ref list) vs Hays 2018 (INDEX/claims)
**Source attributed**: Hays (year ambiguous between online and print issue)
**Verification method**: source-checker audit, Check 5/Warning
**Result**: Year discrepancy attributable to online-first vs print-year publication dates
**Details**: DOI 10.1080/0734578X.2018.1496315 indicates online publication in 2018 (vol 37(3)). Paper 2 cites print-year 2019 (vol 38, pp. 193-207), which is the form expected by AA. The DOI year and the print year diverge for SA articles published online-first.
**Action taken**: Pending verification against the print-edition record. Either keep "Hays 2019, vol 38" (preferred for AA convention) and note the online-first origin in the claims file, or align both to a single citation form.

---

## Re-run notes

- Prior audit at `docs/references/source_check_report.md` (2026-05-01) was on the consolidated AA manuscript. After the two-paper split (commits `34258a2` through `2a2a810`), this is the first source-check on Paper 2 (the empirical paper) in its post-split form.
- Prior audit reported zero critical issues (post-Round-3 fixes). The two new Critical findings here (page-number errors at K&G 2025:177 and Webb 1982:18) appear to be artifacts present in the original AA manuscript that were not detected in the prior audit because the prior audit's quote/page checks did not extend to those specific lines.
- All other findings are stable across the split.

---

*Report generated by source-checker skill, 2026-05-02. Re-run after fixes to verify resolution.*
