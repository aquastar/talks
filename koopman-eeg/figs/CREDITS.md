# Credits and verified sources: Koopman EEG seizure prediction talk (IEEE BIBM 2026)

Collected 2026-11-17. Citations checked against Crossref (api.crossref.org) and PubMed. Numbers are quoted from the published abstract or the PMC full text. In quotes, an en dash in the source is written as a plain hyphen. Paths are relative to `koopman-eeg/figs/`.

---

## 1. WHO epilepsy fact sheet

- Source: World Health Organization, "Epilepsy" fact sheet, published 7 Feb 2024. https://www.who.int/news-room/fact-sheets/detail/epilepsy (fetched 2026-11-17)
- Numbers, quoted from the Key facts:
  - "Around 50 million people worldwide have epilepsy, making it one of the most common neurological diseases globally."
  - "It is estimated that up to 70% of people living with epilepsy could live seizure-free if properly diagnosed and treated."
  - From the Treatment section: "Up to 70% of people living with epilepsy could become seizure free with appropriate use of antiseizure medicines."
- Image: none.

## 2. Kwan and Brodie 2000

- Kwan P, Brodie MJ. Early identification of refractory epilepsy. N Engl J Med. 2000, 342(5):314-319. https://doi.org/10.1056/NEJM200002033420503 (Crossref verified, PMID 10660394)
- Numbers, quoted from the abstract:
  - "More than 30 percent of patients with epilepsy have inadequate control of seizures with drug therapy, but why this happens and whether it can be predicted are unknown."
  - "Among the 525 patients, 333 (63 percent) remained seizure-free during antiepileptic-drug treatment or after treatment was stopped." That means 37% were not seizure free. This is derived, the paper does not state it.
  - "Among 470 previously untreated patients, 222 (47 percent) became seizure-free during treatment with their first antiepileptic drug and 67 (14 percent) became seizure-free during treatment with a second or third drug."
- Image: none (NEJM, not open).

## 3. Cook et al. 2013, NeuroVista first in man

- Cook MJ, O'Brien TJ, Berkovic SF, Murphy M, Morokoff A, Fabinyi G, et al. Prediction of seizure likelihood with a long-term, implanted seizure advisory system in patients with drug-resistant epilepsy: a first-in-man study. Lancet Neurol. 2013, 12(6):563-571. https://doi.org/10.1016/S1474-4422(13)70075-9 (Crossref verified, 17 authors, PMID 23642342, NCT01043406)
- Numbers, quoted from the abstract:
  - "We implanted 15 patients with the advisory system."
  - "The device met enabling criteria in 11 patients upon completion of the data collection phase, with high likelihood performance estimate sensitivities ranging from 65% to 100%."
  - "Three patients' algorithms did not meet performance criteria and one patient required device removal because of an adverse event before sufficient training data were acquired."
  - Enabling criterion: "sensitivity of high-likelihood warnings greater than 65% and performance better than expected through chance prediction of randomly occurring events".
  - Safety: "11 device-related adverse events were noted within four months of implantation, two of which were serious (device migration, seroma)".
  - "We detected no significant changes in clinical effectiveness measures between baseline and 4 months after implantation."
- Image: NONE. I found no openly licensed photo of the NeuroVista device. Wikimedia Commons search gave nothing relevant, and Commons then rate limited us (HTTP 429).

## 4. Baud et al. 2018, multidien rhythms

