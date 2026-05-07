# Crosscheck Log

Running log of verification checks. Every claim in the manuscript that attributes a specific statement to a published source must be verified here before submission.

## Verification Entries

### 2026-05-03 — Hawkes 2000 attribution in Paper 1

**Claim**: "Hawkes (2000) summarizes Hadza data showing that successful big-game hunters secure a reproductive success advantage of about 10-20% relative to less successful hunters, mediated by preferential access to mating opportunities and partner choice." (`docs/paper1_theory/Paper1_Theory_Model.md` line 143)

**Source attributed**: Hawkes, Kristen. 2000. Hunting and the Evolution of Egalitarian Societies: Lessons from the Hadza. In *Hierarchies in Action: Cui Bono?*, edited by Michael W. Diehl, pp. 59-83. Center for Archaeological Investigations Occasional Paper No. 27. Southern Illinois University, Carbondale.

**Verification method**: Full claims extraction of the chapter (`docs/references/claims/hawkes_2000_claims.md`) by the reference-pipeline skill, 2026-05-03.

**Result**: **Discrepancy found.** The 10-20% reproductive-success advantage figure is NOT present in this chapter. The chapter establishes (a) hunter ranking is consistent across years (citing Blurton Jones et al. 1997), (b) better hunters are valuable resources and "hunting prowess may be among a man's most important characteristics" (p. 71), and (c) the qualitative case for partner-choice premium, but does not provide a quantitative reproductive-success premium.

**Details**: The 10-20% figure likely derives from Hawkes 1991 ("Showing Off: Tests of an Hypothesis About Men's Foraging Goals," *Ethology and Sociobiology* 12:29-54) or a related Hawkes paper. The Hawkes 2000 chapter is a synthesis paper that references the partner-choice mechanism qualitatively without restating quantitative figures from earlier work. Paper 1's combined ethnographic-anchor paragraph (line 143) cites three sources: Hawkes 2000 (this entry), Wiessner 2002 (10-30% shortfall-resource access claim, not yet independently verified), and Hawkes & Bliege Bird 2002 (partner-choice premium "within the same magnitude range"). The bracketing of $\lambda_W \in [0.05, 0.30]$ as a plausible-range claim is reasonable on the synthesis of these three sources, but the specific attribution of "10-20%" to Hawkes 2000 is overstated.

**Action taken**: Pending user review. Two recommended fixes:
1. **Cite Hawkes 1991 in addition to (or instead of) Hawkes 2000** for the 10-20% figure. This would require acquiring Hawkes 1991 to verify the figure; Hawkes 1991 is not yet in the project's INDEX.
2. **Soften the Paper 1 attribution to qualitative form** consistent with what Hawkes 2000 actually says: e.g., "Hawkes (2000) summarizes Hadza data showing that better hunters are recognized as valuable partners, with hunter ranking consistent across years and partner choice favoring better hunters." This avoids the unverified quantitative claim.

The Wiessner 2002 hxaro-network claim cited in the same paragraph also requires independent verification once Wiessner 2002 is processed through the pipeline.

**Resolution (2026-05-03):** Paper 1 line 147 has been revised to remove the unsupported "10-20% reproductive-success advantage" attribution to Hawkes 2000. The revised text now reads in qualitative form: "Hawkes (2000) summarizes Hadza data showing that better big-game hunters are recognized as valuable partners: hunter rankings are consistent across years (Blurton Jones et al. 1997, summarized in Hawkes 2000:71), and partner choice favors better hunters — the qualitative pattern that signal quality drives partner-choice premium. Hawkes (2000) does not quantify the reproductive-success advantage and we do not attribute a specific magnitude to that source." The bracketing argument for $\lambda_W \in [0.05, 0.30]$ is preserved by reframing as "ethnographic estimates of related-but-distinct quantities (the qualitative partner-choice pattern; the quantified shortfall-resource premium; the partner-choice-premium magnitude review) jointly support an order-of-magnitude plausibility window." The Wiessner 2002 claim remains pending independent verification.

---

