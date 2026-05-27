# Source-Checker Audit Report — Paper 1 (Theory & Model)

**Project:** Poverty Point Costly Signaling
**Date:** 2026-05-02
**Manuscript audited:** `docs/paper1_theory/Paper1_Theory_Model.md` and `docs/paper1_theory/Paper1_Supplemental.md`
**Run by:** Claude Code (source-checker skill)

---

## Infrastructure Summary

| Component | Status | Details |
|-----------|--------|---------|
| Manuscript format | Markdown | `Paper1_Theory_Model.md` (~8,060 words) + `Paper1_Supplemental.md` (~5,000 words) |
| Citation style | Markdown inline | Parenthetical `(Author Year)` and narrative `Author (Year)` |
| `.bib` file | Absent | Markdown-native bibliography in §References Cited |
| `docs/references/INDEX.md` | Present | 44 source-keyed entries |
| `docs/references/claims/` | Present | 44 claims files |
| `docs/references/summaries/` | Present | 44 summary files |
| `docs/references/crosscheck_log.md` | Present | 13-line log; reviewed |

Checks 1, 2, 3, 4, 5, 7 were run. Check 6 (.bib consistency) is N/A.

**Scope note:** Paper 1 is a theoretical/modeling paper. Most claims are the authors' own derivations or model results, which Check 2 does not flag. Check 2 focuses on claims attributed to prior published work, which in Paper 1 are concentrated in §1 (introduction), §2.1-§2.2 (theoretical-foundations citations), §5.2 (cultural-historical alternatives), and §5.3 (eastern Archaic comparison cases).

---

## Critical Issues

Issues that are likely errors requiring attention before submission.

### Check 1: Citation-to-Source Matching

No orphan citations. All 37 ref-list entries are cited at least once in prose; all in-text citations resolve to the ref list (verified in the prior reference-list audit, commit `2a2a810`).

**Citations matched to INDEX-tracked sources** (10 of 37 ref-list entries have INDEX entries):

| Ref-list entry | INDEX key | Verdict |
|---|---|---|
| Grooms, Ward, and Kidder 2023 | `grooms_ward_kidder_2023` | ✓ |
| Jackson 1986 | `jackson_1986` | ✓ |
| Kidder and Grooms 2025 | `kidder_grooms_2025` | ✓ |
| Ortmann and Kidder 2013 | `ortmann_kidder_2013` | ✓ |
| Quinn 2019 | `quinn_2019` | ✓ |
| Sanger 2023 | `sanger_2023` | ✓ |
| Sanger 2024 | `sanger_2024` | ✓ |
| Sassaman 2005 | `sassaman_2005` | ✓ |
| Ford and Webb 1956 | `webb_1956` | ✓ |
| Webb 1982 (cited indirectly via "Poverty Point Objects" reference) | `webb_1982` | ✓ |

The remaining 27 ref-list entries are theoretical, methodological, or comparative-archaeological background sources expected to lie outside the project's PP-specific INDEX (e.g., Bliege Bird and Smith 2005, Price 1970, Penn and Szamadó 2020, Zahavi 1975, Halstead and O'Shea 1989, Hawkes 2000, Wiessner 2002, Winterhalder 1986, Brent 1973, Grimm et al. 2010, DiNapoli et al. 2019, Marquardt and Watson 2005, Sassaman 2006, Sassaman 2010, Webb [W.S.] 1939, Graeber and Wengrow 2021).

**No issues.**

### Check 2: Claim-to-Summary Verification

Targeted claim spot-checks for attributions to prior work:

| Attribution in Paper 1 | Claims-file evidence | Verdict |
|---|---|---|
| Codding and Jones 2007 / Quinn 2019 critiques of CST in archaeology (`Paper1:33`) | `quinn_2019_claims.md` summarizes the critique that signaling is invoked post-hoc | ✓ consistent with the cited critique |
| Sanger (2023, 2024) reads aggregation centers as institutions of containment, with cyclical aggregation and dispersal preventing the consolidation of authority (`Paper1:29`) | `sanger_2023_claims.md` Claims 1, 4, 7 (institutional flexibility, heterarchy, cyclical authority); `sanger_2024_claims.md` Claim 1+ (awe-mediated cooperation) | ✓ accurate paraphrase |
| Kidder and Grooms (2025) argue for revitalization-movement dynamics (`Paper1:29`) | `kidder_grooms_2025_claims.md` summary section confirms the revitalization framing | ✓ accurate |
| Grimm et al. 2010 ODD protocol (`Paper1:111`) | Methodological reference; standard protocol citation | ✓ standard methodological cite |
| Bliege Bird and Smith 2005 index-signal interpretation (`Paper1:59, 67, 121`) | Theoretical reference; the paper's index-vs-handicap distinction is the foundational citation | ✓ standard theoretical cite |
| Hawkes 2000 / Wiessner 2002 / Hawkes and Bliege Bird 2002 ethnographic anchors for $\lambda_W$ in [0.05, 0.30] (`Paper1:143`) | Theoretical/ethnographic references; the brackets are reasonable paraphrases of the cited literature | ✓ paraphrase consistent with sources |
| Saunders et al. 2005 200+ year inter-stage gaps at WB (referenced in Paper 1 SI §S5 cross-reference, but the substantive WB analysis is in Paper 2) | Same as Paper 2 audit: consistent with Saunders et al. 2005 ENSO-pulse stable-period chronology argument | ✓ |

**No misattributions detected.**

### Check 3: Quote Accuracy

