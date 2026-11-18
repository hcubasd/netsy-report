# TR-D requirements register

As of 18 November 2026. **P** = verified official publisher guidance; **J** = journal scope verified on an official publisher page; **H** = historical journal instructions, current status unverified; **U** = unresolved; **R** = our recommendation, not a journal rule.

## Journal and article fit

**J.** [Official journal description](https://shop.elsevier.com/journals/transportation-research-part-d-transport-and-environment/1361-9209): the journal addresses transport's environmental consequences and responses, with policy and methodological relevance beyond an isolated application. Passenger and freight research are both in scope. For this paper, the environmental question must organize the contribution; software generalization and source-model reproduction supply its methodological foundation.

**R.** Treat the Dutch application as an informative controlled case. Explain what the comparison teaches about environmental assessment, and where conclusions depend on that network, fleet and logistics configuration. A software port alone does not establish that contribution. General-purpose schemas do not demonstrate geographical transfer.

## Length and manuscript organization

| Item | Finding | Status / source |
|---|---|---|
| Main-text word maximum | **Not verified.** Do not adopt 6,000/8,000 words as an official ceiling or assert unlimited length. | U: live guide blocked |
| Word-count exclusions | Whether references, captions, tables, appendices and abstract are excluded is not verified. | U |
| Abstract | Historical pack specifies 1–150 words. Use ≤150 as a provisional drafting target, not a certified current rule. | H |
| Title | Historical advice is about 12 words or fewer, concise, avoiding acronyms and unnecessary method names. | H |
| Keywords | Historical maximum is six. | H |
| Sections | Historical instructions use numbered sections; introduction, methods, results, discussion and conclusions, with optional combined results/discussion. | H |
| Submission layout | Historical instructions specify double spacing, page numbers and no author-added line numbers. | H |
| Glossary | Historical guide requests a separate terminology list. | H |
| References | Historical guide prefers Harvard author–year, consistent complete metadata and DOIs. | H |
| Peer review | Historical pack says single anonymized, normally at least two independent reviews. Confirm current process before deciding whether to anonymize files. | H |
| Suggested reviewers | Historical request: four potential reviewers with contact information. Confirm current portal fields; do not select or contact people yet. | H |
| Figure/table/reference maximum | No current maximum verified. Published examples are not policy. | U |
| Article type | Original research is the intended category; confirm its exact name in Editorial Manager. | J / U portal label |

Historical source: [third-party mirror of the Elsevier author pack dated 4 January 2022](https://www.readkong.com/page/transportation-research-part-d-transport-and-environment-4012795). It is retained locally as historical context only. The table paraphrases a small subset; it does not represent that old pack as current publisher confirmation.

**R. Working length plan:** aim initially for roughly 7,000–8,000 narrative words, with detailed adapters, equations, reproducibility checks and extra figures in appendices/supplements as appropriate. This is our editing budget, subject to the live guide and eventual scientific content. Keep an explicit count definition when reporting it. Do not infer a limit from typeset page counts.

## LaTeX and submission packaging

**P.** [Official LaTeX instructions](https://www.elsevier.com/researcher/author/policies-and-guidelines/latex-instructions) provide the `elsarticle` package and author–year sample. The archive linked directly from that page has been downloaded to `official/elsarticle-template.zip`. It is not a journal-specific TR-D layout certification.

The same page instructs authors to supply the manuscript PDF and appropriate editable source files, including bibliography and nonstandard dependencies, according to portal item types. It explicitly says Editorial Manager cannot process source subdirectories. Keep our modular repository, but implement a **separate flattened submission export**, with rewritten paths and a clean compilation check. A Git source archive of the repository is not that export. BibLaTeX/Biber in the SLR does not establish Editorial Manager compatibility; prefer checking the official `elsarticle` author–year/BibTeX workflow when preparing the actual submission template.

**R.** Do not imitate a downloaded publisher PDF's finished typography as if it were the required review layout. Keep journal submission sources distinct from GitHub release packaging.

## Highlights, artwork and optional graphical abstract

**P.** [Official highlights guidance](https://www.elsevier.com/researcher/author/tools-and-resources/highlights) specifies three to five short points, each at most 85 characters including spaces. Prepare a separate editable file. Their mandatory status for the current TR-D submission must be reconfirmed; the historical journal pack makes them mandatory.

**P.** [Artwork overview](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-overview) and [sizing guidance](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing) describe PDF/EPS vector artwork and TIFF/JPEG raster delivery, embedded fonts and legibility at the intended size. Raster targets are 300 dpi for halftones, 500 for mixed artwork and 1,000 for line art. Preserve vector scientific plots where possible. Captions, units and consistent numbering must accompany the figures; confirm final journal upload requirements.

**P.** [Graphical-abstract guidance](https://www.elsevier.com/researcher/author/tools-and-resources/graphical-abstract) gives a minimum 1,328 × 531 pixels (width × height), 300 dpi, a separate file and a readable left-to-right or top-to-bottom story. The guide says journal-specific instructions govern whether one is needed. Do not treat a graphical abstract as mandatory until verified for TR-D.

**R.** Use nicrainha when a figure needs colors, retain non-color distinctions and readable labels, and avoid decorative article text. This is our figure practice, not an Elsevier endorsement of that library.

## Data, code and declarations

**P.** [Research-data policy](https://www.elsevier.com/about/policies-and-standards/research-data) encourages sharing, appropriate repositories, persistent identifiers, data citation and transparent availability statements. Its definition includes software and methods as well as observations. The current **TR-D-specific data-policy level is unverified**; do not equate the general encouragement with a journal-specific mandatory repository rule.

**R.** Plan a code/version record, source-model commit and repair log, run configurations/seeds, input provenance/units, a data-access statement and shareable derived outputs. Separate public code from Dutch inputs we cannot redistribute. Provide an honest access route or restriction rather than claiming all data are open. A persistent archived software/data snapshot is preferable to a moving branch alone.

**P.** [Publishing ethics](https://www.elsevier.com/about/policies-and-standards/publishing-ethics) requires truthful reporting, proper attribution, responsible human authorship and appropriate declarations. Avoid duplicate submission and undisclosed reuse. The standalone SLR should be cited/disclosed as background as appropriate; do not transplant its text wholesale or call the research paper another SLR. All authors must approve authorship and submission. Funding, interests, contributions, permissions and any applicable ethics/privacy requirements must be resolved by the authors, not populated with invented statements.

**P.** [Current AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals): disclose substantive AI assistance in manuscript preparation; describe research/code/data-analysis assistance reproducibly in Methods. Humans remain responsible and AI tools cannot be authors. Maintain the tool/version/purpose and review record. Current policy distinguishes explanatory diagrams, reproducible data visualizations and primary research imagery; disclosure and provenance requirements differ. General-purpose generative image tools must not create graphical abstracts. This is the retrieved current policy, not the older blanket description sometimes repeated elsewhere.

## Submission pack to prepare, with portal confirmation

- Manuscript PDF and editable source bundle; confirm title-page/anonymization separation.
- Author names, affiliations, corresponding contact and agreed author order.
- Abstract and keywords in both manuscript and portal fields.
- Highlights; graphical abstract if required or chosen.
- Editable tables, figure files and captions; supplements with descriptions.
- Data/code availability, CRediT contributions, funding and competing-interest statements; applicable AI declaration and research-method details.
- Permissions for reused material and any applicable ethics approvals.
- Cover letter explaining environmental contribution and journal fit; confirm whether a separate upload is mandatory.
- Suggested-reviewer information if requested, without contacting reviewers.
- Final portal-generated PDF checked by the authors before approval.

This is a preparation list, not a claim that all items are mandatory in the current TR-D portal. Submission portal: [Editorial Manager TRD](https://www.editorialmanager.com/trd/). No account, draft submission or editor contact was initiated.

## Must verify before calling the template submission-ready

1. Live guide: article type; main-text limit and exclusions; abstract/keyword/title limits; layout; review/anonymization model.
2. Required submission uploads, declarations, reviewer suggestions and data-policy level.
3. Current open-access options, APC/currency/taxes, institutional agreements and any print-color charges. No fee is quoted here because the journal-specific page could not be verified; a corresponding author's affiliation and funding conditions matter.
4. Editorial Manager LaTeX/compiler compatibility and flattened source export.
5. Authors, affiliations, funding, permissions and the actual environmental claim/evidence design.