### 2026-05-03 — Hill et al. 2016 attribution in Paper 2

**Claim**: "Copper was traditionally attributed to Lake Superior (~1,600 km), but recent LA-ICP-MS analysis of six specimens (Hill et al. 2016) indicates that several match Nova Scotia or southern Appalachian sources as well as, or better than, Lake Superior. The framework does not require Great Lakes copper specifically; what matters for the signaling argument is that geochemical sourcing identifies the materials as non-local and unfakeable, so any of these candidate source attributions still places copper in the long-distance index-signal class." (`docs/paper2_empirical/Paper2_Empirical_Evaluation.md` line 39)

**Source attributed**: Hill, Mark A., Diana M. Greenlee, and Hector Neff. 2016. Assessing the Provenance of Poverty Point Copper through LA-ICP-MS Compositional Analysis. *Journal of Archaeological Science: Reports* 6:351-360.

**Verification method**: Full claims extraction of the page-proofs PDF (`docs/references/claims/hill_etal_2016_claims.md`) by the reference-pipeline skill, 2026-05-03.

**Result**: **Confirmed.** Paper 2 line 39 accurately represents the paper's findings. Across three discriminant function tests, all six PP copper samples assigned to eastern (Appalachian / Maritime) sources rather than Lake Superior. The four-region test placed all six samples in Nova Scotia (probabilities 0.54-0.99), but the authors flag this clustering as potentially reflecting undersampling of southern Appalachian source rocks rather than actual Maritime provenance. Paper 2's framing — "as well as, or better than, Lake Superior" — correctly handles the Nova Scotia attribution as one consistent option without overcommitting to it.

**Details**: The PDF version in the repository is the page-proofs / accepted-manuscript with manuscript pagination (pp. 1-22), not the published JAS:Reports vol 6, pp. 351-360 pagination. Paper 2's citation does not include a page reference, so no conversion is needed for the current text. The INDEX has been updated: `hill_etal_2010` (unpublished SAA symposium precursor) marked as superseded by the new `hill_etal_2016` entry, which is now the citable form.

**Action taken**: No fix required to Paper 2 prose. Pipeline outputs added: `claims/hill_etal_2016_claims.md`, `summaries/hill_etal_2016.md`, INDEX entry, evidence integration into `exchange_networks_evidence.md`.

---

### 2026-05-03 — Wiessner 2002 attribution in Paper 1

**Claim**: "Wiessner's (2002) hxaro analysis of Ju/'hoansi exchange estimates that high-network individuals maintain access to roughly 10-30% additional resources during shortfalls." (`docs/paper1_theory/Paper1_Theory_Model.md` line 147, in the same ethnographic-anchor paragraph as the Hawkes 2000 attribution audited above.)

**Source attributed**: Wiessner, Polly. 2002. Hunting, Healing, and Hxaro Exchange: A Long-Term Perspective on !Kung (Ju/'hoansi) Large-Game Hunting. *Evolution and Human Behavior* 23(6):407-436.

**Verification method**: Full claims extraction of the published paper (`docs/references/claims/wiessner_2002_claims.md`) by the reference-pipeline skill, 2026-05-03.

**Result**: **Discrepancy found.** The specific "10-30% additional resources during shortfalls" figure is NOT present in this paper. The paper's quantitative findings about good-vs-poor hunter premiums range from 24% (child survival to age 15: 83% vs 67%, Table 4) to 171% (adult-children co-residence: 84% vs 31%, Table 4). Hxaro-network premiums for good hunters' families are 80% (more partners), 48% (more household possessions), 142% (more distant-kin partnerships), and 84% longer (camp residence duration). The closest shortfall-related quantitative claim in the paper is that 93% of extended visits during food shortages and conflicts are made to camps with hxaro partners (p. 422), and 69% of household possessions are obtained through hxaro (p. 422); 80% of diet during "hungry months" comes from large-game kills (p. 416, citing Wiessner & N!aici 1998). None of these matches "10-30%."

**Details**: Both this and the Hawkes 2000 audit show the same pattern: Paper 1's three-source bracketing argument for $\lambda_W \in [0.05, 0.30]$ used specific numerical claims that are not actually present in the cited papers. The qualitative content (hxaro buffers shortfalls; better hunters have larger networks; good hunters' families have measurably better outcomes) is correct, but the specific percentages do not appear. The likely sources for the "10-30%" figure are Wiessner 1982 (the foundational hxaro-as-shortfall-buffering paper, "Risk, reciprocity and social influences on !Kung San economics") or Wiessner 1986/1996, none of which is currently in the project INDEX.