- Baud MO, Kleen JK, Mirro EA, Andrechak JC, King-Stephens D, Chang EF, Rao VR. Multi-day rhythms modulate seizure risk in epilepsy. Nat Commun. 2018, 9:88. https://doi.org/10.1038/s41467-017-02577-y (Crossref verified, PMC5758806)
- Numbers:
  - Abstract: "Here, in 37 subjects with an implanted brain stimulation device that detects IEA and seizures over years, we find that IEA oscillates with circadian and subject-specific multidien (multi-day) periods."
  - Abstract: "Multidien periodicities, most commonly 20-30 days in duration, are robust and relatively stable for up to 10 years in men and women."
  - Abstract: "We show that seizures occur preferentially during the rising phase of multidien IEA rhythms."
  - Results: "... as well as longer periodicities (5.5-33 days) in most subjects (Fig. 2a ...). The median ratio of multidien to circadian peak amplitude was 1.4 (range 0.4-5.7; >1.0 in 27 subjects)".
  - Results, seizure subset: "Circular statistics of seizure timing confirmed significant entrainment to circadian and multidien rhythms in 12 and 13 out of 14 subjects, respectively".
  - Results, effect size: "small (risk ratio (RR) 1.2, 95% CI: 1.1-1.3) to very large effect sizes (RR 24.5, 95% CI: 3.4-175.9) ... and a large effect-size summary across subjects (unweighted RR 6.8, 95% CI: 3.1-15.1".
  - The paper gives no single percentage of patients with multidien cycles. The abstract says "most subjects". The closest numbers are "in most subjects" (5.5 to 33 days) and the cluster counts in Fig. 2 (9, 12 and 16 of 37 subjects for the weekly to biweekly, triweekly and monthly patterns, which together is all 37).
- Image: `papers/baud2018_fig1_multidien_seizures.png`. Fig. 1 panels e to j for one subject: daily IEA over 12 months with seizures marked as red dots, the 26 d and 10 d wavelet rhythms with the seizures falling on the rising phase, the periodogram, and the phase preference plots. Panel a is left out because it is NeuroPace artwork used with permission and is not CC BY.
- License: CC BY 4.0, (c) The Author(s) 2017. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5758806/ (full-resolution image from media.springernature.com). Changes: cropped.

## 5. Maturana et al. 2020, critical slowing down

- Maturana MI, Meisel C, Dell K, Karoly PJ, D'Souza W, Grayden DB, et al. Critical slowing down as a biomarker for seizure susceptibility. Nat Commun. 2020, 11:2172. https://doi.org/10.1038/s41467-020-15908-3 (Crossref verified, 13 authors, PMC7195436)
- Numbers:
  - Abstract: "Using long-term intracranial electroencephalography (iEEG) recordings from fourteen patients with focal epilepsy, we monitored key signatures of critical slowing down prior to seizures."
  - Abstract: "The metrics used to detect critical slowing down fluctuated over temporally long scales (hours to days), longer than would be detectable in standard clinical evaluation settings."
  - Results: "A gradual increase in the autocorrelation and variance signals, suggestive of critical slowing down, was observed in the tens-of-minutes to hours prior to lead seizures in most patients (9 of 14 patients ...)."
  - Introduction: "Critical slowing down refers to the tendency of a system to take longer to return to equilibrium after perturbations, indicated by an increase in signal variance and autocorrelation."
- Images:
  - `papers/maturana2020_fig2b_autocorr_variance_seizures.png`. Fig. 2b for Patient 1, days 260 to 300: the autocorrelation (ACFW), variance and spike rate signals with the long and short cycles. Seizures (red triangles) fall on the rising phases. Panel a (the implant illustration) is left out.
  - `papers/maturana2020_fig1ab_csd_concept.png`. Fig. 1a and b: a bifurcation diagram coloured by the system time constant, and the predicted autocorrelation response for the two routes into a seizure. This is optional concept art.
- License: CC BY 4.0, (c) The Author(s) 2020. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7195436/ (full-resolution image from media.springernature.com). Changes: cropped.

## 6. Scheffer et al. 2009, early-warning signals

- Scheffer M, Bascompte J, Brock WA, Brovkin V, Carpenter SR, Dakos V, Held H, van Nes EH, Rietkerk M, Sugihara G. Early-warning signals for critical transitions. Nature. 2009, 461(7260):53-59. https://doi.org/10.1038/nature08227 (Crossref verified)
- Abstract, quoted from nature.com: "Complex dynamical systems, ranging from ecosystems to financial markets and the climate, can have tipping points at which a sudden shift to a contrasting dynamical regime may occur. Although predicting such critical points before they are reached is extremely difficult, work in different scientific fields is now suggesting the existence of generic early-warning signals that may indicate for a wide class of systems if a critical threshold is approaching."
- One-line summary, in my own words (not a quote): near a tipping point a system recovers more and more slowly from small perturbations ("critical slowing down"), so its fluctuations show rising autocorrelation and variance. Maturana 2020 has a quotable definition (item 5). The full text of Scheffer is paywalled, so I did not quote its body text.
- Image: none (paywalled).

