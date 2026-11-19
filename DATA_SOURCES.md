# Sources and methodology

## Provenance

| Source | Use | Access |
| --- | --- | --- |
| Headcount Labs, `tech-jobs`, snapshot 2026-10-19 | Discover a starting list of employer career-board identifiers | <https://huggingface.co/datasets/HeadcountLabs/tech-jobs> |
| Greenhouse public Job Board API | Current published posting metadata and descriptions used for annotations | <https://developers.greenhouse.io/job-board.html> |
| Lever public Postings API | Current published posting metadata and descriptions used for annotations | <https://github.com/lever/postings-api> |

The included `data/jobs.json` was collected from the selected employer feeds. Its `metadata.generated_at`, source reports, and per-job `last_checked_at` provide the actual check times. It is not a reproduction of the complete Headcount snapshot. Employer selection is neither exhaustive nor random.

## Credit and reuse

Employer discovery data: **Headcount Labs, ODbL 1.0**. <https://headcountlabs.com/>. Location data in the original discovery dataset includes OpenStreetMap contributors and Overture Maps. Credit those sources when reusing the discovery list. This project's distributed database and source-selection compilation are offered under **ODbL 1.0**, subject to rights in their underlying contents: <https://opendatacommons.org/licenses/odbl/1-0/>. Identify modifications and retain this attribution when redistributing a modified database.

Employer descriptions belong to their employers; this project does not claim a license over their text or trademarks. It processes descriptions to produce short evidence excerpts and annotations, and does not publish full descriptions or recruiter contact details. Software licensing, if added by the repository owner, is separate from database licensing.

## Screening rules

- Geography: selected Bay Area cities or explicit California-remote location evidence. Bare ambiguous names such as Dublin require California evidence. US-remote roles whose California eligibility is unknown have a separate, opt-in classification. A salary paragraph mentioning California does not establish remote eligibility.
- Roles: keyword categories covering MIS/business, data, product/project, finance, operations, revenue/customer work, security, IT, and software. This is an imperfect classification of titles, not an official occupation taxonomy.
- Employment: exclude explicit internships, co-ops, temporary, part-time, and contract labels where available. Unknown employment type remains visible and must be checked.
- Experience: exclude senior titles and numeric minima above two years; keep mixed 0–2 and 3+ alternatives as needs review. Required and preferred sections are distinguished by text rules. Unstated experience is never converted to zero. The default screen includes 0–2 stated minima and entry/new-grad titles.
- Graduation: explicit graduation-year mentions are tracked separately from posting year. A 2026 posting is not automatically a class-of-2026 role. No stated graduation restriction is not confirmed eligibility.
- Dates: original publication and source-update timestamps remain separate. Future publication dates are flagged and left unknown. Collection dates do not become posting dates. Application deadlines are included only from explicit source fields.
- Compensation: retain stated currency and interval. Convert Greenhouse cents to currency units, prefer explicitly California-labelled ranges where available, and leave missing units unspecified. Do not annualize hourly rates or assume a yearly unit from the amount's size. Compare annual USD advertised range midpoints only when a role group has at least five disclosures. These are not actual offers, guaranteed base pay, or total compensation.
- Skills: dictionary-based distinct-posting mention counts. Mentions include required, preferred, and descriptive contexts. A short skill list cannot capture every useful skill.
- Deduplication: stable provider/board/posting IDs and canonical posting URL. Different requisitions with matching titles remain separate. Multi-location postings count once overall and once per matched city.
- Refresh: complete source absence can change a retained posting to no longer listed; a failed source produces unverified status. An all-source failure never replaces the last good dataset. A still-published role that fails an updated screen is removed from the screened dataset without being called closed.

## Data quality limits

Rules can misread alternative degree routes, years of tool-specific experience, remote restrictions, and unfamiliar titles. The dashboard exposes experience excerpts and source links for review. Missing salary or deadline values remain unknown. Narrow filters can produce small samples; the interface states counts and suppresses unsupported salary comparisons. The findings describe observed postings, not completed hires, applicant competition, or total regional demand.