**Action taken (combined with Hawkes 2000 fix)**: Paper 1 line 147 has been further revised to remove both the Hawkes 2000 "10-20%" and the Wiessner 2002 "10-30%" specific-number attributions. The bracketing argument for $\lambda_W \in [0.05, 0.30]$ is now restated as a synthesis of the three sources' qualitative and (where actually documented) quantitative findings, without imputing specific percentages to particular papers. Both source-specific revisions track the same audit pattern and are reported transparently.

---

### 2026-05-03 — Wiessner 1982 attribution audit (third pass on the 10-30% figure)

**Claim**: The "10-30% additional resources during shortfalls" figure that earlier drafts of Paper 1 attributed to Wiessner-source ethnographic anchoring (`docs/paper1_theory/Paper1_Theory_Model.md` line 147, paragraph grounding $\lambda_W \in [0.05, 0.30]$).

**Source attributed**: Wiessner, Polly. 1982. Beyond Willow Smoke and Dogs' Tails: A Comment on Binford's Analysis of Hunter-Gatherer Settlement Systems. *American Antiquity* 47(1):171-178. (Added to the project pdfs collection by the user specifically to test whether the figure originated here.)

**Verification method**: Full claims extraction of the JSTOR-archived published version (`docs/references/claims/wiessner_1982_claims.md`) by the reference-pipeline skill, 2026-05-03.

**Result**: **Discrepancy confirmed.** The 10-30% figure is NOT in this paper. Wiessner 1982 is an eight-page theoretical comment that proposes the four-strategy risk-reduction typology (prevention, transfer, storage, pooling) and sketches archaeological correlates. The only !Kung quantitative material is the qualitative observation (p. 175) that exchange ties do not fall off monotonically with distance, referenced to the Wiessner 1977 dissertation rather than reproduced. There is no percentage figure for shortfall-resource access of any sort.

**Details**: This is the third audit on the same disputed figure. Hawkes 2000 (entry 1 above) does not contain a "10-20% reproductive-success advantage" figure. Wiessner 2002 (entry 3 above) does not contain a "10-30% additional resources during shortfalls" figure; its actual hxaro-shortfall figures (69-93%) describe dominant-mechanism roles rather than marginal supplements. Wiessner 1982 (this entry) does not contain the figure either. The most plausible primary source is Wiessner 1977 (*Hxaro: A regional system of reciprocity for reducing risk among the !Kung San*, Ph.D. dissertation, University of Michigan), which is not in the project's PDF collection. The 10-30% number may also be a paraphrase artifact from secondary literature rather than a figure published anywhere by Wiessner directly.

**Action taken**: No further textual change required to Paper 1 line 147. The Hawkes 2000 fix (entry 1) and Wiessner 2002 fix (entry 3) already removed the unsupported number from Paper 1's prose, replacing it with documented qualitative findings and correctly-quantified figures (80% more hxaro partners, 48% more household possessions, 84% longer camp residence). The bracketing argument for $\lambda_W \in [0.05, 0.30]$ is now framed as an order-of-magnitude plausibility window grounded in the synthesis of Hawkes 2000, Wiessner 2002, and Hawkes & Bliege Bird 2002, with no specific percentage attributed to any paper not in the repo. Wiessner 1982 has been added to the INDEX as the foundational pooling/risk-sharing reference (the qualitative concept Paper 1 invokes), independent of the percentage question.

---

### 2026-05-03 — Wiessner 1977 dissertation audit (fourth pass on the 10-30% figure)

