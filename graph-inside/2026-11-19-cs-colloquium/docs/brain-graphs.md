# How the two brain graphs on slide 31 were made

Both pictures are computed from public data. Nothing is drawn by hand.

## EEG (figs/eeg-graph-pli-physionet.png)
- Data: PhysioNet EEG Motor Movement/Imagery, subjects 1 to 10, run 1 (eyes open rest, 1 minute), loaded with MNE (`mne.datasets.eegbci`).
- Steps: standard 10-05 montage, average reference, band pass 8 to 13 Hz, Hilbert phase, phase lag index for every electrode pair, median over the 10 people.
- T9 and T10 are left out (edge electrodes, strongly connected to everything in this set, likely noise). 62 electrodes remain.
- Edges: the strongest 4% of pairs (76 edges). Width and color follow strength.

## fMRI (figs/fmri-graph-msdl-partial.png)
- Data: nilearn `fetch_development_fmri`, first 10 subjects, MSDL probabilistic atlas (39 regions).
- Steps: `NiftiMapsMasker` with the provided confounds, `ConnectivityMeasure(kind='partial correlation')`, mean over the 10 people.
- Edges: the strongest 8% by absolute value, drawn with `plotting.plot_connectome`, left lateral view.

## Numbers on the slide, checked against the papers
- Tang et al., ICLR 2022: seizure detection AUROC 0.875 on TUSZ v1.5.2.
- Song et al., DGCNN, IEEE TAC 2020: 90.4% subject dependent on SEED.
- Finn et al., Nature Neuroscience 2015: 117 of 126 (92.9%), Rest1 to Rest2, whole brain. Fluid intelligence r = 0.50 (notes only).
- Crossley et al., Brain 2014: lesions across 26 disorders more likely on hubs (P < 1e-4).
- Wilkins et al., Scientific Reports 2014: default mode network most connected during preferred music.