## 7. Koopman 1931

- Koopman BO. Hamiltonian systems and transformation in Hilbert space. Proc Natl Acad Sci USA. 1931, 17(5):315-318. https://doi.org/10.1073/pnas.17.5.315 (Crossref verified, PMC1076052). The printed page says "TRANSFORMATIONS" in the plural. Crossref and PNAS give "Transformation". Use the Crossref form in the citation.
- Image: `papers/koopman1931_pnas_page315_top.png`. The top of page 315: title, "By B. O. Koopman, Department of Mathematics, Columbia University, Communicated March 23, 1931", and the first paragraph. It is a 625 px wide scan, fine at about half-slide size.
- License: a 1931 PNAS scan served free on PMC. No CC license is stated. PNAS lets authors and readers reuse it with citation, and it is likely public domain in the US (published 1931, copyright very likely not renewed). Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC1076052/ (page image pnas01721-0085.png). The PNAS PDF returned 403, and the PMC PDF is behind a JavaScript challenge.
- Photo of Bernard O. Koopman: NOT FOUND. Wikipedia has no portrait. Commons search was rate limited. The INFORMS biography page (https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Koopman-Bernard) has no image. MacTutor did not connect.

## 8. Origins of DMD

- Schmid PJ. Dynamic mode decomposition of numerical and experimental data. J Fluid Mech. 2010, 656:5-28. https://doi.org/10.1017/S0022112010001217 (Crossref verified)
- Rowley CW, Mezić I, Bagheri S, Schlatter P, Henningson DS. Spectral analysis of nonlinear flows. J Fluid Mech. 2009, 641:115-127. https://doi.org/10.1017/S0022112009992059 (Crossref verified, issue date 25 Dec 2009)
- Image: `papers/dmd_mode_joukowsky_vortex_street_wikipedia.png`. A DMD approximation of the dominant vortex-shedding mode (real part) in the Karman vortex street behind a Joukowsky airfoil, shown as a red/green field. It is an airfoil wake, not a cylinder wake, and it is low resolution (573 px), so use it small.
- License: CC BY-SA 3.0 or GFDL, by Wikipedia user T784303. The flow simulation is credited to Jan Schulze and Jörn Sesterhenn, UniBW München, on the companion file. Source: https://en.wikipedia.org/wiki/File:Joukowsky_Karman_Vortex_Street_EV_real.png (used in the Wikipedia article "Dynamic mode decomposition"). Changes: cropped.
- Not obtained: the matching flow snapshot (Commons file Joukowsky_Karman_Vortex_Street_s.png, CC BY-SA 3.0) was blocked by repeated HTTP 429 from upload.wikimedia.org. arXiv candidates (2102.12086, 1312.0041, 1702.01453) all use the arXiv non-exclusive license, not CC, so they were not used.

## 9. Brunton, Johnson, Ojemann, Kutz 2016

- Brunton BW, Johnson LA, Ojemann JG, Kutz JN. Extracting spatial-temporal coherent patterns in large-scale neural recordings using dynamic mode decomposition. J Neurosci Methods. 2016, 258:1-15. https://doi.org/10.1016/j.jneumeth.2015.10.010 (Crossref verified, PMID 26529367, arXiv:1409.5496)
- Image: `papers/brunton2016_fig1_dmd_ecog_overview.png`. Fig. 1: (a) 45-channel ECoG, raw data with the DMD approximation overlaid, plus the electrode grid on the brain. (b) The decomposition X̂(t) = Φ Λ^t z0 (spatial modes, temporal eigenvalues, weights). (c) Reconstruction error against the number of modes r. Caption: "DMD applied to a 500 msec window of 45-channel ECoG data sampled at 200 Hz."
- License: the arXiv non-exclusive distribution license 1.0, not CC. The journal version is Elsevier and not open access. Use with full citation as a scholarly figure in the talk. Source: https://arxiv.org/e-print/1409.5496 (Figure1.pdf, rendered at 200 dpi and cropped).