**Claim**: The "10-30% additional resources during shortfalls" figure that earlier drafts of Paper 1 attributed to Wiessner-source ethnographic anchoring (`docs/paper1_theory/Paper1_Theory_Model.md` line 147 paragraph grounding $\lambda_W \in [0.05, 0.30]$).

**Source attributed**: Wiessner, Pauline Wilson. 1977. *Hxaro: A Regional System of Reciprocity for Reducing Risk Among the !Kung San.* Ph.D. dissertation, University of Michigan. University Microfilms 78-4841. Two volumes, 462 pages. (Added to the project pdfs collection by the user specifically to test whether the figure originates in this primary source after the Hawkes 2000, Wiessner 2002, and Wiessner 1982 audits all failed to locate it.)

**Verification method**: Bounded reading of the dissertation (`docs/references/claims/wiessner_1977_claims.md`) by the reference-pipeline skill, 2026-05-03. The 462-page two-volume dissertation could not be exhaustively read within session budget. The reading scope was: full front matter (acknowledgments, preface, table of contents, list of tables, list of figures, orthography note, pp. i-lvi); Chapter I "Theoretical Framework" opening (body pp. 1-3); Chapter IV "Social Relationships and Access to Goods, Services and Resources" subsections on Services, Food Sharing, and Distributing Non-Food Items (body pp. 129-143). Chapter II (subsistence variability), Chapters V-VIII (hxaro distribution data, social groups, cross-cultural comparison), and the appendices were inspected only via the table of contents and list of tables.

**Result**: **Not located within reading scope.** The food-sharing section (the chapter most likely to contain shortfall-resource quantitative data) is qualitative narrative — describes the three-degree typology of food sharing, the mechanics of meat distribution, and the attitudes and obligations governing redistribution — but contains no specific shortfall-resource percentage. The preface contains one quantitative figure in this conceptual family ("60% of /ai/ai daily conversation involves social control on resource redistribution," p. xxxv), but this is a salience measure, not a resource-access measure. None of the 18 quantitative tables listed in the front matter is titled in a way that announces a shortfall-resource-access percentage as a finding.

**Details**: This is the fourth audit on the same disputed figure. Hawkes 2000, Wiessner 2002, and Wiessner 1982 all failed to locate it. Wiessner 1977 — the dissertation that subsequent Wiessner papers reference back to for !Kung quantitative detail — also fails to surface the figure within the most likely chapters. Tentative conclusion: the 10-30% figure is not a headline finding of any source in the project repository. It is most plausibly either a paraphrase artifact from secondary literature describing hxaro's qualitative shortfall-buffering function or a buried number from a specific data-table comparison that was attributed in Paper 1 without page-level grounding. The chapters not exhaustively read (Wiessner 1977 Chapters II, V, VI, VII, VIII) cannot be ruled out as the source of a buried figure, but no front-matter signal points to one.

**Action taken**: No further textual change required to Paper 1 line 147. The Hawkes 2000 fix (entry 1) and Wiessner 2002 fix (entry 3) already removed the unsupported "10-30%" number. The bracketing of $\lambda_W \in [0.05, 0.30]$ is now an order-of-magnitude plausibility window grounded in the documented quantitative findings of Wiessner 2002 (Tables 1-4) and the qualitative shortfall-buffering pattern that Wiessner 1977 establishes. Wiessner 1977 added to the INDEX as the foundational primary source for hxaro and as the network-breadth parameterization anchor (5-45 partners per adult).

**Audit chain summary**: Across four sources (Hawkes 2000, Wiessner 1982, Wiessner 2002, Wiessner 1977 within bounded reading), the "10-30% additional resources during shortfalls" attribution that appeared in earlier drafts of Paper 1 line 147 is not directly supported. Paper 1 prose has been revised twice and the bracketing argument now rests on the order-of-magnitude consistency of multiple lines of qualitative and correctly-quantified evidence rather than on a single specific percentage.

---

## Pre-Submission Checklist

See `verification-checklist.md` for the full 10-item checklist and gap analysis checks.