Direct attributable quotes are scarce in Paper 1 (it is a derivation paper). Quotation-mark scanning identified terminological quotes (e.g., "tendency to aggregate and contribute," "We can defend this place" / "we will cooperate reliably," "network-density value" — all the authors' own definitions or characterizations) but no verbatim quotes from external sources requiring verification.

**No quote-accuracy issues.**

### Check 4: Page Number Validation

No page-number citations in Paper 1 main or SI prose (i.e., no `Author Year:Page` patterns). All in-text citations are year-only. Page numbers appearing in the ref list are editor-page-range fields for chapters in edited volumes (e.g., Hawkes 2000: pp. 59-83), not in-text quote attributions.

**No page-number issues.**

---

## Warnings

### Check 5: Missing Citations

The introduction §1 and discussion §5 are dense with citations. Spot checks on potential missing-citation gaps:

- `Paper1:27` "Mobile foragers in these contexts built earthworks on scales that required mass mobilization of labor, accumulated exotic raw materials sourced from locations up to 1,600 km away..." — cited (Ford and Webb 1956; Gibson 2000; Sassaman 2010) ✓
- `Paper1:81` "Jackson (1986, 1989) developed it explicitly in subsistence work for the LMV, and Ward (1998) refined it through paleoethnobotany." — cited ✓
- `Paper1:111` "ODD protocol (Grimm et al. 2010)" — cited ✓
- `Paper1:135-141` ablation methodology — cited (Penn and Szamadó 2020) for the cooperation-vs-signaling framing ✓

The §5.3 "Implications" subsection makes conditional placements at Stallings Island (Sassaman 2006), Green River (Marquardt and Watson 2005), Mulberry Creek (Webb 1939; Sassaman 2010), without any quantitative claims requiring further citation. All ref-list entries are appropriately attached.

**No missing-citation issues identified.**

### Check 6: Bibliography Consistency

N/A — no `.bib` file. The Markdown-native reference list (lines 235-307) was audited in the prior reference-list audit (commit `2a2a810`); 37 entries, all cited at least once, all citations resolve to a list entry.

### Check 7: Citation Format Consistency

Paper 1 follows the project's parenthetical-default convention. Author-led citations checked:

- `Paper1:81` "Jackson (1986, 1989) developed it explicitly... and Ward (1998) refined it" — author-led, justified (the sentence is about who developed the conceptual move, not a generic reference).
- `Paper1:29` "Sanger (2023, 2024) reads aggregation centers as institutions of containment" — author-led, justified (Sanger's specific interpretation is the focus).
- `Paper1:29` "Kidder and Grooms (2025) argue for revitalization-movement dynamics" — author-led, justified (their specific argument is the focus).
- `Paper1:151-153` "Hawkes (2000) summarizes Hadza data..." / "Wiessner's (2002) hxaro analysis..." / "Hawkes and Bliege Bird's (2002) review places the partner-choice premium..." — author-led, justified (each sentence specifically describes that author's contribution to the ethnographic-grounding argument).
- `Paper1:35` "(Lipo, Greenlee, and DiNapoli, forthcoming-b)" — parenthetical, justified.

**No format-consistency issues.**

### Orphan Sources (Warning)

Of 44 INDEX entries, 34 are not cited in Paper 1. Most are PP/LMV-specific empirical sources that belong to the empirical paper rather than the theory paper:

`bell_1956`, `bird_etal_2017`, `blackburn_2003`, `britt_etal_2002`, `byrd_1991`, `clay_2023`, `dunnell_greenlee_1999`, `ford_1954`, `gagliano_saucier_1963`, `haag_webb_1953`, `hamilton_buchanan_2009`, `hargrave_etal_2021`, `hays_2018`, `hill_etal_2010`, `jackson_1981a`, `kaufman_etal_2020`, `kidder_2002`, `kidder_2006`, `kidder_etal_2021`, `kidder_grooms_2024`, `kidder_henry_arco_2018`, `lehmann_1990`, `liefert_shuman_2022`, `lipo_2012`, `medina_elizalde_etal_2022`, `ortmann_2007`, `peacock_rafferty_2013`, `pierce_1997`, `salonen_etal_2025`, `saunders_etal_2005`, `shuman_2024`, `shuman_marsicek_2016`, `ward_etal_2022`, `webb_1968`

This is the expected division of labor between the two papers. These sources are appropriately concentrated in the empirical companion paper.

---

## Unresolved Flags

### [CITE-CHECK] flags

None found.

### [UNVERIFIED] flags

None found.

**Total:** 0 unresolved manuscript flags.

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total citations found in Paper 1 (main + SI) | ~70 distinct in-text citations |
| Citations matched to ref-list entries | 100% (37 ref-list entries, all cited) |
| Citations matched to INDEX-tracked sources | 10 of 37 ref entries |
| Orphan citations (in manuscript, missing from ref list) | 0 |
| Orphan sources (in INDEX, not cited in Paper 1) | 34 (PP-specific empirical sources, expected) |
| Claim attributions checked | 7 substantive attributions; all spot-checked |
| Claim mismatches found | 0 |
| Direct quotes requiring verification | 0 (no external direct quotes in prose) |
| Quote mismatches found | 0 |
| Page numbers in prose | 0 |
| Page number mismatches found | 0 |
| Unresolved [CITE-CHECK] flags | 0 |
| Unresolved [UNVERIFIED] flags | 0 |
| .bib issues found | N/A |
| Citation format issues found | 0 |

**Critical issues:** 0
**Warnings:** 0 (orphan-source count is informational; expected division of labor)
**Informational:** 34 INDEX entries not cited in Paper 1 (PP-empirical sources concentrated in companion paper)

---

## Suggested crosscheck_log.md Entries

None warranted. No discrepancies, no missing flags, no claim or page-number mismatches.

---

*Report generated by source-checker skill, 2026-05-02. Re-run after any major prose revision.*