## 10. Proctor and Eckhoff 2015

- Proctor JL, Eckhoff PA. Discovering dynamic patterns from infectious disease data using dynamic mode decomposition. Int Health. 2015, 7(2):139-145. https://doi.org/10.1093/inthealth/ihv009 (Crossref verified, PMC4379984)
- Abstract: "We demonstrate the method on three different infectious disease sets including Google Flu Trends data, pre-vaccination measles in the UK, and paralytic poliomyelitis wild type-1 cases in Nigeria."
- Images:
  - `papers/proctor2015_fig2_measles_dmd.png`. The pre-vaccination measles panel of Fig. 2 (UK, 1944 to 1966): raw data, normalized snapshots, mode selection by frequency (peak near 1/yr), eigenvalue spectrum, and the phase of the dynamic mode on a UK map.
  - `papers/proctor2015_fig2_flu_measles_polio_full.png`. The full Fig. 2 with all three diseases (Google Flu, measles, polio in Nigeria). It is 777 px wide, the highest resolution PMC serves.
- License: CC BY-NC 4.0, (c) The Author 2015, Oxford University Press for RSTMH. Non-commercial reuse is allowed, which fits a conference talk. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4379984/

## 11. Mormann et al. 2007

- Mormann F, Andrzejak RG, Elger CE, Lehnertz K. Seizure prediction: the long and winding road. Brain. 2007, 130(2):314-333. https://doi.org/10.1093/brain/awl241 (Crossref verified, PMID 17008335, online 28 Sep 2006)
- History sentence, quoted from the abstract: "While most of the studies published in the 1990s and around the turn of the millennium yielded rather promising results, more recent evaluations could not reproduce these optimistic findings, thus raising a debate about the validity and reliability of previous investigations."
- Image: none.

## 12. Mezić 2005, and people photos

- Mezić I. Spectral properties of dynamical systems, model reduction and decompositions. Nonlinear Dyn. 2005, 41(1-3):309-325. https://doi.org/10.1007/s11071-005-2824-x (Crossref verified)
- Photos. None of the three has a Wikipedia or Commons photo. These come from university pages and carry no open license (all rights reserved, university or photographer). Use them only for identification, with credit:
  - `people/mezic_igor_ucsb.jpg` (800x672). Igor Mezić headshot. Source: https://me.ucsb.edu/people/igor-mezic (file /sites/default/files/2023-10/Mezic2_0.jpg)
  - `people/brunton_steven_uw.jpg` (200x250, small). Steven L. Brunton headshot. Source: https://www.me.washington.edu/facultyfinder/steve-brunton (image from facultydb.engr.washington.edu/api/profile-photo/steve-brunton)
  - `people/kutz_nathan_uw.jpg` (676x1000). J. Nathan Kutz portrait. Source: https://amath.washington.edu/people/j-nathan-kutz (alt text "NKutzPortrait")

## 13. Korda and Mezić 2018

- Korda M, Mezić I. Linear predictors for nonlinear dynamical systems: Koopman operator meets model predictive control. Automatica. 2018, 93:149-160. https://doi.org/10.1016/j.automatica.2018.03.046 (Crossref verified)

## 14. Susuki and Mezić 2011

- Susuki Y, Mezić I. Nonlinear Koopman modes and coherency identification of coupled swing dynamics. IEEE Trans Power Syst. 2011, 26(4):1894-1904. https://doi.org/10.1109/TPWRS.2010.2103369 (Crossref verified)

---

## Not verified or not obtained

- UNVERIFIED: a single "percentage of patients with multidien cycles" for Baud 2018. The paper says "most subjects" and does not give one number. Use "most of 37" or the counts above.
- NOT FOUND: an openly licensed NeuroVista device photo, and any photo of B. O. Koopman.
- BLOCKED: Wikimedia Commons API and upload.wikimedia.org/commons (HTTP 429, repeated over about 5 minutes). The PNAS PDF (403) and PMC PDFs (JavaScript proof-of-work page) were also blocked. The en.wikipedia local upload path worked.
