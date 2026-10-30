# CD-QFed results report

*COMPLETE grid: 13950 / 13950 configs*  
Generated 2026-10-29 21:41:12 UTC, profile `paper`, backend `torch/cuda`, 60 rounds, 10 seeds.

> Hardware error rates are [PLACEHOLDER]; accuracies are PROXY numbers (as stated in the notebook's own design).

## Headline (paired comparisons by verdict)

| metric | GOOD (significant) | bad trend (n.s.) | good trend (n.s.) |
|---|---|---|---|
| accuracy | 14 | 0 | 10 |
| client-drift E_drift | 24 | 0 | 0 |
| drift alignment S_CDA | 23 | 1 | 0 |

## table1 main results

Main results per scale (all arms, alphas and channels pooled). Mean ± 95% CI over seeds (seed-level means). * = proposed CD-QFed. Higher is better for accuracy and S_CDA, lower for E_drift.

| scale | variant | runs | seeds | accuracy | client drift E_drift | alignment S_CDA |
|---|---|---|---|---|---|---|
| small | base | 450 | 10 | 0.3926 ± 0.0310 | 0.0238 ± 0.0025 | 0.2809 ± 0.0113 |
| small | JEQFL | 450 | 10 | 0.3994 ± 0.0286 | 0.0239 ± 0.0024 | 0.2792 ± 0.0114 |
| small | M4a | 450 | 10 | 0.3953 ± 0.0301 | 0.0247 ± 0.0024 | 0.2771 ± 0.0105 |
| small | M4ab | 450 | 10 | 0.3971 ± 0.0290 | 0.0253 ± 0.0025 | 0.2779 ± 0.0111 |
| small | M5b | 450 | 10 | 0.3840 ± 0.0306 | 0.0197 ± 0.0033 | 0.3408 ± 0.0102 |
| small | M3 | 450 | 10 | 0.3927 ± 0.0307 | 0.0236 ± 0.0024 | 0.2815 ± 0.0114 |
| small | M2 | 450 | 10 | 0.3963 ± 0.0320 | 0.0237 ± 0.0025 | 0.2834 ± 0.0113 |
| small | CDQ | 450 | 10 | 0.3974 ± 0.0220 | 0.0341 ± 0.0065 | 0.2989 ± 0.0104 |
| small | CDQ-lit * | 450 | 10 | 0.3996 ± 0.0260 | 0.0123 ± 0.0014 | 0.3510 ± 0.0133 |
| medium | base | 450 | 10 | 0.4002 ± 0.0254 | 0.0205 ± 0.0020 | 0.2501 ± 0.0202 |
| medium | JEQFL | 450 | 10 | 0.4003 ± 0.0260 | 0.0206 ± 0.0020 | 0.2509 ± 0.0213 |
| medium | M4a | 450 | 10 | 0.4006 ± 0.0260 | 0.0215 ± 0.0018 | 0.2451 ± 0.0204 |
| medium | M4ab | 450 | 10 | 0.4013 ± 0.0261 | 0.0220 ± 0.0019 | 0.2483 ± 0.0201 |
| medium | M5b | 450 | 10 | 0.3948 ± 0.0225 | 0.0184 ± 0.0037 | 0.3202 ± 0.0146 |
| medium | M3 | 450 | 10 | 0.3999 ± 0.0257 | 0.0204 ± 0.0020 | 0.2508 ± 0.0202 |
| medium | M2 | 450 | 10 | 0.3992 ± 0.0249 | 0.0205 ± 0.0022 | 0.2567 ± 0.0192 |
| medium | CDQ | 450 | 10 | 0.4025 ± 0.0192 | 0.0297 ± 0.0032 | 0.2879 ± 0.0185 |
| medium | CDQ-lit * | 450 | 10 | 0.4066 ± 0.0196 | 0.0132 ± 0.0012 | 0.3258 ± 0.0157 |
| large | base | 450 | 10 | 0.3690 ± 0.0147 | 0.0207 ± 0.0034 | 0.2400 ± 0.0226 |
| large | JEQFL | 450 | 10 | 0.3701 ± 0.0146 | 0.0205 ± 0.0032 | 0.2453 ± 0.0249 |
| large | M4a | 450 | 10 | 0.3723 ± 0.0142 | 0.0218 ± 0.0030 | 0.2359 ± 0.0229 |
| large | M4ab | 450 | 10 | 0.3745 ± 0.0143 | 0.0221 ± 0.0031 | 0.2435 ± 0.0231 |
| large | M5b | 450 | 10 | 0.3598 ± 0.0159 | 0.0188 ± 0.0061 | 0.3164 ± 0.0212 |
| large | M3 | 450 | 10 | 0.3694 ± 0.0146 | 0.0205 ± 0.0033 | 0.2412 ± 0.0225 |
| large | M2 | 450 | 10 | 0.3745 ± 0.0130 | 0.0203 ± 0.0032 | 0.2477 ± 0.0257 |
| large | CDQ | 450 | 10 | 0.3685 ± 0.0116 | 0.0283 ± 0.0035 | 0.2839 ± 0.0358 |
| large | CDQ-lit * | 450 | 10 | 0.3754 ± 0.0159 | 0.0129 ± 0.0027 | 0.3121 ± 0.0235 |

## table2 accuracy by channel

Accuracy by channel quality (mean ± 95% CI over seeds).

| scale | variant | channel=good | channel=moderate | channel=poor |
|---|---|---|---|---|
| small | base | 0.3935 ± 0.0327 | 0.3962 ± 0.0355 | 0.3882 ± 0.0363 |
| small | JEQFL | 0.4019 ± 0.0333 | 0.4037 ± 0.0346 | 0.3927 ± 0.0325 |
| small | M4a | 0.3963 ± 0.0317 | 0.3997 ± 0.0359 | 0.3899 ± 0.0349 |
| small | M4ab | 0.3963 ± 0.0321 | 0.4029 ± 0.0327 | 0.3920 ± 0.0329 |
| small | M5b | 0.3985 ± 0.0384 | 0.3978 ± 0.0357 | 0.3557 ± 0.0298 |
| small | M3 | 0.3936 ± 0.0323 | 0.3954 ± 0.0354 | 0.3890 ± 0.0357 |
| small | M2 | 0.3969 ± 0.0328 | 0.3989 ± 0.0395 | 0.3930 ± 0.0355 |
| small | CDQ | 0.4184 ± 0.0278 | 0.4094 ± 0.0243 | 0.3643 ± 0.0172 |
| small | CDQ-lit * | 0.4151 ± 0.0298 | 0.4094 ± 0.0274 | 0.3744 ± 0.0266 |
| medium | base | 0.4143 ± 0.0324 | 0.3941 ± 0.0278 | 0.3921 ± 0.0249 |
| medium | JEQFL | 0.4076 ± 0.0322 | 0.4042 ± 0.0326 | 0.3892 ± 0.0194 |
| medium | M4a | 0.4158 ± 0.0341 | 0.3944 ± 0.0284 | 0.3916 ± 0.0242 |
| medium | M4ab | 0.4177 ± 0.0339 | 0.3989 ± 0.0298 | 0.3873 ± 0.0238 |
| medium | M5b | 0.4073 ± 0.0305 | 0.4032 ± 0.0290 | 0.3738 ± 0.0268 |
| medium | M3 | 0.4138 ± 0.0325 | 0.3934 ± 0.0276 | 0.3927 ± 0.0254 |
| medium | M2 | 0.4143 ± 0.0317 | 0.3926 ± 0.0268 | 0.3907 ± 0.0263 |
| medium | CDQ | 0.4135 ± 0.0275 | 0.4102 ± 0.0240 | 0.3838 ± 0.0203 |
| medium | CDQ-lit * | 0.4150 ± 0.0305 | 0.4074 ± 0.0270 | 0.3974 ± 0.0119 |
| large | base | 0.3664 ± 0.0186 | 0.3706 ± 0.0161 | 0.3700 ± 0.0188 |
| large | JEQFL | 0.3708 ± 0.0149 | 0.3682 ± 0.0193 | 0.3712 ± 0.0183 |
| large | M4a | 0.3683 ± 0.0164 | 0.3754 ± 0.0168 | 0.3732 ± 0.0184 |
| large | M4ab | 0.3724 ± 0.0182 | 0.3765 ± 0.0150 | 0.3745 ± 0.0169 |
| large | M5b | 0.3693 ± 0.0182 | 0.3614 ± 0.0177 | 0.3487 ± 0.0272 |
| large | M3 | 0.3664 ± 0.0189 | 0.3710 ± 0.0160 | 0.3708 ± 0.0183 |
| large | M2 | 0.3745 ± 0.0168 | 0.3740 ± 0.0155 | 0.3749 ± 0.0182 |
| large | CDQ | 0.3819 ± 0.0169 | 0.3725 ± 0.0112 | 0.3512 ± 0.0174 |
| large | CDQ-lit * | 0.3847 ± 0.0254 | 0.3794 ± 0.0199 | 0.3622 ± 0.0177 |

## table3 drift by channel

Client drift E_drift by channel quality (mean ± 95% CI over seeds; lower is better).

| scale | variant | channel=good | channel=moderate | channel=poor |
|---|---|---|---|---|
| small | base | 0.0060 ± 0.0008 | 0.0123 ± 0.0014 | 0.0531 ± 0.0058 |
| small | JEQFL | 0.0057 ± 0.0007 | 0.0127 ± 0.0014 | 0.0534 ± 0.0054 |
| small | M4a | 0.0069 ± 0.0011 | 0.0134 ± 0.0014 | 0.0539 ± 0.0054 |
| small | M4ab | 0.0073 ± 0.0011 | 0.0140 ± 0.0016 | 0.0545 ± 0.0054 |
| small | M5b | 0.0048 ± 0.0011 | 0.0120 ± 0.0022 | 0.0424 ± 0.0075 |
| small | M3 | 0.0059 ± 0.0009 | 0.0122 ± 0.0013 | 0.0527 ± 0.0058 |
| small | M2 | 0.0055 ± 0.0007 | 0.0120 ± 0.0013 | 0.0537 ± 0.0063 |
| small | CDQ | 0.0042 ± 0.0004 | 0.0129 ± 0.0015 | 0.0853 ± 0.0183 |
| small | CDQ-lit * | 0.0031 ± 0.0002 | 0.0076 ± 0.0006 | 0.0260 ± 0.0039 |
| medium | base | 0.0056 ± 0.0004 | 0.0113 ± 0.0007 | 0.0445 ± 0.0054 |
| medium | JEQFL | 0.0053 ± 0.0004 | 0.0115 ± 0.0007 | 0.0450 ± 0.0050 |
| medium | M4a | 0.0065 ± 0.0005 | 0.0123 ± 0.0006 | 0.0458 ± 0.0049 |
| medium | M4ab | 0.0069 ± 0.0007 | 0.0126 ± 0.0008 | 0.0465 ± 0.0051 |
| medium | M5b | 0.0042 ± 0.0006 | 0.0103 ± 0.0019 | 0.0408 ± 0.0103 |
| medium | M3 | 0.0055 ± 0.0004 | 0.0113 ± 0.0007 | 0.0442 ± 0.0052 |
| medium | M2 | 0.0050 ± 0.0003 | 0.0111 ± 0.0007 | 0.0455 ± 0.0060 |
| medium | CDQ | 0.0035 ± 0.0003 | 0.0114 ± 0.0008 | 0.0743 ± 0.0091 |
| medium | CDQ-lit * | 0.0026 ± 0.0004 | 0.0069 ± 0.0010 | 0.0300 ± 0.0028 |
| large | base | 0.0059 ± 0.0014 | 0.0109 ± 0.0021 | 0.0453 ± 0.0075 |
| large | JEQFL | 0.0055 ± 0.0012 | 0.0109 ± 0.0019 | 0.0450 ± 0.0069 |
| large | M4a | 0.0069 ± 0.0014 | 0.0121 ± 0.0022 | 0.0465 ± 0.0065 |
| large | M4ab | 0.0070 ± 0.0013 | 0.0123 ± 0.0020 | 0.0469 ± 0.0068 |
| large | M5b | 0.0044 ± 0.0013 | 0.0099 ± 0.0035 | 0.0421 ± 0.0140 |
| large | M3 | 0.0058 ± 0.0013 | 0.0108 ± 0.0020 | 0.0449 ± 0.0073 |
| large | M2 | 0.0050 ± 0.0010 | 0.0103 ± 0.0018 | 0.0455 ± 0.0073 |
| large | CDQ | 0.0033 ± 0.0004 | 0.0102 ± 0.0008 | 0.0716 ± 0.0097 |
| large | CDQ-lit * | 0.0027 ± 0.0006 | 0.0070 ± 0.0015 | 0.0290 ± 0.0065 |

## table4 accuracy by alpha

Accuracy by data-heterogeneity level alpha (mean ± 95% CI over seeds).

| scale | variant | alpha=25 | alpha=50 | alpha=100 |
|---|---|---|---|---|
| small | base | 0.3877 ± 0.0264 | 0.3927 ± 0.0333 | 0.3975 ± 0.0349 |
| small | JEQFL | 0.3894 ± 0.0274 | 0.4005 ± 0.0301 | 0.4083 ± 0.0302 |
| small | M4a | 0.3910 ± 0.0268 | 0.3954 ± 0.0319 | 0.3996 ± 0.0334 |
| small | M4ab | 0.3916 ± 0.0267 | 0.3958 ± 0.0300 | 0.4038 ± 0.0323 |
| small | M5b | 0.3776 ± 0.0282 | 0.3854 ± 0.0326 | 0.3889 ± 0.0346 |
| small | M3 | 0.3872 ± 0.0265 | 0.3934 ± 0.0330 | 0.3974 ± 0.0344 |
| small | M2 | 0.3911 ± 0.0306 | 0.3980 ± 0.0336 | 0.3997 ± 0.0336 |
| small | CDQ | 0.3980 ± 0.0207 | 0.3948 ± 0.0244 | 0.3993 ± 0.0240 |
| small | CDQ-lit * | 0.4007 ± 0.0270 | 0.3986 ± 0.0238 | 0.3997 ± 0.0286 |
| medium | base | 0.4008 ± 0.0235 | 0.4030 ± 0.0260 | 0.3967 ± 0.0296 |
| medium | JEQFL | 0.4009 ± 0.0246 | 0.4037 ± 0.0239 | 0.3963 ± 0.0320 |
| medium | M4a | 0.4004 ± 0.0238 | 0.4036 ± 0.0266 | 0.3978 ± 0.0306 |
| medium | M4ab | 0.3994 ± 0.0227 | 0.4031 ± 0.0268 | 0.4014 ± 0.0314 |
| medium | M5b | 0.3971 ± 0.0237 | 0.3973 ± 0.0179 | 0.3899 ± 0.0291 |
| medium | M3 | 0.4006 ± 0.0235 | 0.4026 ± 0.0261 | 0.3966 ± 0.0301 |
| medium | M2 | 0.3987 ± 0.0223 | 0.4028 ± 0.0266 | 0.3961 ± 0.0295 |
| medium | CDQ | 0.4041 ± 0.0197 | 0.3982 ± 0.0194 | 0.4053 ± 0.0231 |
| medium | CDQ-lit * | 0.4107 ± 0.0193 | 0.4036 ± 0.0198 | 0.4056 ± 0.0233 |
| large | base | 0.3642 ± 0.0192 | 0.3688 ± 0.0145 | 0.3740 ± 0.0146 |
| large | JEQFL | 0.3678 ± 0.0145 | 0.3684 ± 0.0149 | 0.3740 ± 0.0176 |
| large | M4a | 0.3692 ± 0.0174 | 0.3718 ± 0.0164 | 0.3760 ± 0.0132 |
| large | M4ab | 0.3711 ± 0.0145 | 0.3737 ± 0.0156 | 0.3787 ± 0.0156 |
| large | M5b | 0.3561 ± 0.0190 | 0.3597 ± 0.0183 | 0.3636 ± 0.0148 |
| large | M3 | 0.3649 ± 0.0195 | 0.3701 ± 0.0138 | 0.3732 ± 0.0145 |
| large | M2 | 0.3720 ± 0.0156 | 0.3729 ± 0.0148 | 0.3785 ± 0.0136 |
| large | CDQ | 0.3641 ± 0.0146 | 0.3707 ± 0.0133 | 0.3709 ± 0.0101 |
| large | CDQ-lit * | 0.3712 ± 0.0195 | 0.3758 ± 0.0168 | 0.3793 ± 0.0131 |

## table5 paired pooled

Paired comparison of CD-QFed against every baseline, pooled per scale (paired t-test, Benjamini-Hochberg q within each metric).

| scale | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | base | accuracy | 450 | 0.3754 | 0.369 | 0.006446 | 1.747 | 0.01146 | 0.009944 | 0.02751 | 549 | GOOD (significant) |
| medium | base | accuracy | 450 | 0.4066 | 0.4002 | 0.006449 | 1.612 | 0.004104 | 0.00164 | 0.01407 | 425 | GOOD (significant) |
| small | base | accuracy | 450 | 0.3996 | 0.3926 | 0.007017 | 1.787 | 0.01335 | 0.001084 | 0.02776 | 573 | GOOD (significant) |
| large | base | client-drift E_drift | 450 | 0.01288 | 0.02069 | -0.007807 | -37.74 | 8.862e-29 | 1.272e-55 | 1.418e-28 | 25 | GOOD (significant) |
| medium | base | client-drift E_drift | 450 | 0.01319 | 0.02049 | -0.007295 | -35.61 | 9.477e-35 | 9.32e-57 | 3.249e-34 | 20 | GOOD (significant) |
| small | base | client-drift E_drift | 450 | 0.01225 | 0.0238 | -0.01155 | -48.52 | 2.491e-23 | 1.103e-57 | 2.594e-23 | 32 | GOOD (significant) |
| large | base | drift alignment S_CDA | 450 | 0.3121 | 0.24 | 0.07208 | 30.03 | 1.286e-79 | 5.009e-65 | 4.408e-79 | 7 | GOOD (significant) |
| medium | base | drift alignment S_CDA | 450 | 0.3258 | 0.2501 | 0.07562 | 30.23 | 2.73e-81 | 4.822e-68 | 1.638e-80 | 7 | GOOD (significant) |
| small | base | drift alignment S_CDA | 450 | 0.351 | 0.2809 | 0.07003 | 24.93 | 1.857e-64 | 5.749e-61 | 2.622e-64 | 9 | GOOD (significant) |
| large | JEQFL | accuracy | 450 | 0.3754 | 0.3701 | 0.005356 | 1.447 | 0.03199 | 0.002756 | 0.05119 | 764 | good trend (n.s.) |
| medium | JEQFL | accuracy | 450 | 0.4066 | 0.4003 | 0.00632 | 1.579 | 0.008535 | 0.0008863 | 0.02276 | 507 | GOOD (significant) |
| small | JEQFL | accuracy | 450 | 0.3996 | 0.3994 | 0.0002309 | 0.0578 | 0.9369 | 0.3804 | 0.9369 | 5.636e+05 | good trend (n.s.) |
| large | JEQFL | client-drift E_drift | 450 | 0.01288 | 0.02048 | -0.007601 | -37.11 | 2.278e-28 | 5.107e-54 | 3.417e-28 | 26 | GOOD (significant) |
| medium | JEQFL | client-drift E_drift | 450 | 0.01319 | 0.02062 | -0.007432 | -36.04 | 4.788e-34 | 4.806e-59 | 1.436e-33 | 21 | GOOD (significant) |
| small | JEQFL | client-drift E_drift | 450 | 0.01225 | 0.02393 | -0.01168 | -48.8 | 2.866e-25 | 3.643e-59 | 3.44e-25 | 29 | GOOD (significant) |
| large | JEQFL | drift alignment S_CDA | 450 | 0.3121 | 0.2453 | 0.06675 | 27.21 | 5.278e-67 | 1.555e-57 | 7.916e-67 | 9 | GOOD (significant) |
| medium | JEQFL | drift alignment S_CDA | 450 | 0.3258 | 0.2509 | 0.07485 | 29.83 | 1.273e-78 | 8.064e-65 | 3.395e-78 | 7 | GOOD (significant) |
| small | JEQFL | drift alignment S_CDA | 450 | 0.351 | 0.2792 | 0.07171 | 25.68 | 1.409e-71 | 9.93e-64 | 2.819e-71 | 8 | GOOD (significant) |
| large | M4a | accuracy | 450 | 0.3754 | 0.3723 | 0.003111 | 0.8356 | 0.2206 | 0.3245 | 0.2786 | 2347 | good trend (n.s.) |
| medium | M4a | accuracy | 450 | 0.4066 | 0.4006 | 0.006019 | 1.502 | 0.007459 | 0.0009252 | 0.02238 | 489 | GOOD (significant) |
| small | M4a | accuracy | 450 | 0.3996 | 0.3953 | 0.00432 | 1.093 | 0.1218 | 0.01879 | 0.1719 | 1470 | good trend (n.s.) |
| large | M4a | client-drift E_drift | 450 | 0.01288 | 0.02183 | -0.008946 | -40.99 | 1.287e-33 | 2.882e-58 | 3.431e-33 | 21 | GOOD (significant) |
| medium | M4a | client-drift E_drift | 450 | 0.01319 | 0.02154 | -0.008349 | -38.76 | 1.346e-37 | 7.919e-60 | 1.077e-36 | 18 | GOOD (significant) |
| small | M4a | client-drift E_drift | 450 | 0.01225 | 0.02473 | -0.01248 | -50.46 | 3.981e-26 | 9.734e-61 | 5.028e-26 | 28 | GOOD (significant) |
| large | M4a | drift alignment S_CDA | 450 | 0.3121 | 0.2359 | 0.07617 | 32.29 | 2.115e-85 | 1.222e-67 | 5.075e-84 | 6 | GOOD (significant) |
| medium | M4a | drift alignment S_CDA | 450 | 0.3258 | 0.2451 | 0.08068 | 32.92 | 2.93e-83 | 2.089e-69 | 3.516e-82 | 7 | GOOD (significant) |
| small | M4a | drift alignment S_CDA | 450 | 0.351 | 0.2771 | 0.07381 | 26.63 | 3.59e-67 | 4.556e-64 | 5.743e-67 | 9 | GOOD (significant) |
| large | M4ab | accuracy | 450 | 0.3754 | 0.3745 | 0.0009358 | 0.2499 | 0.7042 | 0.94 | 0.7348 | 2.446e+04 | good trend (n.s.) |
| medium | M4ab | accuracy | 450 | 0.4066 | 0.4013 | 0.005342 | 1.331 | 0.01581 | 0.002968 | 0.02829 | 602 | GOOD (significant) |
| small | M4ab | accuracy | 450 | 0.3996 | 0.3971 | 0.002558 | 0.6442 | 0.3774 | 0.09164 | 0.4313 | 4525 | good trend (n.s.) |
| large | M4ab | client-drift E_drift | 450 | 0.01288 | 0.02209 | -0.009206 | -41.68 | 6.302e-32 | 9.379e-55 | 1.26e-31 | 22 | GOOD (significant) |
| medium | M4ab | client-drift E_drift | 450 | 0.01319 | 0.02203 | -0.008839 | -40.12 | 3.757e-37 | 4.694e-59 | 2.254e-36 | 19 | GOOD (significant) |
| small | M4ab | client-drift E_drift | 450 | 0.01225 | 0.02526 | -0.01301 | -51.49 | 1.881e-26 | 1.213e-59 | 2.655e-26 | 28 | GOOD (significant) |
| large | M4ab | drift alignment S_CDA | 450 | 0.3121 | 0.2435 | 0.06858 | 28.16 | 1.187e-69 | 4.781e-60 | 2.036e-69 | 8 | GOOD (significant) |
| medium | M4ab | drift alignment S_CDA | 450 | 0.3258 | 0.2483 | 0.07746 | 31.2 | 1.064e-76 | 7.186e-68 | 2.321e-76 | 7 | GOOD (significant) |
| small | M4ab | drift alignment S_CDA | 450 | 0.351 | 0.2779 | 0.07301 | 26.27 | 2.007e-64 | 3.787e-63 | 2.676e-64 | 9 | GOOD (significant) |
| large | M5b | accuracy | 450 | 0.3754 | 0.3598 | 0.01562 | 4.34 | 2.812e-13 | 2.002e-12 | 6.748e-12 | 63 | GOOD (significant) |
| medium | M5b | accuracy | 450 | 0.4066 | 0.3948 | 0.01186 | 3.005 | 2.231e-07 | 3.08e-08 | 1.785e-06 | 128 | GOOD (significant) |
| small | M5b | accuracy | 450 | 0.3996 | 0.384 | 0.01567 | 4.08 | 7.796e-11 | 3.702e-11 | 9.355e-10 | 80 | GOOD (significant) |
| large | M5b | client-drift E_drift | 450 | 0.01288 | 0.0188 | -0.005919 | -31.48 | 2.754e-26 | 4.516e-44 | 3.672e-26 | 28 | GOOD (significant) |
| medium | M5b | client-drift E_drift | 450 | 0.01319 | 0.01843 | -0.005234 | -28.41 | 1.094e-23 | 4.513e-42 | 1.193e-23 | 32 | GOOD (significant) |
| small | M5b | client-drift E_drift | 450 | 0.01225 | 0.0197 | -0.007448 | -37.81 | 2.204e-33 | 5.149e-56 | 5.29e-33 | 21 | GOOD (significant) |
| large | M5b | drift alignment S_CDA | 450 | 0.3121 | 0.3164 | -0.004312 | -1.363 | 0.1023 | 0.004014 | 0.1023 | 1318 | bad trend (n.s.) |
| medium | M5b | drift alignment S_CDA | 450 | 0.3258 | 0.3202 | 0.005545 | 1.732 | 0.0212 | 0.2474 | 0.02212 | 661 | GOOD (significant) |
| small | M5b | drift alignment S_CDA | 450 | 0.351 | 0.3408 | 0.0102 | 2.995 | 0.000221 | 0.008412 | 0.0002411 | 255 | GOOD (significant) |
| large | M3 | accuracy | 450 | 0.3754 | 0.3694 | 0.006035 | 1.634 | 0.0165 | 0.01283 | 0.02829 | 610 | GOOD (significant) |
| medium | M3 | accuracy | 450 | 0.4066 | 0.3999 | 0.006681 | 1.671 | 0.002852 | 0.0009559 | 0.01204 | 393 | GOOD (significant) |
| small | M3 | accuracy | 450 | 0.3996 | 0.3927 | 0.00698 | 1.778 | 0.01388 | 0.0007111 | 0.02776 | 579 | GOOD (significant) |
| large | M3 | client-drift E_drift | 450 | 0.01288 | 0.02051 | -0.007624 | -37.18 | 6.584e-30 | 1.163e-54 | 1.216e-29 | 24 | GOOD (significant) |
| medium | M3 | client-drift E_drift | 450 | 0.01319 | 0.02036 | -0.007166 | -35.2 | 1.95e-35 | 1.134e-56 | 7.8e-35 | 20 | GOOD (significant) |
| small | M3 | client-drift E_drift | 450 | 0.01225 | 0.02361 | -0.01136 | -48.1 | 2.594e-23 | 1.592e-57 | 2.594e-23 | 32 | GOOD (significant) |
| large | M3 | drift alignment S_CDA | 450 | 0.3121 | 0.2412 | 0.07087 | 29.38 | 1.794e-78 | 1.363e-64 | 4.305e-78 | 7 | GOOD (significant) |
| medium | M3 | drift alignment S_CDA | 450 | 0.3258 | 0.2508 | 0.07497 | 29.9 | 2.041e-80 | 1.352e-67 | 8.165e-80 | 7 | GOOD (significant) |
| small | M3 | drift alignment S_CDA | 450 | 0.351 | 0.2815 | 0.06945 | 24.67 | 3.1e-64 | 7.482e-61 | 3.916e-64 | 9 | GOOD (significant) |
| large | M2 | accuracy | 450 | 0.3754 | 0.3745 | 0.0009642 | 0.2575 | 0.6875 | 0.535 | 0.7348 | 2.18e+04 | good trend (n.s.) |
| medium | M2 | accuracy | 450 | 0.4066 | 0.3992 | 0.007433 | 1.862 | 0.001162 | 0.0005438 | 0.006973 | 331 | GOOD (significant) |
| small | M2 | accuracy | 450 | 0.3996 | 0.3963 | 0.003377 | 0.8521 | 0.2186 | 0.004673 | 0.2786 | 2327 | good trend (n.s.) |
| large | M2 | client-drift E_drift | 450 | 0.01288 | 0.02025 | -0.007372 | -36.4 | 1.222e-29 | 1.601e-57 | 2.095e-29 | 24 | GOOD (significant) |
| medium | M2 | client-drift E_drift | 450 | 0.01319 | 0.02052 | -0.007333 | -35.73 | 2.623e-36 | 1.374e-59 | 1.259e-35 | 19 | GOOD (significant) |
| small | M2 | client-drift E_drift | 450 | 0.01225 | 0.02371 | -0.01146 | -48.32 | 1.251e-24 | 6.101e-62 | 1.43e-24 | 30 | GOOD (significant) |
| large | M2 | drift alignment S_CDA | 450 | 0.3121 | 0.2477 | 0.06439 | 26 | 1.054e-78 | 2.016e-62 | 3.162e-78 | 7 | GOOD (significant) |
| medium | M2 | drift alignment S_CDA | 450 | 0.3258 | 0.2567 | 0.06907 | 26.91 | 3.61e-81 | 1.726e-66 | 1.733e-80 | 7 | GOOD (significant) |
| small | M2 | drift alignment S_CDA | 450 | 0.351 | 0.2834 | 0.0676 | 23.86 | 6.055e-71 | 1.256e-62 | 1.118e-70 | 8 | GOOD (significant) |
| large | CDQ | accuracy | 450 | 0.3754 | 0.3685 | 0.006881 | 1.867 | 0.00301 | 5.572e-05 | 0.01204 | 397 | GOOD (significant) |
| medium | CDQ | accuracy | 450 | 0.4066 | 0.4025 | 0.004126 | 1.025 | 0.1079 | 0.2377 | 0.1618 | 1362 | good trend (n.s.) |
| small | CDQ | accuracy | 450 | 0.3996 | 0.3974 | 0.002279 | 0.5735 | 0.3577 | 0.65 | 0.4292 | 4166 | good trend (n.s.) |
| large | CDQ | client-drift E_drift | 450 | 0.01288 | 0.02835 | -0.01547 | -54.56 | 3.085e-32 | 4.096e-60 | 6.732e-32 | 22 | GOOD (significant) |
| medium | CDQ | client-drift E_drift | 450 | 0.01319 | 0.02972 | -0.01653 | -55.62 | 6.611e-40 | 1.436e-71 | 1.587e-38 | 17 | GOOD (significant) |
| small | CDQ | client-drift E_drift | 450 | 0.01225 | 0.03411 | -0.02186 | -64.08 | 8.604e-39 | 1.98e-74 | 1.032e-37 | 18 | GOOD (significant) |
| large | CDQ | drift alignment S_CDA | 450 | 0.3121 | 0.2839 | 0.02817 | 9.923 | 5.04e-33 | 1.379e-30 | 5.761e-33 | 21 | GOOD (significant) |
| medium | CDQ | drift alignment S_CDA | 450 | 0.3258 | 0.2879 | 0.03787 | 13.16 | 2.639e-57 | 8.567e-48 | 3.167e-57 | 11 | GOOD (significant) |
| small | CDQ | drift alignment S_CDA | 450 | 0.351 | 0.2989 | 0.05211 | 17.44 | 1.709e-82 | 9.075e-59 | 1.368e-81 | 7 | GOOD (significant) |

## table6 paired by channel

Paired comparison by channel quality.

| scale | channel | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | good | base | accuracy | 150 | 0.3847 | 0.3664 | 0.01831 | 4.997 | 7.978e-06 | 1.271e-05 | 0.0001077 | 55 | GOOD (significant) |
| large | moderate | base | accuracy | 150 | 0.3794 | 0.3706 | 0.008878 | 2.396 | 0.02609 | 0.04293 | 0.06404 | 234 | good trend (n.s.) |
| large | poor | base | accuracy | 150 | 0.3622 | 0.37 | -0.007848 | -2.121 | 0.1162 | 0.1782 | 0.1743 | 472 | bad trend (n.s.) |
| medium | good | base | accuracy | 150 | 0.415 | 0.4143 | 0.0006963 | 0.1681 | 0.822 | 0.6445 | 0.8537 | 2.319e+04 | good trend (n.s.) |
| medium | moderate | base | accuracy | 150 | 0.4074 | 0.3941 | 0.01331 | 3.377 | 0.0008707 | 7.918e-05 | 0.004702 | 102 | GOOD (significant) |
| medium | poor | base | accuracy | 150 | 0.3974 | 0.3921 | 0.005341 | 1.362 | 0.2312 | 0.3021 | 0.2973 | 815 | good trend (n.s.) |
| small | good | base | accuracy | 150 | 0.4151 | 0.3935 | 0.02165 | 5.502 | 1.905e-07 | 2.226e-07 | 5.143e-06 | 40 | GOOD (significant) |
| small | moderate | base | accuracy | 150 | 0.4094 | 0.3962 | 0.01324 | 3.342 | 0.00137 | 0.0004359 | 0.006166 | 111 | GOOD (significant) |
| small | poor | base | accuracy | 150 | 0.3744 | 0.3882 | -0.01384 | -3.564 | 0.02131 | 0.05698 | 0.06041 | 218 | bad trend (n.s.) |
| large | good | base | client-drift E_drift | 150 | 0.002655 | 0.005884 | -0.003229 | -54.87 | 5.479e-21 | 2.394e-26 | 1.644e-20 | 10 | GOOD (significant) |
| large | moderate | base | client-drift E_drift | 150 | 0.006964 | 0.01088 | -0.003912 | -35.97 | 1.235e-16 | 8.091e-20 | 1.45e-16 | 14 | GOOD (significant) |
| large | poor | base | client-drift E_drift | 150 | 0.02902 | 0.04531 | -0.01628 | -35.94 | 2.621e-17 | 1.849e-19 | 3.872e-17 | 13 | GOOD (significant) |
| medium | good | base | client-drift E_drift | 150 | 0.002627 | 0.005578 | -0.002951 | -52.9 | 7.364e-19 | 4.197e-26 | 1.326e-18 | 12 | GOOD (significant) |
| medium | moderate | base | client-drift E_drift | 150 | 0.00692 | 0.01133 | -0.004413 | -38.94 | 8.363e-17 | 1.195e-21 | 1.026e-16 | 14 | GOOD (significant) |
| medium | poor | base | client-drift E_drift | 150 | 0.03003 | 0.04455 | -0.01452 | -32.59 | 3.212e-20 | 1.557e-19 | 7.883e-20 | 11 | GOOD (significant) |
| small | good | base | client-drift E_drift | 150 | 0.003143 | 0.005981 | -0.002838 | -47.45 | 6.089e-12 | 4.323e-23 | 6.85e-12 | 22 | GOOD (significant) |
| small | moderate | base | client-drift E_drift | 150 | 0.007615 | 0.01234 | -0.004726 | -38.29 | 2.263e-11 | 1.557e-17 | 2.263e-11 | 23 | GOOD (significant) |
| small | poor | base | client-drift E_drift | 150 | 0.026 | 0.05308 | -0.02708 | -51.02 | 1.906e-17 | 6.638e-24 | 3.216e-17 | 13 | GOOD (significant) |
| large | good | base | drift alignment S_CDA | 150 | 0.4254 | 0.3351 | 0.09026 | 26.94 | 4.789e-32 | 3.298e-25 | 4.31e-31 | 6 | GOOD (significant) |
| large | moderate | base | drift alignment S_CDA | 150 | 0.3141 | 0.2422 | 0.07189 | 29.69 | 5.484e-27 | 5.077e-22 | 1.139e-26 | 7 | GOOD (significant) |
| large | poor | base | drift alignment S_CDA | 150 | 0.1968 | 0.1428 | 0.05407 | 37.88 | 8.63e-27 | 2.308e-20 | 1.664e-26 | 7 | GOOD (significant) |
| medium | good | base | drift alignment S_CDA | 150 | 0.443 | 0.3499 | 0.09317 | 26.63 | 7.85e-30 | 1.107e-24 | 3.533e-29 | 6 | GOOD (significant) |
| medium | moderate | base | drift alignment S_CDA | 150 | 0.3284 | 0.2461 | 0.08233 | 33.45 | 2.27e-32 | 1.268e-24 | 4.31e-31 | 6 | GOOD (significant) |
| medium | poor | base | drift alignment S_CDA | 150 | 0.2058 | 0.1544 | 0.05137 | 33.27 | 6.615e-28 | 9.266e-22 | 1.786e-27 | 7 | GOOD (significant) |
| small | good | base | drift alignment S_CDA | 150 | 0.4862 | 0.397 | 0.08917 | 22.46 | 8.228e-24 | 8.506e-24 | 1.169e-23 | 9 | GOOD (significant) |
| small | moderate | base | drift alignment S_CDA | 150 | 0.3545 | 0.29 | 0.06451 | 22.24 | 9.868e-21 | 8.975e-20 | 1.269e-20 | 10 | GOOD (significant) |
| small | poor | base | drift alignment S_CDA | 150 | 0.2122 | 0.1558 | 0.0564 | 36.2 | 1.06e-28 | 1.337e-20 | 3.576e-28 | 7 | GOOD (significant) |
| large | good | JEQFL | accuracy | 150 | 0.3847 | 0.3708 | 0.01382 | 3.727 | 0.0001325 | 9.427e-05 | 0.001192 | 77 | GOOD (significant) |
| large | moderate | JEQFL | accuracy | 150 | 0.3794 | 0.3682 | 0.01125 | 3.055 | 0.006418 | 0.007623 | 0.02166 | 155 | GOOD (significant) |
| large | poor | JEQFL | accuracy | 150 | 0.3622 | 0.3712 | -0.009004 | -2.426 | 0.07361 | 0.2732 | 0.1246 | 363 | bad trend (n.s.) |
| medium | good | JEQFL | accuracy | 150 | 0.415 | 0.4076 | 0.007459 | 1.83 | 0.03758 | 0.01358 | 0.0836 | 268 | good trend (n.s.) |
| medium | moderate | JEQFL | accuracy | 150 | 0.4074 | 0.4042 | 0.003256 | 0.8055 | 0.4275 | 0.06328 | 0.5018 | 1860 | good trend (n.s.) |
| medium | poor | JEQFL | accuracy | 150 | 0.3974 | 0.3892 | 0.008244 | 2.118 | 0.08262 | 0.1297 | 0.1312 | 386 | good trend (n.s.) |
| small | good | JEQFL | accuracy | 150 | 0.4151 | 0.4019 | 0.01325 | 3.297 | 0.0005703 | 0.0006629 | 0.00385 | 95 | GOOD (significant) |
| small | moderate | JEQFL | accuracy | 150 | 0.4094 | 0.4037 | 0.00573 | 1.419 | 0.1754 | 0.05708 | 0.2493 | 636 | good trend (n.s.) |
| small | poor | JEQFL | accuracy | 150 | 0.3744 | 0.3927 | -0.01829 | -4.657 | 0.005105 | 0.007737 | 0.01969 | 146 | BAD (significant) |
| large | good | JEQFL | client-drift E_drift | 150 | 0.002655 | 0.005545 | -0.00289 | -52.12 | 3.913e-19 | 7.052e-26 | 8.127e-19 | 12 | GOOD (significant) |
| large | moderate | JEQFL | client-drift E_drift | 150 | 0.006964 | 0.01092 | -0.003953 | -36.21 | 2.868e-17 | 1.182e-20 | 3.872e-17 | 13 | GOOD (significant) |
| large | poor | JEQFL | client-drift E_drift | 150 | 0.02902 | 0.04498 | -0.01596 | -35.48 | 2.767e-17 | 2.101e-18 | 3.872e-17 | 13 | GOOD (significant) |
| medium | good | JEQFL | client-drift E_drift | 150 | 0.002627 | 0.005294 | -0.002667 | -50.38 | 3.786e-17 | 1.385e-25 | 4.868e-17 | 13 | GOOD (significant) |
| medium | moderate | JEQFL | client-drift E_drift | 150 | 0.00692 | 0.01153 | -0.004611 | -39.99 | 2.339e-17 | 2.221e-22 | 3.715e-17 | 13 | GOOD (significant) |
| medium | poor | JEQFL | client-drift E_drift | 150 | 0.03003 | 0.04505 | -0.01502 | -33.34 | 2.356e-20 | 6.349e-20 | 6.36e-20 | 11 | GOOD (significant) |
| small | good | JEQFL | client-drift E_drift | 150 | 0.003143 | 0.005654 | -0.002511 | -44.42 | 1.528e-11 | 1.567e-21 | 1.587e-11 | 23 | GOOD (significant) |
| small | moderate | JEQFL | client-drift E_drift | 150 | 0.007615 | 0.01272 | -0.005105 | -40.14 | 1.093e-11 | 2.172e-18 | 1.181e-11 | 22 | GOOD (significant) |
| small | poor | JEQFL | client-drift E_drift | 150 | 0.026 | 0.05341 | -0.02741 | -51.32 | 2.568e-19 | 8.937e-25 | 5.778e-19 | 11 | GOOD (significant) |
| large | good | JEQFL | drift alignment S_CDA | 150 | 0.4254 | 0.3413 | 0.08404 | 24.62 | 1.37e-27 | 1.175e-23 | 3.082e-27 | 7 | GOOD (significant) |
| large | moderate | JEQFL | drift alignment S_CDA | 150 | 0.3141 | 0.2526 | 0.06149 | 24.35 | 8.861e-19 | 4.612e-16 | 9.968e-19 | 12 | GOOD (significant) |
| large | poor | JEQFL | drift alignment S_CDA | 150 | 0.1968 | 0.1421 | 0.05471 | 38.49 | 4.858e-28 | 1.878e-21 | 1.457e-27 | 7 | GOOD (significant) |
| medium | good | JEQFL | drift alignment S_CDA | 150 | 0.443 | 0.3474 | 0.09568 | 27.54 | 2.237e-31 | 9.475e-25 | 1.221e-30 | 6 | GOOD (significant) |
| medium | moderate | JEQFL | drift alignment S_CDA | 150 | 0.3284 | 0.2505 | 0.07796 | 31.13 | 2.798e-29 | 8.012e-23 | 1.079e-28 | 6 | GOOD (significant) |
| medium | poor | JEQFL | drift alignment S_CDA | 150 | 0.2058 | 0.1549 | 0.05092 | 32.88 | 1.701e-25 | 2.564e-20 | 2.702e-25 | 8 | GOOD (significant) |
| small | good | JEQFL | drift alignment S_CDA | 150 | 0.4862 | 0.4027 | 0.08349 | 20.73 | 4.128e-23 | 5.725e-23 | 5.572e-23 | 9 | GOOD (significant) |
| small | moderate | JEQFL | drift alignment S_CDA | 150 | 0.3545 | 0.2817 | 0.07284 | 25.86 | 4.414e-26 | 1.059e-22 | 7.449e-26 | 8 | GOOD (significant) |
| small | poor | JEQFL | drift alignment S_CDA | 150 | 0.2122 | 0.1534 | 0.05881 | 38.34 | 2.26e-31 | 3.399e-21 | 1.221e-30 | 6 | GOOD (significant) |
| large | good | CDQ | accuracy | 150 | 0.3847 | 0.3819 | 0.002756 | 0.7215 | 0.2233 | 0.6492 | 0.2973 | 788 | good trend (n.s.) |
| large | moderate | CDQ | accuracy | 150 | 0.3794 | 0.3725 | 0.006911 | 1.855 | 0.04025 | 0.0009984 | 0.0836 | 275 | good trend (n.s.) |
| large | poor | CDQ | accuracy | 150 | 0.3622 | 0.3512 | 0.01098 | 3.126 | 0.0529 | 0.01027 | 0.102 | 310 | good trend (n.s.) |
| medium | good | CDQ | accuracy | 150 | 0.415 | 0.4135 | 0.001489 | 0.36 | 0.596 | 0.9038 | 0.6436 | 4171 | good trend (n.s.) |
| medium | moderate | CDQ | accuracy | 150 | 0.4074 | 0.4102 | -0.002733 | -0.6664 | 0.4907 | 0.2324 | 0.552 | 2466 | bad trend (n.s.) |
| medium | poor | CDQ | accuracy | 150 | 0.3974 | 0.3838 | 0.01362 | 3.549 | 0.02237 | 0.01283 | 0.06041 | 222 | good trend (n.s.) |
| small | good | CDQ | accuracy | 150 | 0.4151 | 0.4184 | -0.003293 | -0.7869 | 0.3438 | 0.2588 | 0.4219 | 1306 | bad trend (n.s.) |
| small | moderate | CDQ | accuracy | 150 | 0.4094 | 0.4094 | 4.074e-05 | 0.009951 | 0.9904 | 0.8008 | 0.9904 | 8.022e+06 | good trend (n.s.) |
| small | poor | CDQ | accuracy | 150 | 0.3744 | 0.3643 | 0.01009 | 2.77 | 0.07382 | 0.1305 | 0.1246 | 364 | good trend (n.s.) |
| large | good | CDQ | client-drift E_drift | 150 | 0.002655 | 0.003296 | -0.0006406 | -19.44 | 4.247e-19 | 5.813e-17 | 8.191e-19 | 12 | GOOD (significant) |
| large | moderate | CDQ | client-drift E_drift | 150 | 0.006964 | 0.01016 | -0.003196 | -31.46 | 6.896e-25 | 3.034e-19 | 2.327e-24 | 8 | GOOD (significant) |
| large | poor | CDQ | client-drift E_drift | 150 | 0.02902 | 0.07159 | -0.04257 | -59.46 | 8.515e-39 | 5.334e-26 | 4.598e-38 | 4 | GOOD (significant) |
| medium | good | CDQ | client-drift E_drift | 150 | 0.002627 | 0.003454 | -0.0008276 | -23.96 | 8.109e-35 | 1.476e-23 | 3.128e-34 | 5 | GOOD (significant) |
| medium | moderate | CDQ | client-drift E_drift | 150 | 0.00692 | 0.01141 | -0.004488 | -39.34 | 2.846e-51 | 1.655e-25 | 3.842e-50 | 3 | GOOD (significant) |
| medium | poor | CDQ | client-drift E_drift | 150 | 0.03003 | 0.07431 | -0.04428 | -59.59 | 7.358e-51 | 2.701e-26 | 6.622e-50 | 3 | GOOD (significant) |
| small | good | CDQ | client-drift E_drift | 150 | 0.003143 | 0.004159 | -0.001016 | -24.43 | 3.199e-35 | 4.441e-24 | 1.44e-34 | 5 | GOOD (significant) |
| small | moderate | CDQ | client-drift E_drift | 150 | 0.007615 | 0.01291 | -0.005299 | -41.04 | 6.242e-53 | 2.492e-26 | 1.685e-51 | 3 | GOOD (significant) |
| small | poor | CDQ | client-drift E_drift | 150 | 0.026 | 0.08527 | -0.05927 | -69.51 | 1.427e-50 | 2.3e-26 | 9.632e-50 | 3 | GOOD (significant) |
| large | good | CDQ | drift alignment S_CDA | 150 | 0.4254 | 0.4004 | 0.02492 | 6.224 | 1.899e-11 | 3.173e-10 | 1.972e-11 | 23 | GOOD (significant) |
| large | moderate | CDQ | drift alignment S_CDA | 150 | 0.3141 | 0.289 | 0.02502 | 8.657 | 4.884e-08 | 6.103e-08 | 4.884e-08 | 36 | GOOD (significant) |
| large | poor | CDQ | drift alignment S_CDA | 150 | 0.1968 | 0.1623 | 0.03457 | 21.3 | 4.97e-19 | 1.263e-16 | 5.971e-19 | 12 | GOOD (significant) |
| medium | good | CDQ | drift alignment S_CDA | 150 | 0.443 | 0.4113 | 0.03172 | 7.713 | 5.086e-19 | 3.771e-16 | 5.971e-19 | 12 | GOOD (significant) |
| medium | moderate | CDQ | drift alignment S_CDA | 150 | 0.3284 | 0.2839 | 0.04452 | 15.68 | 7.584e-25 | 4.563e-20 | 1.138e-24 | 8 | GOOD (significant) |
| medium | poor | CDQ | drift alignment S_CDA | 150 | 0.2058 | 0.1684 | 0.03738 | 22.19 | 1.719e-17 | 4.717e-15 | 1.856e-17 | 13 | GOOD (significant) |
| small | good | CDQ | drift alignment S_CDA | 150 | 0.4862 | 0.437 | 0.04916 | 11.25 | 1.26e-27 | 2.702e-20 | 3.082e-27 | 7 | GOOD (significant) |
| small | moderate | CDQ | drift alignment S_CDA | 150 | 0.3545 | 0.2939 | 0.0606 | 20.62 | 4.626e-32 | 7.314e-22 | 4.31e-31 | 6 | GOOD (significant) |
| small | poor | CDQ | drift alignment S_CDA | 150 | 0.2122 | 0.1656 | 0.04657 | 28.12 | 1.668e-26 | 4.563e-20 | 3.002e-26 | 7 | GOOD (significant) |

## table7 paired by alpha

Paired comparison by alpha.

| scale | alpha | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | 25 | base | accuracy | 150 | 0.3712 | 0.3642 | 0.006993 | 1.92 | 0.1106 | 0.04609 | 0.2014 | 457 | good trend (n.s.) |
| large | 50 | base | accuracy | 150 | 0.3758 | 0.3688 | 0.007059 | 1.914 | 0.1119 | 0.2583 | 0.2014 | 461 | good trend (n.s.) |
| large | 100 | base | accuracy | 150 | 0.3793 | 0.374 | 0.005285 | 1.413 | 0.2369 | 0.1894 | 0.328 | 835 | good trend (n.s.) |
| medium | 25 | base | accuracy | 150 | 0.4107 | 0.4008 | 0.009837 | 2.454 | 0.01992 | 0.01568 | 0.09061 | 213 | good trend (n.s.) |
| medium | 50 | base | accuracy | 150 | 0.4036 | 0.403 | 0.0005889 | 0.1461 | 0.8641 | 0.5272 | 0.9149 | 4.004e+04 | good trend (n.s.) |
| medium | 100 | base | accuracy | 150 | 0.4056 | 0.3967 | 0.008922 | 2.249 | 0.02517 | 0.02057 | 0.09061 | 231 | good trend (n.s.) |
| small | 25 | base | accuracy | 150 | 0.4007 | 0.3877 | 0.01302 | 3.359 | 0.01943 | 0.01021 | 0.09061 | 211 | good trend (n.s.) |
| small | 50 | base | accuracy | 150 | 0.3986 | 0.3927 | 0.005915 | 1.506 | 0.2069 | 0.03229 | 0.3105 | 733 | good trend (n.s.) |
| small | 100 | base | accuracy | 150 | 0.3997 | 0.3975 | 0.002115 | 0.532 | 0.6334 | 0.3239 | 0.7601 | 5156 | good trend (n.s.) |
| large | 25 | base | client-drift E_drift | 150 | 0.01356 | 0.02293 | -0.009366 | -40.85 | 6.296e-13 | 1.268e-20 | 3.777e-12 | 19 | GOOD (significant) |
| large | 50 | base | client-drift E_drift | 150 | 0.01311 | 0.01998 | -0.006863 | -34.36 | 4.564e-10 | 1.64e-19 | 8.215e-10 | 27 | GOOD (significant) |
| large | 100 | base | client-drift E_drift | 150 | 0.01197 | 0.01916 | -0.007193 | -37.54 | 6.429e-09 | 5.978e-19 | 7.715e-09 | 32 | GOOD (significant) |
| medium | 25 | base | client-drift E_drift | 150 | 0.01387 | 0.02259 | -0.008727 | -38.62 | 5.844e-14 | 2.84e-21 | 5.26e-13 | 18 | GOOD (significant) |
| medium | 50 | base | client-drift E_drift | 150 | 0.01349 | 0.02022 | -0.006725 | -33.26 | 2.798e-12 | 1.104e-19 | 1.007e-11 | 21 | GOOD (significant) |
| medium | 100 | base | client-drift E_drift | 150 | 0.01222 | 0.01865 | -0.006433 | -34.5 | 1.214e-11 | 4.718e-19 | 3.122e-11 | 22 | GOOD (significant) |
| small | 25 | base | client-drift E_drift | 150 | 0.01338 | 0.02566 | -0.01228 | -47.86 | 9.522e-10 | 5.117e-23 | 1.558e-09 | 28 | GOOD (significant) |
| small | 50 | base | client-drift E_drift | 150 | 0.01222 | 0.02351 | -0.01129 | -48.01 | 2.196e-08 | 1.203e-19 | 2.325e-08 | 34 | GOOD (significant) |
| small | 100 | base | client-drift E_drift | 150 | 0.01116 | 0.02223 | -0.01108 | -49.82 | 4.472e-08 | 2.137e-18 | 4.472e-08 | 36 | GOOD (significant) |
| large | 25 | base | drift alignment S_CDA | 150 | 0.3084 | 0.2269 | 0.08152 | 35.94 | 1.023e-35 | 7.636e-26 | 1.841e-34 | 5 | GOOD (significant) |
| large | 50 | base | drift alignment S_CDA | 150 | 0.31 | 0.2468 | 0.06315 | 25.59 | 1.268e-21 | 1.163e-19 | 1.426e-21 | 10 | GOOD (significant) |
| large | 100 | base | drift alignment S_CDA | 150 | 0.3179 | 0.2464 | 0.07156 | 29.05 | 6.112e-27 | 1.952e-22 | 1.375e-26 | 7 | GOOD (significant) |
| medium | 25 | base | drift alignment S_CDA | 150 | 0.327 | 0.2413 | 0.08576 | 35.54 | 3.82e-33 | 2.056e-25 | 3.438e-32 | 5 | GOOD (significant) |
| medium | 50 | base | drift alignment S_CDA | 150 | 0.3241 | 0.2527 | 0.07136 | 28.24 | 3.561e-27 | 4.615e-24 | 9.156e-27 | 7 | GOOD (significant) |
| medium | 100 | base | drift alignment S_CDA | 150 | 0.3261 | 0.2564 | 0.06975 | 27.21 | 1.346e-24 | 9.786e-22 | 2.422e-24 | 8 | GOOD (significant) |
| small | 25 | base | drift alignment S_CDA | 150 | 0.3452 | 0.2709 | 0.07438 | 27.46 | 9.409e-26 | 8.012e-23 | 1.882e-25 | 8 | GOOD (significant) |
| small | 50 | base | drift alignment S_CDA | 150 | 0.3521 | 0.2854 | 0.06675 | 23.39 | 4.553e-20 | 2.433e-20 | 4.821e-20 | 11 | GOOD (significant) |
| small | 100 | base | drift alignment S_CDA | 150 | 0.3555 | 0.2866 | 0.06894 | 24.06 | 5.615e-22 | 2.84e-21 | 6.738e-22 | 10 | GOOD (significant) |
| large | 25 | JEQFL | accuracy | 150 | 0.3712 | 0.3678 | 0.0034 | 0.9245 | 0.4621 | 0.06729 | 0.5941 | 2166 | good trend (n.s.) |
| large | 50 | JEQFL | accuracy | 150 | 0.3758 | 0.3684 | 0.007415 | 2.013 | 0.07871 | 0.05973 | 0.1771 | 376 | good trend (n.s.) |
| large | 100 | JEQFL | accuracy | 150 | 0.3793 | 0.374 | 0.005252 | 1.404 | 0.207 | 0.1714 | 0.3105 | 733 | good trend (n.s.) |
| medium | 25 | JEQFL | accuracy | 150 | 0.4107 | 0.4009 | 0.009733 | 2.428 | 0.03176 | 0.01863 | 0.09529 | 251 | good trend (n.s.) |
| medium | 50 | JEQFL | accuracy | 150 | 0.4036 | 0.4037 | -0.0001 | -0.02477 | 0.9803 | 0.8005 | 0.9803 | 1.934e+06 | bad trend (n.s.) |
| medium | 100 | JEQFL | accuracy | 150 | 0.4056 | 0.3963 | 0.009326 | 2.353 | 0.0163 | 0.002666 | 0.09061 | 200 | good trend (n.s.) |
| small | 25 | JEQFL | accuracy | 150 | 0.4007 | 0.3894 | 0.01126 | 2.89 | 0.0248 | 0.01026 | 0.09061 | 229 | good trend (n.s.) |
| small | 50 | JEQFL | accuracy | 150 | 0.3986 | 0.4005 | -0.001911 | -0.4772 | 0.7191 | 0.6798 | 0.809 | 9068 | bad trend (n.s.) |
| small | 100 | JEQFL | accuracy | 150 | 0.3997 | 0.4083 | -0.008652 | -2.119 | 0.07167 | 0.1346 | 0.1771 | 358 | bad trend (n.s.) |
| large | 25 | JEQFL | client-drift E_drift | 150 | 0.01356 | 0.02242 | -0.008858 | -39.51 | 2.029e-12 | 8.146e-21 | 9.132e-12 | 20 | GOOD (significant) |
| large | 50 | JEQFL | client-drift E_drift | 150 | 0.01311 | 0.01979 | -0.006676 | -33.74 | 1.732e-09 | 1.557e-17 | 2.593e-09 | 29 | GOOD (significant) |
| large | 100 | JEQFL | client-drift E_drift | 150 | 0.01197 | 0.01924 | -0.00727 | -37.79 | 1.873e-09 | 3.982e-19 | 2.593e-09 | 29 | GOOD (significant) |
| medium | 25 | JEQFL | client-drift E_drift | 150 | 0.01387 | 0.02307 | -0.009204 | -39.89 | 3.61e-14 | 1.04e-22 | 5.26e-13 | 17 | GOOD (significant) |
| medium | 50 | JEQFL | client-drift E_drift | 150 | 0.01349 | 0.01997 | -0.006481 | -32.45 | 3.217e-11 | 9.955e-20 | 7.239e-11 | 23 | GOOD (significant) |
| medium | 100 | JEQFL | client-drift E_drift | 150 | 0.01222 | 0.01883 | -0.006611 | -35.11 | 7.694e-12 | 9.785e-20 | 2.308e-11 | 22 | GOOD (significant) |
| small | 25 | JEQFL | client-drift E_drift | 150 | 0.01338 | 0.02573 | -0.01235 | -48.01 | 4.357e-10 | 5.943e-23 | 8.215e-10 | 27 | GOOD (significant) |
| small | 50 | JEQFL | client-drift E_drift | 150 | 0.01222 | 0.02382 | -0.0116 | -48.68 | 8.288e-09 | 4.256e-20 | 9.323e-09 | 32 | GOOD (significant) |
| small | 100 | JEQFL | client-drift E_drift | 150 | 0.01116 | 0.02224 | -0.01108 | -49.83 | 2.858e-09 | 1.405e-19 | 3.675e-09 | 30 | GOOD (significant) |
| large | 25 | JEQFL | drift alignment S_CDA | 150 | 0.3084 | 0.2324 | 0.07595 | 32.68 | 6.403e-32 | 3.638e-25 | 2.881e-31 | 6 | GOOD (significant) |
| large | 50 | JEQFL | drift alignment S_CDA | 150 | 0.31 | 0.2529 | 0.05702 | 22.54 | 1.457e-17 | 3.179e-16 | 1.457e-17 | 13 | GOOD (significant) |
| large | 100 | JEQFL | drift alignment S_CDA | 150 | 0.3179 | 0.2506 | 0.06727 | 26.84 | 1.558e-22 | 1.224e-19 | 2.11e-22 | 9 | GOOD (significant) |
| medium | 25 | JEQFL | drift alignment S_CDA | 150 | 0.327 | 0.2437 | 0.08338 | 34.22 | 6.244e-32 | 1.452e-24 | 2.881e-31 | 6 | GOOD (significant) |
| medium | 50 | JEQFL | drift alignment S_CDA | 150 | 0.3241 | 0.2515 | 0.07253 | 28.83 | 4.691e-28 | 1.198e-23 | 1.689e-27 | 7 | GOOD (significant) |
| medium | 100 | JEQFL | drift alignment S_CDA | 150 | 0.3261 | 0.2575 | 0.06864 | 26.66 | 1.641e-22 | 8.821e-20 | 2.11e-22 | 9 | GOOD (significant) |
| small | 25 | JEQFL | drift alignment S_CDA | 150 | 0.3452 | 0.2688 | 0.07639 | 28.41 | 1.035e-27 | 2.348e-22 | 3.106e-27 | 7 | GOOD (significant) |
| small | 50 | JEQFL | drift alignment S_CDA | 150 | 0.3521 | 0.2835 | 0.06861 | 24.2 | 2.154e-23 | 1.373e-22 | 3.231e-23 | 9 | GOOD (significant) |
| small | 100 | JEQFL | drift alignment S_CDA | 150 | 0.3555 | 0.2854 | 0.07014 | 24.58 | 1.185e-23 | 3.392e-22 | 1.939e-23 | 9 | GOOD (significant) |

## table8 paired by arm

Paired comparison by experimental arm.

| scale | arm | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | A0_A3 | base | accuracy | 90 | 0.3761 | 0.3644 | 0.01169 | 3.208 | 0.06294 | 0.0416 | 0.1888 | 200 | good trend (n.s.) |
| large | A1 | base | accuracy | 90 | 0.3768 | 0.3835 | -0.006679 | -1.742 | 0.2282 | 0.3251 | 0.428 | 480 | bad trend (n.s.) |
| large | A2 | base | accuracy | 90 | 0.3818 | 0.3823 | -0.0004383 | -0.1147 | 0.9333 | 0.8092 | 0.9333 | 1.001e+05 | bad trend (n.s.) |
| large | A3 | base | accuracy | 90 | 0.3745 | 0.3594 | 0.01517 | 4.222 | 0.02482 | 0.05495 | 0.1377 | 136 | good trend (n.s.) |
| large | A3adv | base | accuracy | 90 | 0.3679 | 0.3554 | 0.01248 | 3.512 | 0.004482 | 0.01411 | 0.04838 | 84 | GOOD (significant) |
| medium | A0_A3 | base | accuracy | 90 | 0.4139 | 0.4055 | 0.008475 | 2.09 | 0.1263 | 0.1414 | 0.2841 | 297 | good trend (n.s.) |
| medium | A1 | base | accuracy | 90 | 0.4129 | 0.408 | 0.004864 | 1.192 | 0.3709 | 0.3478 | 0.6182 | 874 | good trend (n.s.) |
| medium | A2 | base | accuracy | 90 | 0.4149 | 0.4065 | 0.008395 | 2.065 | 0.08418 | 0.06476 | 0.2104 | 232 | good trend (n.s.) |
| medium | A3 | base | accuracy | 90 | 0.42 | 0.4105 | 0.009549 | 2.326 | 0.07652 | 0.2352 | 0.2026 | 220 | good trend (n.s.) |
| medium | A3adv | base | accuracy | 90 | 0.3714 | 0.3704 | 0.000963 | 0.26 | 0.8016 | 0.00234 | 0.918 | 1.112e+04 | good trend (n.s.) |
| small | A0_A3 | base | accuracy | 90 | 0.4152 | 0.3875 | 0.02773 | 7.157 | 0.0001621 | 3.347e-05 | 0.007294 | 46 | GOOD (significant) |
| small | A1 | base | accuracy | 90 | 0.4084 | 0.404 | 0.004401 | 1.09 | 0.5439 | 0.1147 | 0.7648 | 1903 | good trend (n.s.) |
| small | A2 | base | accuracy | 90 | 0.4063 | 0.4046 | 0.001735 | 0.4287 | 0.762 | 0.3653 | 0.9023 | 7653 | good trend (n.s.) |
| small | A3 | base | accuracy | 90 | 0.3997 | 0.3898 | 0.009864 | 2.53 | 0.1449 | 0.104 | 0.3105 | 327 | good trend (n.s.) |
| small | A3adv | base | accuracy | 90 | 0.3686 | 0.3772 | -0.008648 | -2.293 | 0.02265 | 0.03805 | 0.1377 | 132 | bad trend (n.s.) |
| large | A0_A3 | base | client-drift E_drift | 90 | 0.01151 | 0.01426 | -0.002759 | -19.34 | 9.29e-05 | 5.289e-07 | 9.29e-05 | 43 | GOOD (significant) |
| large | A1 | base | client-drift E_drift | 90 | 0.01112 | 0.01602 | -0.004903 | -30.6 | 8.795e-08 | 5.105e-12 | 1.365e-07 | 21 | GOOD (significant) |
| large | A2 | base | client-drift E_drift | 90 | 0.01152 | 0.01623 | -0.004708 | -29.01 | 4.386e-07 | 3.379e-11 | 5.723e-07 | 24 | GOOD (significant) |
| large | A3 | base | client-drift E_drift | 90 | 0.01163 | 0.01593 | -0.004297 | -26.97 | 4.645e-08 | 1.719e-12 | 8.71e-08 | 20 | GOOD (significant) |
| large | A3adv | base | client-drift E_drift | 90 | 0.01862 | 0.04099 | -0.02237 | -54.57 | 1.398e-15 | 1.744e-16 | 1.573e-14 | 8 | GOOD (significant) |
| medium | A0_A3 | base | client-drift E_drift | 90 | 0.01166 | 0.01442 | -0.002757 | -19.12 | 6.51e-05 | 4.728e-09 | 6.83e-05 | 41 | GOOD (significant) |
| medium | A1 | base | client-drift E_drift | 90 | 0.01168 | 0.01646 | -0.004772 | -29 | 1.076e-09 | 7.096e-14 | 4.305e-09 | 16 | GOOD (significant) |
| medium | A2 | base | client-drift E_drift | 90 | 0.01145 | 0.0166 | -0.005151 | -31.04 | 2.497e-09 | 3.386e-14 | 7.491e-09 | 17 | GOOD (significant) |
| medium | A3 | base | client-drift E_drift | 90 | 0.01233 | 0.01525 | -0.002919 | -19.14 | 2.956e-05 | 1.821e-07 | 3.244e-05 | 37 | GOOD (significant) |
| medium | A3adv | base | client-drift E_drift | 90 | 0.01883 | 0.03971 | -0.02088 | -52.57 | 4.998e-21 | 1.744e-16 | 1.291e-19 | 5 | GOOD (significant) |
| small | A0_A3 | base | client-drift E_drift | 90 | 0.01095 | 0.01468 | -0.003734 | -25.44 | 1.304e-07 | 1.329e-10 | 1.779e-07 | 22 | GOOD (significant) |
| small | A1 | base | client-drift E_drift | 90 | 0.01128 | 0.01726 | -0.005978 | -34.63 | 6.026e-08 | 8.244e-12 | 9.798e-08 | 21 | GOOD (significant) |
| small | A2 | base | client-drift E_drift | 90 | 0.01073 | 0.01773 | -0.006998 | -39.47 | 3.076e-09 | 1.873e-14 | 8.65e-09 | 17 | GOOD (significant) |
| small | A3 | base | client-drift E_drift | 90 | 0.01192 | 0.01533 | -0.003408 | -22.24 | 1.88e-05 | 2.464e-07 | 2.169e-05 | 35 | GOOD (significant) |
| small | A3adv | base | client-drift E_drift | 90 | 0.01638 | 0.054 | -0.03762 | -69.67 | 4.035e-14 | 1.744e-16 | 3.026e-13 | 9 | GOOD (significant) |
| large | A0_A3 | base | drift alignment S_CDA | 90 | 0.3143 | 0.2727 | 0.04156 | 15.24 | 1.016e-12 | 8.922e-11 | 1.474e-12 | 11 | GOOD (significant) |
| large | A1 | base | drift alignment S_CDA | 90 | 0.3271 | 0.267 | 0.06015 | 22.53 | 4.208e-24 | 1.193e-15 | 1.894e-23 | 4 | GOOD (significant) |
| large | A2 | base | drift alignment S_CDA | 90 | 0.3262 | 0.2687 | 0.05755 | 21.42 | 1.741e-23 | 5.812e-15 | 7.122e-23 | 4 | GOOD (significant) |
| large | A3 | base | drift alignment S_CDA | 90 | 0.3019 | 0.2629 | 0.03893 | 14.81 | 1.007e-13 | 1.953e-11 | 1.511e-13 | 10 | GOOD (significant) |
| large | A3adv | base | drift alignment S_CDA | 90 | 0.2909 | 0.1287 | 0.1622 | 126 | 1.522e-42 | 1.995e-16 | 3.424e-41 | 2 | GOOD (significant) |
| medium | A0_A3 | base | drift alignment S_CDA | 90 | 0.3234 | 0.2812 | 0.04223 | 15.02 | 6.919e-16 | 2.649e-12 | 1.153e-15 | 8 | GOOD (significant) |
| medium | A1 | base | drift alignment S_CDA | 90 | 0.3303 | 0.2769 | 0.05339 | 19.28 | 2.887e-20 | 1.168e-14 | 7.218e-20 | 5 | GOOD (significant) |
| medium | A2 | base | drift alignment S_CDA | 90 | 0.3374 | 0.2772 | 0.06024 | 21.73 | 3.033e-23 | 4.954e-15 | 1.05e-22 | 4 | GOOD (significant) |
| medium | A3 | base | drift alignment S_CDA | 90 | 0.3268 | 0.2733 | 0.05357 | 19.6 | 2.031e-18 | 2.19e-14 | 4.351e-18 | 6 | GOOD (significant) |
| medium | A3adv | base | drift alignment S_CDA | 90 | 0.3108 | 0.1421 | 0.1687 | 118.7 | 3.997e-40 | 1.744e-16 | 2.998e-39 | 2 | GOOD (significant) |
| small | A0_A3 | base | drift alignment S_CDA | 90 | 0.3556 | 0.3186 | 0.03697 | 11.6 | 3.46e-12 | 1.294e-10 | 4.866e-12 | 11 | GOOD (significant) |
| small | A1 | base | drift alignment S_CDA | 90 | 0.3595 | 0.3061 | 0.05342 | 17.45 | 1.992e-22 | 2.778e-15 | 6.401e-22 | 5 | GOOD (significant) |
| small | A2 | base | drift alignment S_CDA | 90 | 0.3591 | 0.3019 | 0.05716 | 18.93 | 1.242e-21 | 6.195e-15 | 3.493e-21 | 5 | GOOD (significant) |
| small | A3 | base | drift alignment S_CDA | 90 | 0.3424 | 0.3185 | 0.02394 | 7.516 | 3.255e-07 | 1.025e-06 | 3.406e-07 | 24 | GOOD (significant) |
| small | A3adv | base | drift alignment S_CDA | 90 | 0.3382 | 0.1595 | 0.1786 | 112 | 2.226e-40 | 1.744e-16 | 2.004e-39 | 2 | GOOD (significant) |
| large | A0_A3 | JEQFL | accuracy | 90 | 0.3761 | 0.3635 | 0.01256 | 3.456 | 0.03198 | 0.01818 | 0.1439 | 149 | good trend (n.s.) |
| large | A1 | JEQFL | accuracy | 90 | 0.3768 | 0.378 | -0.001185 | -0.3135 | 0.8364 | 0.6933 | 0.918 | 1.647e+04 | bad trend (n.s.) |
| large | A2 | JEQFL | accuracy | 90 | 0.3818 | 0.3891 | -0.007296 | -1.875 | 0.1724 | 0.6896 | 0.3525 | 374 | bad trend (n.s.) |
| large | A3 | JEQFL | accuracy | 90 | 0.3745 | 0.364 | 0.01049 | 2.881 | 0.1097 | 0.1045 | 0.2599 | 271 | good trend (n.s.) |
| large | A3adv | JEQFL | accuracy | 90 | 0.3679 | 0.3556 | 0.01221 | 3.433 | 0.003339 | 0.006447 | 0.04838 | 78 | GOOD (significant) |
| medium | A0_A3 | JEQFL | accuracy | 90 | 0.4139 | 0.4027 | 0.01125 | 2.793 | 0.04925 | 0.06246 | 0.1847 | 178 | good trend (n.s.) |
| medium | A1 | JEQFL | accuracy | 90 | 0.4129 | 0.406 | 0.006901 | 1.7 | 0.2396 | 0.1002 | 0.4313 | 505 | good trend (n.s.) |
| medium | A2 | JEQFL | accuracy | 90 | 0.4149 | 0.4113 | 0.003586 | 0.8719 | 0.5129 | 0.3859 | 0.7446 | 1638 | good trend (n.s.) |
| medium | A3 | JEQFL | accuracy | 90 | 0.42 | 0.4084 | 0.01162 | 2.844 | 0.03762 | 0.05571 | 0.1539 | 159 | good trend (n.s.) |
| medium | A3adv | JEQFL | accuracy | 90 | 0.3714 | 0.3731 | -0.001753 | -0.4698 | 0.672 | 0.1033 | 0.864 | 3915 | bad trend (n.s.) |
| small | A0_A3 | JEQFL | accuracy | 90 | 0.4152 | 0.3965 | 0.01872 | 4.722 | 0.0153 | 0.01297 | 0.1148 | 116 | good trend (n.s.) |
| small | A1 | JEQFL | accuracy | 90 | 0.4084 | 0.4067 | 0.001667 | 0.4098 | 0.8264 | 0.2548 | 0.918 | 1.46e+04 | good trend (n.s.) |
| small | A2 | JEQFL | accuracy | 90 | 0.4063 | 0.4189 | -0.01259 | -3.006 | 0.05521 | 0.1452 | 0.1888 | 188 | bad trend (n.s.) |
| small | A3 | JEQFL | accuracy | 90 | 0.3997 | 0.3951 | 0.004574 | 1.158 | 0.4411 | 0.2436 | 0.6845 | 1180 | good trend (n.s.) |
| small | A3adv | JEQFL | accuracy | 90 | 0.3686 | 0.3798 | -0.01122 | -2.953 | 0.005375 | 0.008652 | 0.04838 | 87 | BAD (significant) |
| large | A0_A3 | JEQFL | client-drift E_drift | 90 | 0.01151 | 0.01395 | -0.002445 | -17.52 | 6.526e-05 | 8.069e-08 | 6.83e-05 | 41 | GOOD (significant) |
| large | A1 | JEQFL | client-drift E_drift | 90 | 0.01112 | 0.01609 | -0.004972 | -30.9 | 9.757e-08 | 1.186e-11 | 1.416e-07 | 21 | GOOD (significant) |
| large | A2 | JEQFL | client-drift E_drift | 90 | 0.01152 | 0.01587 | -0.004343 | -27.37 | 1.023e-07 | 1.848e-11 | 1.438e-07 | 22 | GOOD (significant) |
| large | A3 | JEQFL | client-drift E_drift | 90 | 0.01163 | 0.01562 | -0.003986 | -25.52 | 1.636e-06 | 3.379e-11 | 2.045e-06 | 27 | GOOD (significant) |
| large | A3adv | JEQFL | client-drift E_drift | 90 | 0.01862 | 0.04088 | -0.02226 | -54.45 | 5.931e-16 | 1.929e-16 | 8.897e-15 | 8 | GOOD (significant) |
| medium | A0_A3 | JEQFL | client-drift E_drift | 90 | 0.01166 | 0.01418 | -0.002512 | -17.72 | 8.667e-05 | 4.844e-09 | 8.864e-05 | 42 | GOOD (significant) |
| medium | A1 | JEQFL | client-drift E_drift | 90 | 0.01168 | 0.01659 | -0.004908 | -29.58 | 5.015e-08 | 8.27e-14 | 9.027e-08 | 20 | GOOD (significant) |
| medium | A2 | JEQFL | client-drift E_drift | 90 | 0.01145 | 0.01675 | -0.005304 | -31.66 | 1.548e-09 | 1.823e-15 | 4.975e-09 | 16 | GOOD (significant) |
| medium | A3 | JEQFL | client-drift E_drift | 90 | 0.01233 | 0.01539 | -0.003062 | -19.89 | 2.387e-05 | 8.827e-09 | 2.685e-05 | 36 | GOOD (significant) |
| medium | A3adv | JEQFL | client-drift E_drift | 90 | 0.01883 | 0.04021 | -0.02138 | -53.16 | 5.736e-21 | 1.744e-16 | 1.291e-19 | 5 | GOOD (significant) |
| small | A0_A3 | JEQFL | client-drift E_drift | 90 | 0.01095 | 0.01482 | -0.003877 | -26.15 | 5.739e-08 | 6.827e-11 | 9.798e-08 | 21 | GOOD (significant) |
| small | A1 | JEQFL | client-drift E_drift | 90 | 0.01128 | 0.01741 | -0.00613 | -35.2 | 7.504e-09 | 5.66e-13 | 1.608e-08 | 18 | GOOD (significant) |
| small | A2 | JEQFL | client-drift E_drift | 90 | 0.01073 | 0.01827 | -0.007536 | -41.25 | 9.945e-10 | 1.704e-14 | 4.305e-09 | 16 | GOOD (significant) |
| small | A3 | JEQFL | client-drift E_drift | 90 | 0.01192 | 0.01582 | -0.003905 | -24.68 | 6.418e-06 | 1.706e-07 | 7.6e-06 | 31 | GOOD (significant) |
| small | A3adv | JEQFL | client-drift E_drift | 90 | 0.01638 | 0.05331 | -0.03693 | -69.28 | 1.039e-14 | 1.744e-16 | 9.349e-14 | 9 | GOOD (significant) |
| large | A0_A3 | JEQFL | drift alignment S_CDA | 90 | 0.3143 | 0.2807 | 0.03357 | 11.96 | 1.967e-09 | 9.94e-09 | 2.212e-09 | 16 | GOOD (significant) |
| large | A1 | JEQFL | drift alignment S_CDA | 90 | 0.3271 | 0.2731 | 0.05402 | 19.78 | 1.638e-17 | 1.145e-12 | 3.35e-17 | 7 | GOOD (significant) |
| large | A2 | JEQFL | drift alignment S_CDA | 90 | 0.3262 | 0.2743 | 0.05192 | 18.93 | 8.986e-20 | 8.021e-14 | 2.022e-19 | 6 | GOOD (significant) |
| large | A3 | JEQFL | drift alignment S_CDA | 90 | 0.3019 | 0.2706 | 0.03128 | 11.56 | 6.667e-09 | 5.035e-08 | 7.317e-09 | 18 | GOOD (significant) |
| large | A3adv | JEQFL | drift alignment S_CDA | 90 | 0.2909 | 0.128 | 0.163 | 127.3 | 2.077e-45 | 1.744e-16 | 9.346e-44 | 1 | GOOD (significant) |
| medium | A0_A3 | JEQFL | drift alignment S_CDA | 90 | 0.3234 | 0.2804 | 0.04306 | 15.36 | 6.422e-17 | 1.249e-12 | 1.159e-16 | 7 | GOOD (significant) |
| medium | A1 | JEQFL | drift alignment S_CDA | 90 | 0.3303 | 0.277 | 0.05329 | 19.24 | 8.001e-17 | 6.559e-13 | 1.385e-16 | 7 | GOOD (significant) |
| medium | A2 | JEQFL | drift alignment S_CDA | 90 | 0.3374 | 0.2775 | 0.05991 | 21.59 | 3.255e-20 | 6.882e-14 | 7.708e-20 | 5 | GOOD (significant) |
| medium | A3 | JEQFL | drift alignment S_CDA | 90 | 0.3268 | 0.2759 | 0.05091 | 18.45 | 6.437e-17 | 1.663e-13 | 1.159e-16 | 7 | GOOD (significant) |
| medium | A3adv | JEQFL | drift alignment S_CDA | 90 | 0.3108 | 0.1437 | 0.1671 | 116.3 | 1.949e-40 | 1.744e-16 | 2.004e-39 | 2 | GOOD (significant) |
| small | A0_A3 | JEQFL | drift alignment S_CDA | 90 | 0.3556 | 0.3151 | 0.0405 | 12.85 | 1.774e-15 | 2.574e-12 | 2.851e-15 | 8 | GOOD (significant) |
| small | A1 | JEQFL | drift alignment S_CDA | 90 | 0.3595 | 0.3014 | 0.05808 | 19.27 | 3.915e-25 | 2.076e-15 | 2.202e-24 | 4 | GOOD (significant) |
| small | A2 | JEQFL | drift alignment S_CDA | 90 | 0.3591 | 0.3018 | 0.05727 | 18.98 | 1.573e-20 | 2.19e-14 | 4.164e-20 | 5 | GOOD (significant) |
| small | A3 | JEQFL | drift alignment S_CDA | 90 | 0.3424 | 0.3138 | 0.02866 | 9.134 | 1.433e-09 | 1.876e-08 | 1.653e-09 | 16 | GOOD (significant) |
| small | A3adv | JEQFL | drift alignment S_CDA | 90 | 0.3382 | 0.1641 | 0.1741 | 106.1 | 1.175e-41 | 1.744e-16 | 1.763e-40 | 2 | GOOD (significant) |
| large | A0_A3 | CDQ | accuracy | 90 | 0.3761 | 0.3755 | 0.0006173 | 0.1644 | 0.9252 | 0.2973 | 0.9333 | 7.976e+04 | good trend (n.s.) |
| large | A1 | CDQ | accuracy | 90 | 0.3768 | 0.3642 | 0.0126 | 3.459 | 0.02755 | 0.00243 | 0.1377 | 141 | good trend (n.s.) |
| large | A2 | CDQ | accuracy | 90 | 0.3818 | 0.367 | 0.01483 | 4.04 | 0.001608 | 0.003354 | 0.03617 | 67 | GOOD (significant) |
| large | A3 | CDQ | accuracy | 90 | 0.3745 | 0.373 | 0.001488 | 0.3988 | 0.7528 | 0.3573 | 0.9023 | 7081 | good trend (n.s.) |
| large | A3adv | CDQ | accuracy | 90 | 0.3679 | 0.363 | 0.004877 | 1.343 | 0.2077 | 0.4542 | 0.4065 | 439 | good trend (n.s.) |
| medium | A0_A3 | CDQ | accuracy | 90 | 0.4139 | 0.4133 | 0.0006667 | 0.1613 | 0.916 | 0.937 | 0.9333 | 6.309e+04 | good trend (n.s.) |
| medium | A1 | CDQ | accuracy | 90 | 0.4129 | 0.4098 | 0.003031 | 0.7395 | 0.6099 | 0.5435 | 0.8316 | 2694 | good trend (n.s.) |
| medium | A2 | CDQ | accuracy | 90 | 0.4149 | 0.41 | 0.004957 | 1.209 | 0.367 | 0.376 | 0.6182 | 860 | good trend (n.s.) |
| medium | A3 | CDQ | accuracy | 90 | 0.42 | 0.4085 | 0.0115 | 2.815 | 0.06946 | 0.1581 | 0.1954 | 210 | good trend (n.s.) |
| medium | A3adv | CDQ | accuracy | 90 | 0.3714 | 0.3709 | 0.0004753 | 0.1282 | 0.9172 | 0.5023 | 0.9333 | 6.498e+04 | good trend (n.s.) |
| small | A0_A3 | CDQ | accuracy | 90 | 0.4152 | 0.4024 | 0.01285 | 3.194 | 0.06139 | 0.2 | 0.1888 | 197 | good trend (n.s.) |
| small | A1 | CDQ | accuracy | 90 | 0.4084 | 0.4041 | 0.004253 | 1.052 | 0.4911 | 0.5101 | 0.7366 | 1478 | good trend (n.s.) |
| small | A2 | CDQ | accuracy | 90 | 0.4063 | 0.4105 | -0.00421 | -1.025 | 0.4067 | 0.5355 | 0.6537 | 1017 | bad trend (n.s.) |
| small | A3 | CDQ | accuracy | 90 | 0.3997 | 0.4024 | -0.002691 | -0.6689 | 0.6316 | 0.68 | 0.8359 | 3051 | bad trend (n.s.) |
| small | A3adv | CDQ | accuracy | 90 | 0.3686 | 0.3674 | 0.001191 | 0.3243 | 0.7298 | 0.6537 | 0.9023 | 5886 | good trend (n.s.) |
| large | A0_A3 | CDQ | client-drift E_drift | 90 | 0.01151 | 0.02614 | -0.01464 | -55.99 | 4.451e-07 | 4.085e-13 | 5.723e-07 | 24 | GOOD (significant) |
| large | A1 | CDQ | client-drift E_drift | 90 | 0.01112 | 0.02633 | -0.01521 | -57.77 | 7.377e-09 | 1.876e-13 | 1.608e-08 | 18 | GOOD (significant) |
| large | A2 | CDQ | client-drift E_drift | 90 | 0.01152 | 0.02666 | -0.01513 | -56.77 | 6.642e-09 | 5.66e-13 | 1.573e-08 | 18 | GOOD (significant) |
| large | A3 | CDQ | client-drift E_drift | 90 | 0.01163 | 0.0251 | -0.01347 | -53.65 | 8.564e-09 | 1.601e-15 | 1.752e-08 | 18 | GOOD (significant) |
| large | A3adv | CDQ | client-drift E_drift | 90 | 0.01862 | 0.03751 | -0.01889 | -50.35 | 1.82e-06 | 1.219e-11 | 2.213e-06 | 28 | GOOD (significant) |
| medium | A0_A3 | CDQ | client-drift E_drift | 90 | 0.01166 | 0.02625 | -0.01458 | -55.56 | 6.327e-09 | 6.186e-16 | 1.573e-08 | 18 | GOOD (significant) |
| medium | A1 | CDQ | client-drift E_drift | 90 | 0.01168 | 0.02798 | -0.0163 | -58.24 | 1.317e-09 | 1.995e-16 | 4.56e-09 | 16 | GOOD (significant) |
| medium | A2 | CDQ | client-drift E_drift | 90 | 0.01145 | 0.02857 | -0.01713 | -59.94 | 7.186e-10 | 2.98e-16 | 3.593e-09 | 15 | GOOD (significant) |
| medium | A3 | CDQ | client-drift E_drift | 90 | 0.01233 | 0.02875 | -0.01642 | -57.1 | 1.908e-10 | 4.157e-16 | 1.227e-09 | 14 | GOOD (significant) |
| medium | A3adv | CDQ | client-drift E_drift | 90 | 0.01883 | 0.03707 | -0.01824 | -49.2 | 9.279e-08 | 9.931e-14 | 1.392e-07 | 21 | GOOD (significant) |
| small | A0_A3 | CDQ | client-drift E_drift | 90 | 0.01095 | 0.03355 | -0.0226 | -67.37 | 1.148e-09 | 2.063e-16 | 4.305e-09 | 16 | GOOD (significant) |
| small | A1 | CDQ | client-drift E_drift | 90 | 0.01128 | 0.03294 | -0.02166 | -65.74 | 6.258e-10 | 1.744e-16 | 3.52e-09 | 15 | GOOD (significant) |
| small | A2 | CDQ | client-drift E_drift | 90 | 0.01073 | 0.03231 | -0.02158 | -66.78 | 6.437e-09 | 2.608e-16 | 1.573e-08 | 18 | GOOD (significant) |
| small | A3 | CDQ | client-drift E_drift | 90 | 0.01192 | 0.03588 | -0.02396 | -66.79 | 6.097e-08 | 2.608e-16 | 9.798e-08 | 21 | GOOD (significant) |
| small | A3adv | CDQ | client-drift E_drift | 90 | 0.01638 | 0.03588 | -0.0195 | -54.35 | 1.408e-08 | 3.594e-15 | 2.755e-08 | 19 | GOOD (significant) |
| large | A0_A3 | CDQ | drift alignment S_CDA | 90 | 0.3143 | 0.2807 | 0.03354 | 11.95 | 7.995e-10 | 6.315e-09 | 9.468e-10 | 15 | GOOD (significant) |
| large | A1 | CDQ | drift alignment S_CDA | 90 | 0.3271 | 0.2895 | 0.03761 | 12.99 | 4.534e-11 | 6.626e-09 | 6.001e-11 | 13 | GOOD (significant) |
| large | A2 | CDQ | drift alignment S_CDA | 90 | 0.3262 | 0.2962 | 0.03 | 10.13 | 2.269e-08 | 1.284e-07 | 2.431e-08 | 19 | GOOD (significant) |
| large | A3 | CDQ | drift alignment S_CDA | 90 | 0.3019 | 0.2695 | 0.0324 | 12.02 | 2.824e-10 | 7.649e-09 | 3.53e-10 | 14 | GOOD (significant) |
| large | A3adv | CDQ | drift alignment S_CDA | 90 | 0.2909 | 0.2836 | 0.007317 | 2.58 | 0.09188 | 0.02621 | 0.09188 | 244 | good trend (n.s.) |
| medium | A0_A3 | CDQ | drift alignment S_CDA | 90 | 0.3234 | 0.2916 | 0.03185 | 10.92 | 6.283e-10 | 7.12e-09 | 7.641e-10 | 15 | GOOD (significant) |
| medium | A1 | CDQ | drift alignment S_CDA | 90 | 0.3303 | 0.2886 | 0.04167 | 14.44 | 7.412e-15 | 8.479e-12 | 1.15e-14 | 9 | GOOD (significant) |
| medium | A2 | CDQ | drift alignment S_CDA | 90 | 0.3374 | 0.3007 | 0.03672 | 12.21 | 7.994e-11 | 9.717e-10 | 1.028e-10 | 13 | GOOD (significant) |
| medium | A3 | CDQ | drift alignment S_CDA | 90 | 0.3268 | 0.2789 | 0.04796 | 17.2 | 4.224e-17 | 2.181e-13 | 8.265e-17 | 7 | GOOD (significant) |
| medium | A3adv | CDQ | drift alignment S_CDA | 90 | 0.3108 | 0.2796 | 0.03116 | 11.14 | 1.684e-11 | 2.698e-10 | 2.297e-11 | 12 | GOOD (significant) |
| small | A0_A3 | CDQ | drift alignment S_CDA | 90 | 0.3556 | 0.2906 | 0.06497 | 22.35 | 1.188e-25 | 3.37e-15 | 7.636e-25 | 4 | GOOD (significant) |
| small | A1 | CDQ | drift alignment S_CDA | 90 | 0.3595 | 0.2977 | 0.06175 | 20.74 | 1.212e-24 | 2.363e-15 | 6.06e-24 | 4 | GOOD (significant) |
| small | A2 | CDQ | drift alignment S_CDA | 90 | 0.3591 | 0.2987 | 0.06037 | 20.21 | 3.07e-22 | 7.741e-15 | 9.21e-22 | 5 | GOOD (significant) |
| small | A3 | CDQ | drift alignment S_CDA | 90 | 0.3424 | 0.2839 | 0.05849 | 20.6 | 2.465e-23 | 9.976e-15 | 9.245e-23 | 4 | GOOD (significant) |
| small | A3adv | CDQ | drift alignment S_CDA | 90 | 0.3382 | 0.3232 | 0.01496 | 4.628 | 0.001481 | 0.00149 | 0.001514 | 66 | GOOD (significant) |

## table9 shrinkage ablation

Gauss-Markov orphan-shrinkage ablation: CDQ-lit (shrinkage on) vs CDQ (shrinkage removed).

| scale | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | CDQ | accuracy | 450 | 0.3754 | 0.3685 | 0.006881 | 1.867 | 0.00301 | 5.572e-05 | 0.009029 | 397 | GOOD (significant) |
| medium | CDQ | accuracy | 450 | 0.4066 | 0.4025 | 0.004126 | 1.025 | 0.1079 | 0.2377 | 0.1618 | 1362 | good trend (n.s.) |
| small | CDQ | accuracy | 450 | 0.3996 | 0.3974 | 0.002279 | 0.5735 | 0.3577 | 0.65 | 0.3577 | 4166 | good trend (n.s.) |
| large | CDQ | client-drift E_drift | 450 | 0.01288 | 0.02835 | -0.01547 | -54.56 | 3.085e-32 | 4.096e-60 | 3.085e-32 | 22 | GOOD (significant) |
| medium | CDQ | client-drift E_drift | 450 | 0.01319 | 0.02972 | -0.01653 | -55.62 | 6.611e-40 | 1.436e-71 | 1.983e-39 | 17 | GOOD (significant) |
| small | CDQ | client-drift E_drift | 450 | 0.01225 | 0.03411 | -0.02186 | -64.08 | 8.604e-39 | 1.98e-74 | 1.291e-38 | 18 | GOOD (significant) |
| large | CDQ | drift alignment S_CDA | 450 | 0.3121 | 0.2839 | 0.02817 | 9.923 | 5.04e-33 | 1.379e-30 | 5.04e-33 | 21 | GOOD (significant) |
| medium | CDQ | drift alignment S_CDA | 450 | 0.3258 | 0.2879 | 0.03787 | 13.16 | 2.639e-57 | 8.567e-48 | 3.959e-57 | 11 | GOOD (significant) |
| small | CDQ | drift alignment S_CDA | 450 | 0.351 | 0.2989 | 0.05211 | 17.44 | 1.709e-82 | 9.075e-59 | 5.128e-82 | 7 | GOOD (significant) |
| large | CDQ | reconstruction error | 450 | 0.07855 | 0.1089 | -0.0303 | -27.84 | 2.33e-48 | 3.2e-59 | 2.33e-48 | 13 | GOOD (significant) |
| medium | CDQ | reconstruction error | 450 | 0.08095 | 0.1193 | -0.03831 | -32.12 | 1.261e-62 | 2.432e-74 | 1.892e-62 | 10 | GOOD (significant) |
| small | CDQ | reconstruction error | 450 | 0.08383 | 0.1315 | -0.04766 | -36.25 | 1.239e-63 | 1.02e-74 | 3.717e-63 | 9 | GOOD (significant) |
| large | CDQ | active clients | 450 | 9.452 | 9.452 | -0.0004506 | -0.004767 | 0.8054 | 0.8726 | 0.8054 | 5.813e+04 | bad trend (n.s.) |
| medium | CDQ | active clients | 450 | 9.471 | 9.47 | 0.0006296 | 0.006648 | 0.7394 | 0.7538 | 0.8054 | 3.187e+04 | good trend (n.s.) |
| small | CDQ | active clients | 450 | 9.468 | 9.467 | 0.0005926 | 0.006259 | 0.7244 | 0.711 | 0.8054 | 2.838e+04 | good trend (n.s.) |
| large | CDQ | /g_hat///g*/ | 450 | 1.297 | 1.713 | -0.4166 | -24.32 | 3.11e-55 | 9.672e-63 | 3.11e-55 | 11 | n/a (diagnostic) |
| medium | CDQ | /g_hat///g*/ | 450 | 1.253 | 1.619 | -0.3667 | -22.64 | 1.218e-61 | 6.658e-65 | 1.826e-61 | 10 | n/a (diagnostic) |
| small | CDQ | /g_hat///g*/ | 450 | 1.182 | 1.554 | -0.3722 | -23.94 | 1.819e-72 | 3.891e-73 | 5.456e-72 | 8 | n/a (diagnostic) |
| large | CDQ | Bad-tier weight share | 450 | 0.2825 | 0.2824 | 0.0001524 | 0.05397 | 0.2769 | 0.2219 | 0.2769 | 2980 | n/a (diagnostic) |
| medium | CDQ | Bad-tier weight share | 450 | 0.293 | 0.2927 | 0.0002854 | 0.09748 | 0.07224 | 0.1615 | 0.1084 | 1088 | n/a (diagnostic) |
| small | CDQ | Bad-tier weight share | 450 | 0.2904 | 0.2898 | 0.0006171 | 0.2129 | 2.704e-05 | 0.0001801 | 8.111e-05 | 197 | n/a (diagnostic) |

## table10 innovation ablation lit

Per-innovation ablation anchored on CDQ-lit (contribution = CDQ-lit minus CDQ-lit without it).

| scale | removed | metric | n_pairs | full | ablated | contribution | sd | t | p | q_BH | innovation_helps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| large | I1 | accuracy | 60 | 0.3737 | 0.3658 | 0.00788 | 0.02856 | 2.137 | 0.03677 | 0.08645 | good trend (n.s.) |
| medium | I1 | accuracy | 60 | 0.3906 | 0.3899 | 0.0006574 | 0.03343 | 0.1523 | 0.8794 | 0.9423 | good trend (n.s.) |
| small | I1 | accuracy | 60 | 0.3663 | 0.3725 | -0.006194 | 0.04322 | -1.11 | 0.2714 | 0.4211 | bad trend (n.s.) |
| large | I1 | client-drift E_drift | 60 | 0.01648 | 0.01957 | -0.003089 | 0.008599 | -2.783 | 0.007227 | 0.02502 | GOOD (significant) |
| medium | I1 | client-drift E_drift | 60 | 0.01753 | 0.01683 | 0.0007046 | 0.006246 | 0.8739 | 0.3857 | 0.5305 | bad trend (n.s.) |
| small | I1 | client-drift E_drift | 60 | 0.01631 | 0.01637 | -6.02e-05 | 0.005011 | -0.09306 | 0.9262 | 0.9664 | good trend (n.s.) |
| large | I1 | drift alignment S_CDA | 60 | 0.2901 | 0.2587 | 0.03136 | 0.03669 | 6.621 | 1.182e-08 | 2.66e-07 | GOOD (significant) |
| medium | I1 | drift alignment S_CDA | 60 | 0.3113 | 0.2916 | 0.01967 | 0.04959 | 3.073 | 0.003205 | 0.01311 | GOOD (significant) |
| small | I1 | drift alignment S_CDA | 60 | 0.3368 | 0.3205 | 0.01629 | 0.03566 | 3.538 | 0.000792 | 0.00396 | GOOD (significant) |
| large | I2 | accuracy | 60 | 0.3737 | 0.371 | 0.002639 | 0.02515 | 0.8128 | 0.4196 | 0.5554 | good trend (n.s.) |
| medium | I2 | accuracy | 60 | 0.3906 | 0.3876 | 0.002963 | 0.03226 | 0.7115 | 0.4796 | 0.5995 | good trend (n.s.) |
| small | I2 | accuracy | 60 | 0.3663 | 0.3604 | 0.005935 | 0.05239 | 0.8775 | 0.3838 | 0.5305 | good trend (n.s.) |
| large | I2 | client-drift E_drift | 60 | 0.01648 | 0.01306 | 0.003418 | 0.007072 | 3.744 | 0.0004133 | 0.002325 | BAD (significant) |
| medium | I2 | client-drift E_drift | 60 | 0.01753 | 0.01597 | 0.001558 | 0.005329 | 2.265 | 0.02723 | 0.07765 | bad trend (n.s.) |
| small | I2 | client-drift E_drift | 60 | 0.01631 | 0.01467 | 0.001646 | 0.005643 | 2.259 | 0.02761 | 0.07765 | bad trend (n.s.) |
| large | I2 | drift alignment S_CDA | 60 | 0.2901 | 0.3029 | -0.01279 | 0.02971 | -3.333 | 0.001487 | 0.00669 | BAD (significant) |
| medium | I2 | drift alignment S_CDA | 60 | 0.3113 | 0.3199 | -0.008549 | 0.03827 | -1.73 | 0.0888 | 0.1665 | bad trend (n.s.) |
| small | I2 | drift alignment S_CDA | 60 | 0.3368 | 0.3487 | -0.01191 | 0.04356 | -2.118 | 0.03842 | 0.08645 | bad trend (n.s.) |
| large | I3a | accuracy | 60 | 0.3737 | 0.3664 | 0.007278 | 0.04651 | 1.212 | 0.2303 | 0.3701 | good trend (n.s.) |
| medium | I3a | accuracy | 60 | 0.3906 | 0.3917 | -0.001083 | 0.03451 | -0.2431 | 0.8087 | 0.9098 | bad trend (n.s.) |
| small | I3a | accuracy | 60 | 0.3663 | 0.3675 | -0.001213 | 0.0471 | -0.1995 | 0.8426 | 0.9248 | bad trend (n.s.) |
| large | I3a | client-drift E_drift | 60 | 0.01648 | 0.02862 | -0.01214 | 0.02202 | -4.272 | 7.158e-05 | 0.0005368 | GOOD (significant) |
| medium | I3a | client-drift E_drift | 60 | 0.01753 | 0.02759 | -0.01006 | 0.01566 | -4.975 | 5.978e-06 | 5.38e-05 | GOOD (significant) |
| small | I3a | client-drift E_drift | 60 | 0.01631 | 0.03631 | -0.02 | 0.02337 | -6.629 | 1.145e-08 | 2.66e-07 | GOOD (significant) |
| large | I3a | drift alignment S_CDA | 60 | 0.2901 | 0.2932 | -0.003161 | 0.03552 | -0.6892 | 0.4934 | 0.6001 | bad trend (n.s.) |
| medium | I3a | drift alignment S_CDA | 60 | 0.3113 | 0.2996 | 0.01168 | 0.04149 | 2.181 | 0.03321 | 0.08645 | good trend (n.s.) |
| small | I3a | drift alignment S_CDA | 60 | 0.3368 | 0.3114 | 0.0254 | 0.03336 | 5.899 | 1.903e-07 | 2.855e-06 | GOOD (significant) |
| large | I3b | accuracy | 60 | 0.3737 | 0.3716 | 0.002102 | 0.02613 | 0.623 | 0.5357 | 0.6344 | good trend (n.s.) |
| medium | I3b | accuracy | 60 | 0.3906 | 0.4004 | -0.009778 | 0.0391 | -1.937 | 0.05755 | 0.1177 | bad trend (n.s.) |
| small | I3b | accuracy | 60 | 0.3663 | 0.3777 | -0.01138 | 0.04229 | -2.084 | 0.04146 | 0.08883 | bad trend (n.s.) |
| large | I3b | client-drift E_drift | 60 | 0.01648 | 0.01536 | 0.001119 | 0.005644 | 1.536 | 0.1299 | 0.2338 | bad trend (n.s.) |
| medium | I3b | client-drift E_drift | 60 | 0.01753 | 0.01702 | 0.0005127 | 0.005538 | 0.717 | 0.4762 | 0.5995 | bad trend (n.s.) |
| small | I3b | client-drift E_drift | 60 | 0.01631 | 0.01803 | -0.001723 | 0.006271 | -2.128 | 0.03749 | 0.08645 | good trend (n.s.) |
| large | I3b | drift alignment S_CDA | 60 | 0.2901 | 0.2976 | -0.007502 | 0.04656 | -1.248 | 0.2169 | 0.3615 | bad trend (n.s.) |
| medium | I3b | drift alignment S_CDA | 60 | 0.3113 | 0.3169 | -0.00556 | 0.04192 | -1.027 | 0.3084 | 0.4626 | bad trend (n.s.) |
| small | I3b | drift alignment S_CDA | 60 | 0.3368 | 0.3268 | 0.01005 | 0.05751 | 1.353 | 0.1812 | 0.3137 | good trend (n.s.) |
| large | I4 | accuracy | 60 | 0.3737 | 0.3735 | 0.0001759 | 0.02834 | 0.04809 | 0.9618 | 0.9664 | good trend (n.s.) |
| medium | I4 | accuracy | 60 | 0.3906 | 0.3908 | -0.0001944 | 0.03556 | -0.04235 | 0.9664 | 0.9664 | bad trend (n.s.) |
| small | I4 | accuracy | 60 | 0.3663 | 0.3644 | 0.001917 | 0.04165 | 0.3565 | 0.7227 | 0.8339 | good trend (n.s.) |
| large | I4 | client-drift E_drift | 60 | 0.01648 | 0.01295 | 0.003524 | 0.005154 | 5.296 | 1.835e-06 | 2.064e-05 | BAD (significant) |
| medium | I4 | client-drift E_drift | 60 | 0.01753 | 0.01599 | 0.001546 | 0.006495 | 1.844 | 0.07019 | 0.1373 | bad trend (n.s.) |
| small | I4 | client-drift E_drift | 60 | 0.01631 | 0.01578 | 0.0005361 | 0.004785 | 0.8678 | 0.389 | 0.5305 | bad trend (n.s.) |
| large | I4 | drift alignment S_CDA | 60 | 0.2901 | 0.3074 | -0.01736 | 0.03284 | -4.094 | 0.0001308 | 0.0008411 | BAD (significant) |
| medium | I4 | drift alignment S_CDA | 60 | 0.3113 | 0.3252 | -0.01391 | 0.04053 | -2.658 | 0.0101 | 0.03245 | BAD (significant) |
| small | I4 | drift alignment S_CDA | 60 | 0.3368 | 0.3521 | -0.01523 | 0.04119 | -2.864 | 0.005777 | 0.02166 | BAD (significant) |

## table11 innovation ablation cdq

Per-innovation ablation anchored on CDQ.

| scale | removed | metric | n_pairs | full | ablated | contribution | sd | t | p | q_BH | innovation_helps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| large | I1 | accuracy | 60 | 0.3619 | 0.3557 | 0.006213 | 0.04563 | 1.055 | 0.2958 | 0.4034 | good trend (n.s.) |
| medium | I1 | accuracy | 60 | 0.3847 | 0.3795 | 0.00525 | 0.05222 | 0.7787 | 0.4393 | 0.5202 | good trend (n.s.) |
| small | I1 | accuracy | 60 | 0.3675 | 0.368 | -0.0005648 | 0.0548 | -0.07984 | 0.9366 | 0.9579 | bad trend (n.s.) |
| large | I1 | client-drift E_drift | 60 | 0.04015 | 0.04193 | -0.001789 | 0.01526 | -0.9083 | 0.3674 | 0.4724 | good trend (n.s.) |
| medium | I1 | client-drift E_drift | 60 | 0.04493 | 0.04187 | 0.00307 | 0.01855 | 1.282 | 0.2048 | 0.3178 | bad trend (n.s.) |
| small | I1 | client-drift E_drift | 60 | 0.05223 | 0.04804 | 0.004193 | 0.03005 | 1.081 | 0.2842 | 0.3997 | bad trend (n.s.) |
| large | I1 | drift alignment S_CDA | 60 | 0.2585 | 0.2226 | 0.03588 | 0.03796 | 7.322 | 7.698e-10 | 3.464e-08 | GOOD (significant) |
| medium | I1 | drift alignment S_CDA | 60 | 0.2772 | 0.2578 | 0.01944 | 0.04386 | 3.433 | 0.001097 | 0.002743 | GOOD (significant) |
| small | I1 | drift alignment S_CDA | 60 | 0.2965 | 0.2813 | 0.01523 | 0.04104 | 2.874 | 0.005621 | 0.0115 | GOOD (significant) |
| large | I2 | accuracy | 60 | 0.3619 | 0.3587 | 0.003278 | 0.03509 | 0.7235 | 0.4723 | 0.5439 | good trend (n.s.) |
| medium | I2 | accuracy | 60 | 0.3847 | 0.3756 | 0.009083 | 0.05791 | 1.215 | 0.2292 | 0.3438 | good trend (n.s.) |
| small | I2 | accuracy | 60 | 0.3675 | 0.3699 | -0.002463 | 0.05961 | -0.32 | 0.7501 | 0.8036 | bad trend (n.s.) |
| large | I2 | client-drift E_drift | 60 | 0.04015 | 0.03132 | 0.00883 | 0.01664 | 4.111 | 0.0001236 | 0.0003708 | BAD (significant) |
| medium | I2 | client-drift E_drift | 60 | 0.04493 | 0.03765 | 0.007286 | 0.01239 | 4.555 | 2.684e-05 | 0.0001208 | BAD (significant) |
| small | I2 | client-drift E_drift | 60 | 0.05223 | 0.03592 | 0.01631 | 0.03096 | 4.082 | 0.0001363 | 0.0003834 | BAD (significant) |
| large | I2 | drift alignment S_CDA | 60 | 0.2585 | 0.275 | -0.01656 | 0.04451 | -2.882 | 0.005496 | 0.0115 | BAD (significant) |
| medium | I2 | drift alignment S_CDA | 60 | 0.2772 | 0.2848 | -0.007595 | 0.04345 | -1.354 | 0.1809 | 0.2907 | bad trend (n.s.) |
| small | I2 | drift alignment S_CDA | 60 | 0.2965 | 0.3123 | -0.01581 | 0.05748 | -2.131 | 0.0373 | 0.06456 | bad trend (n.s.) |
| large | I3a | accuracy | 60 | 0.3619 | 0.3664 | -0.004472 | 0.04241 | -0.8168 | 0.4173 | 0.5075 | bad trend (n.s.) |
| medium | I3a | accuracy | 60 | 0.3847 | 0.3917 | -0.006954 | 0.05208 | -1.034 | 0.3053 | 0.404 | bad trend (n.s.) |
| small | I3a | accuracy | 60 | 0.3675 | 0.3675 | -2.778e-05 | 0.04987 | -0.004315 | 0.9966 | 0.9966 | bad trend (n.s.) |
| large | I3a | client-drift E_drift | 60 | 0.04015 | 0.02862 | 0.01152 | 0.01871 | 4.77 | 1.251e-05 | 6.578e-05 | BAD (significant) |
| medium | I3a | client-drift E_drift | 60 | 0.04493 | 0.02759 | 0.01734 | 0.02801 | 4.796 | 1.137e-05 | 6.578e-05 | BAD (significant) |
| small | I3a | client-drift E_drift | 60 | 0.05223 | 0.03631 | 0.01592 | 0.03845 | 3.207 | 0.002169 | 0.00488 | BAD (significant) |
| large | I3a | drift alignment S_CDA | 60 | 0.2585 | 0.2932 | -0.03477 | 0.04111 | -6.551 | 1.552e-08 | 3.492e-07 | BAD (significant) |
| medium | I3a | drift alignment S_CDA | 60 | 0.2772 | 0.2996 | -0.02239 | 0.03647 | -4.756 | 1.316e-05 | 6.578e-05 | BAD (significant) |
| small | I3a | drift alignment S_CDA | 60 | 0.2965 | 0.3114 | -0.01494 | 0.04545 | -2.545 | 0.01355 | 0.02651 | BAD (significant) |
| large | I3b | accuracy | 60 | 0.3619 | 0.3602 | 0.001741 | 0.04023 | 0.3352 | 0.7387 | 0.8036 | good trend (n.s.) |
| medium | I3b | accuracy | 60 | 0.3847 | 0.3953 | -0.01062 | 0.04097 | -2.008 | 0.04921 | 0.08202 | bad trend (n.s.) |
| small | I3b | accuracy | 60 | 0.3675 | 0.3823 | -0.01481 | 0.04981 | -2.304 | 0.02477 | 0.04459 | BAD (significant) |
| large | I3b | client-drift E_drift | 60 | 0.04015 | 0.02886 | 0.01129 | 0.01953 | 4.478 | 3.505e-05 | 0.0001434 | BAD (significant) |
| medium | I3b | client-drift E_drift | 60 | 0.04493 | 0.02919 | 0.01575 | 0.02278 | 5.356 | 1.47e-06 | 1.653e-05 | BAD (significant) |
| small | I3b | client-drift E_drift | 60 | 0.05223 | 0.0331 | 0.01914 | 0.03542 | 4.185 | 9.619e-05 | 0.0003092 | BAD (significant) |
| large | I3b | drift alignment S_CDA | 60 | 0.2585 | 0.2916 | -0.0331 | 0.06046 | -4.241 | 7.952e-05 | 0.0002753 | BAD (significant) |
| medium | I3b | drift alignment S_CDA | 60 | 0.2772 | 0.312 | -0.03471 | 0.05233 | -5.138 | 3.292e-06 | 2.469e-05 | BAD (significant) |
| small | I3b | drift alignment S_CDA | 60 | 0.2965 | 0.3292 | -0.03272 | 0.06993 | -3.624 | 0.0006049 | 0.001601 | BAD (significant) |
| large | I4 | accuracy | 60 | 0.3619 | 0.3574 | 0.004574 | 0.05025 | 0.7051 | 0.4835 | 0.5439 | good trend (n.s.) |
| medium | I4 | accuracy | 60 | 0.3847 | 0.3896 | -0.004926 | 0.04634 | -0.8234 | 0.4136 | 0.5075 | bad trend (n.s.) |
| small | I4 | accuracy | 60 | 0.3675 | 0.3667 | 0.0007593 | 0.06408 | 0.09177 | 0.9272 | 0.9579 | good trend (n.s.) |
| large | I4 | client-drift E_drift | 60 | 0.04015 | 0.03841 | 0.001732 | 0.01177 | 1.14 | 0.2591 | 0.3761 | bad trend (n.s.) |
| medium | I4 | client-drift E_drift | 60 | 0.04493 | 0.03945 | 0.005484 | 0.01253 | 3.39 | 0.001253 | 0.002967 | BAD (significant) |
| small | I4 | client-drift E_drift | 60 | 0.05223 | 0.04367 | 0.008559 | 0.02852 | 2.325 | 0.02354 | 0.04413 | BAD (significant) |
| large | I4 | drift alignment S_CDA | 60 | 0.2585 | 0.2819 | -0.02341 | 0.04207 | -4.311 | 6.268e-05 | 0.0002351 | BAD (significant) |
| medium | I4 | drift alignment S_CDA | 60 | 0.2772 | 0.3065 | -0.02929 | 0.0389 | -5.833 | 2.446e-07 | 3.67e-06 | BAD (significant) |
| small | I4 | drift alignment S_CDA | 60 | 0.2965 | 0.3297 | -0.03317 | 0.04944 | -5.196 | 2.658e-06 | 2.392e-05 | BAD (significant) |

## table12 power

Observed paired effect, paired sd and the number of pairs needed for 80% power.

| scale | baseline | metric | n_pairs | gap | sd | n_80pow | p | q_BH | verdict |
|---|---|---|---|---|---|---|---|---|---|
| large | base | accuracy | 450 | 0.006446 | 0.05386 | 549 | 0.01146 | 0.02751 | GOOD (significant) |
| medium | base | accuracy | 450 | 0.006449 | 0.04742 | 425 | 0.004104 | 0.01407 | GOOD (significant) |
| small | base | accuracy | 450 | 0.007017 | 0.05992 | 573 | 0.01335 | 0.02776 | GOOD (significant) |
| large | base | client-drift E_drift | 450 | -0.007807 | 0.01386 | 25 | 8.862e-29 | 1.418e-28 | GOOD (significant) |
| medium | base | client-drift E_drift | 450 | -0.007295 | 0.01153 | 20 | 9.477e-35 | 3.249e-34 | GOOD (significant) |
| small | base | client-drift E_drift | 450 | -0.01155 | 0.02326 | 32 | 2.491e-23 | 2.594e-23 | GOOD (significant) |
| large | base | drift alignment S_CDA | 450 | 0.07208 | 0.06543 | 7 | 1.286e-79 | 4.408e-79 | GOOD (significant) |
| medium | base | drift alignment S_CDA | 450 | 0.07562 | 0.06759 | 7 | 2.73e-81 | 1.638e-80 | GOOD (significant) |
| small | base | drift alignment S_CDA | 450 | 0.07003 | 0.07399 | 9 | 1.857e-64 | 2.622e-64 | GOOD (significant) |
| large | JEQFL | accuracy | 450 | 0.005356 | 0.05281 | 764 | 0.03199 | 0.05119 | good trend (n.s.) |
| medium | JEQFL | accuracy | 450 | 0.00632 | 0.05075 | 507 | 0.008535 | 0.02276 | GOOD (significant) |
| small | JEQFL | accuracy | 450 | 0.0002309 | 0.06187 | 5.636e+05 | 0.9369 | 0.9369 | good trend (n.s.) |
| large | JEQFL | client-drift E_drift | 450 | -0.007601 | 0.01361 | 26 | 2.278e-28 | 3.417e-28 | GOOD (significant) |
| medium | JEQFL | client-drift E_drift | 450 | -0.007432 | 0.0119 | 21 | 4.788e-34 | 1.436e-33 | GOOD (significant) |
| small | JEQFL | client-drift E_drift | 450 | -0.01168 | 0.02242 | 29 | 2.866e-25 | 3.44e-25 | GOOD (significant) |
| large | JEQFL | drift alignment S_CDA | 450 | 0.06675 | 0.06863 | 9 | 5.278e-67 | 7.916e-67 | GOOD (significant) |
| medium | JEQFL | drift alignment S_CDA | 450 | 0.07485 | 0.06858 | 7 | 1.273e-78 | 3.395e-78 | GOOD (significant) |
| small | JEQFL | drift alignment S_CDA | 450 | 0.07171 | 0.07036 | 8 | 1.409e-71 | 2.819e-71 | GOOD (significant) |
| large | M4a | accuracy | 450 | 0.003111 | 0.0538 | 2347 | 0.2206 | 0.2786 | good trend (n.s.) |
| medium | M4a | accuracy | 450 | 0.006019 | 0.0475 | 489 | 0.007459 | 0.02238 | GOOD (significant) |
| small | M4a | accuracy | 450 | 0.00432 | 0.05911 | 1470 | 0.1218 | 0.1719 | good trend (n.s.) |
| large | M4a | client-drift E_drift | 450 | -0.008946 | 0.01444 | 21 | 1.287e-33 | 3.431e-33 | GOOD (significant) |
| medium | M4a | client-drift E_drift | 450 | -0.008349 | 0.01257 | 18 | 1.346e-37 | 1.077e-36 | GOOD (significant) |
| small | M4a | client-drift E_drift | 450 | -0.01248 | 0.02349 | 28 | 3.981e-26 | 5.028e-26 | GOOD (significant) |
| large | M4a | drift alignment S_CDA | 450 | 0.07617 | 0.06559 | 6 | 2.115e-85 | 5.075e-84 | GOOD (significant) |
| medium | M4a | drift alignment S_CDA | 450 | 0.08068 | 0.07083 | 7 | 2.93e-83 | 3.516e-82 | GOOD (significant) |
| small | M4a | drift alignment S_CDA | 450 | 0.07381 | 0.07577 | 9 | 3.59e-67 | 5.743e-67 | GOOD (significant) |
| large | M4ab | accuracy | 450 | 0.0009358 | 0.05225 | 2.446e+04 | 0.7042 | 0.7348 | good trend (n.s.) |
| medium | M4ab | accuracy | 450 | 0.005342 | 0.04678 | 602 | 0.01581 | 0.02829 | GOOD (significant) |
| small | M4ab | accuracy | 450 | 0.002558 | 0.06142 | 4525 | 0.3774 | 0.4313 | good trend (n.s.) |
| large | M4ab | client-drift E_drift | 450 | -0.009206 | 0.01534 | 22 | 6.302e-32 | 1.26e-31 | GOOD (significant) |
| medium | M4ab | client-drift E_drift | 450 | -0.008839 | 0.01341 | 19 | 3.757e-37 | 2.254e-36 | GOOD (significant) |
| small | M4ab | client-drift E_drift | 450 | -0.01301 | 0.02429 | 28 | 1.881e-26 | 2.655e-26 | GOOD (significant) |
| large | M4ab | drift alignment S_CDA | 450 | 0.06858 | 0.0686 | 8 | 1.187e-69 | 2.036e-69 | GOOD (significant) |
| medium | M4ab | drift alignment S_CDA | 450 | 0.07746 | 0.07227 | 7 | 1.064e-76 | 2.321e-76 | GOOD (significant) |
| small | M4ab | drift alignment S_CDA | 450 | 0.07301 | 0.07717 | 9 | 2.007e-64 | 2.676e-64 | GOOD (significant) |
| large | M5b | accuracy | 450 | 0.01562 | 0.044 | 63 | 2.812e-13 | 6.748e-12 | GOOD (significant) |
| medium | M5b | accuracy | 450 | 0.01186 | 0.04784 | 128 | 2.231e-07 | 1.785e-06 | GOOD (significant) |
| small | M5b | accuracy | 450 | 0.01567 | 0.04986 | 80 | 7.796e-11 | 9.355e-10 | GOOD (significant) |
| large | M5b | client-drift E_drift | 450 | -0.005919 | 0.0111 | 28 | 2.754e-26 | 3.672e-26 | GOOD (significant) |
| medium | M5b | client-drift E_drift | 450 | -0.005234 | 0.01045 | 32 | 1.094e-23 | 1.193e-23 | GOOD (significant) |
| small | M5b | client-drift E_drift | 450 | -0.007448 | 0.01207 | 21 | 2.204e-33 | 5.29e-33 | GOOD (significant) |
| large | M5b | drift alignment S_CDA | 450 | -0.004312 | 0.05587 | 1318 | 0.1023 | 0.1023 | bad trend (n.s.) |
| medium | M5b | drift alignment S_CDA | 450 | 0.005545 | 0.05086 | 661 | 0.0212 | 0.02212 | GOOD (significant) |
| small | M5b | drift alignment S_CDA | 450 | 0.0102 | 0.05813 | 255 | 0.000221 | 0.0002411 | GOOD (significant) |
| large | M3 | accuracy | 450 | 0.006035 | 0.05319 | 610 | 0.0165 | 0.02829 | GOOD (significant) |
| medium | M3 | accuracy | 450 | 0.006681 | 0.04725 | 393 | 0.002852 | 0.01204 | GOOD (significant) |
| small | M3 | accuracy | 450 | 0.00698 | 0.05995 | 579 | 0.01388 | 0.02776 | GOOD (significant) |
| large | M3 | client-drift E_drift | 450 | -0.007624 | 0.01322 | 24 | 6.584e-30 | 1.216e-29 | GOOD (significant) |
| medium | M3 | client-drift E_drift | 450 | -0.007166 | 0.01119 | 20 | 1.95e-35 | 7.8e-35 | GOOD (significant) |
| small | M3 | client-drift E_drift | 450 | -0.01136 | 0.02288 | 32 | 2.594e-23 | 2.594e-23 | GOOD (significant) |
| large | M3 | drift alignment S_CDA | 450 | 0.07087 | 0.06503 | 7 | 1.794e-78 | 4.305e-78 | GOOD (significant) |
| medium | M3 | drift alignment S_CDA | 450 | 0.07497 | 0.06755 | 7 | 2.041e-80 | 8.165e-80 | GOOD (significant) |
| small | M3 | drift alignment S_CDA | 450 | 0.06945 | 0.07356 | 9 | 3.1e-64 | 3.916e-64 | GOOD (significant) |
| large | M2 | accuracy | 450 | 0.0009642 | 0.05081 | 2.18e+04 | 0.6875 | 0.7348 | good trend (n.s.) |
| medium | M2 | accuracy | 450 | 0.007433 | 0.04824 | 331 | 0.001162 | 0.006973 | GOOD (significant) |
| small | M2 | accuracy | 450 | 0.003377 | 0.05814 | 2327 | 0.2186 | 0.2786 | good trend (n.s.) |
| large | M2 | client-drift E_drift | 450 | -0.007372 | 0.01285 | 24 | 1.222e-29 | 2.095e-29 | GOOD (significant) |
| medium | M2 | client-drift E_drift | 450 | -0.007333 | 0.01128 | 19 | 2.623e-36 | 1.259e-35 | GOOD (significant) |
| small | M2 | client-drift E_drift | 450 | -0.01146 | 0.02234 | 30 | 1.251e-24 | 1.43e-24 | GOOD (significant) |
| large | M2 | drift alignment S_CDA | 450 | 0.06439 | 0.05895 | 7 | 1.054e-78 | 3.162e-78 | GOOD (significant) |
| medium | M2 | drift alignment S_CDA | 450 | 0.06907 | 0.0618 | 7 | 3.61e-81 | 1.733e-80 | GOOD (significant) |
| small | M2 | drift alignment S_CDA | 450 | 0.0676 | 0.06674 | 8 | 6.055e-71 | 1.118e-70 | GOOD (significant) |
| large | CDQ | accuracy | 450 | 0.006881 | 0.04894 | 397 | 0.00301 | 0.01204 | GOOD (significant) |
| medium | CDQ | accuracy | 450 | 0.004126 | 0.05433 | 1362 | 0.1079 | 0.1618 | good trend (n.s.) |
| small | CDQ | accuracy | 450 | 0.002279 | 0.0525 | 4166 | 0.3577 | 0.4292 | good trend (n.s.) |
| large | CDQ | client-drift E_drift | 450 | -0.01547 | 0.02561 | 22 | 3.085e-32 | 6.732e-32 | GOOD (significant) |
| medium | CDQ | client-drift E_drift | 450 | -0.01653 | 0.02397 | 17 | 6.611e-40 | 1.587e-38 | GOOD (significant) |
| small | CDQ | client-drift E_drift | 450 | -0.02186 | 0.03227 | 18 | 8.604e-39 | 1.032e-37 | GOOD (significant) |
| large | CDQ | drift alignment S_CDA | 450 | 0.02817 | 0.04597 | 21 | 5.04e-33 | 5.761e-33 | GOOD (significant) |
| medium | CDQ | drift alignment S_CDA | 450 | 0.03787 | 0.04338 | 11 | 2.639e-57 | 3.167e-57 | GOOD (significant) |
| small | CDQ | drift alignment S_CDA | 450 | 0.05211 | 0.04606 | 7 | 1.709e-82 | 1.368e-81 | GOOD (significant) |

## table13 diagnostics

Paired comparison on the diagnostic metrics.

| scale | baseline | metric | n_pairs | mean_method | mean_baseline | gap | rel_change_pct | p | p_wilcoxon | q_BH | n_80pow | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| large | base | accuracy | 450 | 0.3754 | 0.369 | 0.006446 | 1.747 | 0.01146 | 0.009944 | 0.02751 | 549 | GOOD (significant) |
| medium | base | accuracy | 450 | 0.4066 | 0.4002 | 0.006449 | 1.612 | 0.004104 | 0.00164 | 0.01407 | 425 | GOOD (significant) |
| small | base | accuracy | 450 | 0.3996 | 0.3926 | 0.007017 | 1.787 | 0.01335 | 0.001084 | 0.02776 | 573 | GOOD (significant) |
| large | base | client-drift E_drift | 450 | 0.01288 | 0.02069 | -0.007807 | -37.74 | 8.862e-29 | 1.272e-55 | 1.418e-28 | 25 | GOOD (significant) |
| medium | base | client-drift E_drift | 450 | 0.01319 | 0.02049 | -0.007295 | -35.61 | 9.477e-35 | 9.32e-57 | 3.249e-34 | 20 | GOOD (significant) |
| small | base | client-drift E_drift | 450 | 0.01225 | 0.0238 | -0.01155 | -48.52 | 2.491e-23 | 1.103e-57 | 2.594e-23 | 32 | GOOD (significant) |
| large | base | drift alignment S_CDA | 450 | 0.3121 | 0.24 | 0.07208 | 30.03 | 1.286e-79 | 5.009e-65 | 4.408e-79 | 7 | GOOD (significant) |
| medium | base | drift alignment S_CDA | 450 | 0.3258 | 0.2501 | 0.07562 | 30.23 | 2.73e-81 | 4.822e-68 | 1.638e-80 | 7 | GOOD (significant) |
| small | base | drift alignment S_CDA | 450 | 0.351 | 0.2809 | 0.07003 | 24.93 | 1.857e-64 | 5.749e-61 | 2.622e-64 | 9 | GOOD (significant) |
| large | base | reconstruction error | 450 | 0.07855 | 0.1084 | -0.02988 | -27.56 | 5.634e-61 | 6.943e-71 | 1.127e-60 | 10 | GOOD (significant) |
| medium | base | reconstruction error | 450 | 0.08095 | 0.1108 | -0.02988 | -26.96 | 9.102e-70 | 8.759e-72 | 5.461e-69 | 8 | GOOD (significant) |
| small | base | reconstruction error | 450 | 0.08383 | 0.1189 | -0.03508 | -29.5 | 1.037e-48 | 1.369e-70 | 1.245e-48 | 13 | GOOD (significant) |
| large | base | active clients | 450 | 9.452 | 9.411 | 0.04118 | 0.4376 | 7.034e-22 | 1.214e-22 | 8.039e-22 | 35 | GOOD (significant) |
| medium | base | active clients | 450 | 9.471 | 9.411 | 0.06018 | 0.6395 | 4.213e-57 | 2.966e-46 | 1.011e-56 | 11 | GOOD (significant) |
| small | base | active clients | 450 | 9.468 | 9.411 | 0.05723 | 0.6082 | 1.825e-47 | 1.333e-40 | 3.129e-47 | 14 | GOOD (significant) |
| large | base | /g_hat///g*/ | 450 | 1.297 | 1.506 | -0.2096 | -13.91 | 1.101e-19 | 2.201e-15 | 1.322e-19 | 39 | n/a (diagnostic) |
| medium | base | /g_hat///g*/ | 450 | 1.253 | 1.459 | -0.2059 | -14.12 | 2.239e-24 | 9.095e-17 | 3.583e-24 | 31 | n/a (diagnostic) |
| small | base | /g_hat///g*/ | 450 | 1.182 | 1.384 | -0.2015 | -14.56 | 4.463e-28 | 2.298e-21 | 9.738e-28 | 26 | n/a (diagnostic) |
| large | base | Bad-tier weight share | 450 | 0.2825 | 0.3347 | -0.0522 | -15.59 | 3.913e-85 | 4.419e-53 | 1.043e-84 | 6 | n/a (diagnostic) |
| medium | base | Bad-tier weight share | 450 | 0.293 | 0.3347 | -0.04169 | -12.46 | 1.253e-86 | 1.879e-58 | 5.012e-86 | 6 | n/a (diagnostic) |
| small | base | Bad-tier weight share | 450 | 0.2904 | 0.3347 | -0.04427 | -13.23 | 6.87e-81 | 1.589e-52 | 1.178e-80 | 7 | n/a (diagnostic) |
| large | JEQFL | accuracy | 450 | 0.3754 | 0.3701 | 0.005356 | 1.447 | 0.03199 | 0.002756 | 0.05119 | 764 | good trend (n.s.) |
| medium | JEQFL | accuracy | 450 | 0.4066 | 0.4003 | 0.00632 | 1.579 | 0.008535 | 0.0008863 | 0.02276 | 507 | GOOD (significant) |
| small | JEQFL | accuracy | 450 | 0.3996 | 0.3994 | 0.0002309 | 0.0578 | 0.9369 | 0.3804 | 0.9369 | 5.636e+05 | good trend (n.s.) |
| large | JEQFL | client-drift E_drift | 450 | 0.01288 | 0.02048 | -0.007601 | -37.11 | 2.278e-28 | 5.107e-54 | 3.417e-28 | 26 | GOOD (significant) |
| medium | JEQFL | client-drift E_drift | 450 | 0.01319 | 0.02062 | -0.007432 | -36.04 | 4.788e-34 | 4.806e-59 | 1.436e-33 | 21 | GOOD (significant) |
| small | JEQFL | client-drift E_drift | 450 | 0.01225 | 0.02393 | -0.01168 | -48.8 | 2.866e-25 | 3.643e-59 | 3.44e-25 | 29 | GOOD (significant) |
| large | JEQFL | drift alignment S_CDA | 450 | 0.3121 | 0.2453 | 0.06675 | 27.21 | 5.278e-67 | 1.555e-57 | 7.916e-67 | 9 | GOOD (significant) |
| medium | JEQFL | drift alignment S_CDA | 450 | 0.3258 | 0.2509 | 0.07485 | 29.83 | 1.273e-78 | 8.064e-65 | 3.395e-78 | 7 | GOOD (significant) |
| small | JEQFL | drift alignment S_CDA | 450 | 0.351 | 0.2792 | 0.07171 | 25.68 | 1.409e-71 | 9.93e-64 | 2.819e-71 | 8 | GOOD (significant) |
| large | JEQFL | reconstruction error | 450 | 0.07855 | 0.1077 | -0.02918 | -27.08 | 7.169e-59 | 3.353e-69 | 1.229e-58 | 10 | GOOD (significant) |
| medium | JEQFL | reconstruction error | 450 | 0.08095 | 0.1108 | -0.02983 | -26.93 | 1.278e-66 | 7.504e-71 | 6.135e-66 | 9 | GOOD (significant) |
| small | JEQFL | reconstruction error | 450 | 0.08383 | 0.1196 | -0.03575 | -29.9 | 3.24e-51 | 2.84e-71 | 4.575e-51 | 12 | GOOD (significant) |
| large | JEQFL | active clients | 450 | 9.452 | 9.523 | -0.07128 | -0.7485 | 2.022e-44 | 1.854e-43 | 3.236e-44 | 15 | BAD (significant) |
| medium | JEQFL | active clients | 450 | 9.471 | 9.524 | -0.0533 | -0.5596 | 2.516e-43 | 1.444e-40 | 3.773e-43 | 15 | BAD (significant) |
| small | JEQFL | active clients | 450 | 9.468 | 9.522 | -0.05403 | -0.5674 | 6.176e-39 | 1.892e-38 | 8.719e-39 | 18 | BAD (significant) |
| large | JEQFL | /g_hat///g*/ | 450 | 1.297 | 1.492 | -0.1951 | -13.08 | 1.948e-18 | 5.208e-13 | 2.033e-18 | 43 | n/a (diagnostic) |
| medium | JEQFL | /g_hat///g*/ | 450 | 1.253 | 1.432 | -0.1797 | -12.54 | 8.235e-20 | 7.152e-12 | 1.04e-19 | 39 | n/a (diagnostic) |
| small | JEQFL | /g_hat///g*/ | 450 | 1.182 | 1.389 | -0.2067 | -14.88 | 1.025e-29 | 1.954e-22 | 2.46e-29 | 24 | n/a (diagnostic) |
| large | JEQFL | Bad-tier weight share | 450 | 0.2825 | 0.3341 | -0.05157 | -15.44 | 1.723e-83 | 3.319e-48 | 3.758e-83 | 7 | n/a (diagnostic) |
| medium | JEQFL | Bad-tier weight share | 450 | 0.293 | 0.3338 | -0.04081 | -12.22 | 1.06e-83 | 2.101e-53 | 2.544e-83 | 7 | n/a (diagnostic) |
| small | JEQFL | Bad-tier weight share | 450 | 0.2904 | 0.3337 | -0.0433 | -12.97 | 3.46e-78 | 1.073e-46 | 5.536e-78 | 7 | n/a (diagnostic) |
| large | M4a | accuracy | 450 | 0.3754 | 0.3723 | 0.003111 | 0.8356 | 0.2206 | 0.3245 | 0.2786 | 2347 | good trend (n.s.) |
| medium | M4a | accuracy | 450 | 0.4066 | 0.4006 | 0.006019 | 1.502 | 0.007459 | 0.0009252 | 0.02238 | 489 | GOOD (significant) |
| small | M4a | accuracy | 450 | 0.3996 | 0.3953 | 0.00432 | 1.093 | 0.1218 | 0.01879 | 0.1719 | 1470 | good trend (n.s.) |
| large | M4a | client-drift E_drift | 450 | 0.01288 | 0.02183 | -0.008946 | -40.99 | 1.287e-33 | 2.882e-58 | 3.431e-33 | 21 | GOOD (significant) |
| medium | M4a | client-drift E_drift | 450 | 0.01319 | 0.02154 | -0.008349 | -38.76 | 1.346e-37 | 7.919e-60 | 1.077e-36 | 18 | GOOD (significant) |
| small | M4a | client-drift E_drift | 450 | 0.01225 | 0.02473 | -0.01248 | -50.46 | 3.981e-26 | 9.734e-61 | 5.028e-26 | 28 | GOOD (significant) |
| large | M4a | drift alignment S_CDA | 450 | 0.3121 | 0.2359 | 0.07617 | 32.29 | 2.115e-85 | 1.222e-67 | 5.075e-84 | 6 | GOOD (significant) |
| medium | M4a | drift alignment S_CDA | 450 | 0.3258 | 0.2451 | 0.08068 | 32.92 | 2.93e-83 | 2.089e-69 | 3.516e-82 | 7 | GOOD (significant) |
| small | M4a | drift alignment S_CDA | 450 | 0.351 | 0.2771 | 0.07381 | 26.63 | 3.59e-67 | 4.556e-64 | 5.743e-67 | 9 | GOOD (significant) |
| large | M4a | reconstruction error | 450 | 0.07855 | 0.1117 | -0.03318 | -29.69 | 1.084e-65 | 3.381e-72 | 4.336e-65 | 9 | GOOD (significant) |
| medium | M4a | reconstruction error | 450 | 0.08095 | 0.1137 | -0.03279 | -28.83 | 2.496e-70 | 7.405e-73 | 2.995e-69 | 8 | GOOD (significant) |
| small | M4a | reconstruction error | 450 | 0.08383 | 0.1216 | -0.03772 | -31.03 | 4.996e-52 | 3.146e-72 | 7.494e-52 | 12 | GOOD (significant) |
| large | M4a | active clients | 450 | 9.452 | 9.411 | 0.04118 | 0.4376 | 7.034e-22 | 1.214e-22 | 8.039e-22 | 35 | GOOD (significant) |
| medium | M4a | active clients | 450 | 9.471 | 9.411 | 0.06018 | 0.6395 | 4.213e-57 | 2.966e-46 | 1.011e-56 | 11 | GOOD (significant) |
| small | M4a | active clients | 450 | 9.468 | 9.411 | 0.05723 | 0.6082 | 1.825e-47 | 1.333e-40 | 3.129e-47 | 14 | GOOD (significant) |
| large | M4a | /g_hat///g*/ | 450 | 1.297 | 1.503 | -0.2068 | -13.75 | 6.871e-21 | 1.526e-16 | 9.162e-21 | 37 | n/a (diagnostic) |
| medium | M4a | /g_hat///g*/ | 450 | 1.253 | 1.444 | -0.1907 | -13.21 | 1.809e-22 | 6.273e-15 | 2.554e-22 | 34 | n/a (diagnostic) |
| small | M4a | /g_hat///g*/ | 450 | 1.182 | 1.378 | -0.1959 | -14.22 | 7.505e-28 | 9.07e-21 | 1.501e-27 | 26 | n/a (diagnostic) |
| large | M4a | Bad-tier weight share | 450 | 0.2825 | 0.2843 | -0.001753 | -0.6169 | 9.28e-05 | 3.114e-06 | 0.0001012 | 228 | n/a (diagnostic) |
| medium | M4a | Bad-tier weight share | 450 | 0.293 | 0.2979 | -0.004867 | -1.634 | 8.747e-17 | 5.889e-15 | 1.105e-16 | 48 | n/a (diagnostic) |
| small | M4a | Bad-tier weight share | 450 | 0.2904 | 0.3038 | -0.01332 | -4.387 | 2.4e-61 | 1.902e-49 | 3.388e-61 | 10 | n/a (diagnostic) |
| large | M4ab | accuracy | 450 | 0.3754 | 0.3745 | 0.0009358 | 0.2499 | 0.7042 | 0.94 | 0.7348 | 2.446e+04 | good trend (n.s.) |
| medium | M4ab | accuracy | 450 | 0.4066 | 0.4013 | 0.005342 | 1.331 | 0.01581 | 0.002968 | 0.02829 | 602 | GOOD (significant) |
| small | M4ab | accuracy | 450 | 0.3996 | 0.3971 | 0.002558 | 0.6442 | 0.3774 | 0.09164 | 0.4313 | 4525 | good trend (n.s.) |
| large | M4ab | client-drift E_drift | 450 | 0.01288 | 0.02209 | -0.009206 | -41.68 | 6.302e-32 | 9.379e-55 | 1.26e-31 | 22 | GOOD (significant) |
| medium | M4ab | client-drift E_drift | 450 | 0.01319 | 0.02203 | -0.008839 | -40.12 | 3.757e-37 | 4.694e-59 | 2.254e-36 | 19 | GOOD (significant) |
| small | M4ab | client-drift E_drift | 450 | 0.01225 | 0.02526 | -0.01301 | -51.49 | 1.881e-26 | 1.213e-59 | 2.655e-26 | 28 | GOOD (significant) |
| large | M4ab | drift alignment S_CDA | 450 | 0.3121 | 0.2435 | 0.06858 | 28.16 | 1.187e-69 | 4.781e-60 | 2.036e-69 | 8 | GOOD (significant) |
| medium | M4ab | drift alignment S_CDA | 450 | 0.3258 | 0.2483 | 0.07746 | 31.2 | 1.064e-76 | 7.186e-68 | 2.321e-76 | 7 | GOOD (significant) |
| small | M4ab | drift alignment S_CDA | 450 | 0.351 | 0.2779 | 0.07301 | 26.27 | 2.007e-64 | 3.787e-63 | 2.676e-64 | 9 | GOOD (significant) |
| large | M4ab | reconstruction error | 450 | 0.07855 | 0.1112 | -0.03263 | -29.35 | 8.745e-60 | 3.669e-70 | 1.614e-59 | 10 | GOOD (significant) |
| medium | M4ab | reconstruction error | 450 | 0.08095 | 0.1142 | -0.03326 | -29.12 | 4.287e-65 | 2.017e-72 | 1.47e-64 | 9 | GOOD (significant) |
| small | M4ab | reconstruction error | 450 | 0.08383 | 0.1225 | -0.03865 | -31.56 | 9.206e-51 | 7.443e-72 | 1.227e-50 | 13 | GOOD (significant) |
| large | M4ab | active clients | 450 | 9.452 | 9.373 | 0.07864 | 0.839 | 7.782e-90 | 1.592e-64 | 3.735e-89 | 6 | GOOD (significant) |
| medium | M4ab | active clients | 450 | 9.471 | 9.395 | 0.0764 | 0.8132 | 6.426e-92 | 1.739e-64 | 3.856e-91 | 6 | GOOD (significant) |
| small | M4ab | active clients | 450 | 9.468 | 9.4 | 0.06779 | 0.7212 | 1.857e-70 | 3.032e-55 | 7.427e-70 | 8 | GOOD (significant) |
| large | M4ab | /g_hat///g*/ | 450 | 1.297 | 1.476 | -0.1791 | -12.14 | 4.893e-17 | 1.462e-10 | 4.893e-17 | 47 | n/a (diagnostic) |
| medium | M4ab | /g_hat///g*/ | 450 | 1.253 | 1.424 | -0.1712 | -12.02 | 5.204e-19 | 6.662e-12 | 5.947e-19 | 41 | n/a (diagnostic) |
| small | M4ab | /g_hat///g*/ | 450 | 1.182 | 1.373 | -0.191 | -13.91 | 5.707e-26 | 1.831e-17 | 9.783e-26 | 28 | n/a (diagnostic) |
| large | M4ab | Bad-tier weight share | 450 | 0.2825 | 0.2587 | 0.02384 | 9.216 | 3.246e-69 | 9.915e-54 | 4.869e-69 | 8 | n/a (diagnostic) |
| medium | M4ab | Bad-tier weight share | 450 | 0.293 | 0.278 | 0.01506 | 5.42 | 8.415e-45 | 4.897e-38 | 1.122e-44 | 15 | n/a (diagnostic) |
| small | M4ab | Bad-tier weight share | 450 | 0.2904 | 0.2866 | 0.003835 | 1.338 | 4.004e-14 | 2.486e-05 | 4.805e-14 | 58 | n/a (diagnostic) |
| large | M5b | accuracy | 450 | 0.3754 | 0.3598 | 0.01562 | 4.34 | 2.812e-13 | 2.002e-12 | 6.748e-12 | 63 | GOOD (significant) |
| medium | M5b | accuracy | 450 | 0.4066 | 0.3948 | 0.01186 | 3.005 | 2.231e-07 | 3.08e-08 | 1.785e-06 | 128 | GOOD (significant) |
| small | M5b | accuracy | 450 | 0.3996 | 0.384 | 0.01567 | 4.08 | 7.796e-11 | 3.702e-11 | 9.355e-10 | 80 | GOOD (significant) |
| large | M5b | client-drift E_drift | 450 | 0.01288 | 0.0188 | -0.005919 | -31.48 | 2.754e-26 | 4.516e-44 | 3.672e-26 | 28 | GOOD (significant) |
| medium | M5b | client-drift E_drift | 450 | 0.01319 | 0.01843 | -0.005234 | -28.41 | 1.094e-23 | 4.513e-42 | 1.193e-23 | 32 | GOOD (significant) |
| small | M5b | client-drift E_drift | 450 | 0.01225 | 0.0197 | -0.007448 | -37.81 | 2.204e-33 | 5.149e-56 | 5.29e-33 | 21 | GOOD (significant) |
| large | M5b | drift alignment S_CDA | 450 | 0.3121 | 0.3164 | -0.004312 | -1.363 | 0.1023 | 0.004014 | 0.1023 | 1318 | bad trend (n.s.) |
| medium | M5b | drift alignment S_CDA | 450 | 0.3258 | 0.3202 | 0.005545 | 1.732 | 0.0212 | 0.2474 | 0.02212 | 661 | GOOD (significant) |
| small | M5b | drift alignment S_CDA | 450 | 0.351 | 0.3408 | 0.0102 | 2.995 | 0.000221 | 0.008412 | 0.0002411 | 255 | GOOD (significant) |
| large | M5b | reconstruction error | 450 | 0.07855 | 0.08611 | -0.007553 | -8.772 | 3.484e-18 | 2.876e-15 | 3.484e-18 | 43 | GOOD (significant) |
| medium | M5b | reconstruction error | 450 | 0.08095 | 0.08968 | -0.008726 | -9.731 | 2.817e-21 | 3.656e-23 | 2.94e-21 | 36 | GOOD (significant) |
| small | M5b | reconstruction error | 450 | 0.08383 | 0.09741 | -0.01358 | -13.94 | 9.62e-37 | 2.209e-35 | 1.049e-36 | 19 | GOOD (significant) |
| large | M5b | active clients | 450 | 9.452 | 4.668 | 4.784 | 102.5 | 0 | 1.851e-75 | 0 | 1 | GOOD (significant) |
| medium | M5b | active clients | 450 | 9.471 | 4.668 | 4.803 | 102.9 | 0 | 1.852e-75 | 0 | 1 | GOOD (significant) |
| small | M5b | active clients | 450 | 9.468 | 4.668 | 4.8 | 102.8 | 0 | 1.852e-75 | 0 | 1 | GOOD (significant) |
| large | M5b | /g_hat///g*/ | 450 | 1.297 | 1.07 | 0.2267 | 21.19 | 1.806e-66 | 1.128e-56 | 2.167e-65 | 9 | n/a (diagnostic) |
| medium | M5b | /g_hat///g*/ | 450 | 1.253 | 1.083 | 0.1698 | 15.68 | 8.028e-60 | 1.033e-50 | 4.817e-59 | 10 | n/a (diagnostic) |
| small | M5b | /g_hat///g*/ | 450 | 1.182 | 1.048 | 0.1346 | 12.84 | 5.481e-52 | 1.697e-43 | 2.192e-51 | 12 | n/a (diagnostic) |
| large | M5b | Bad-tier weight share | 450 | 0.2825 | 0.3403 | -0.0578 | -16.98 | 5.086e-91 | 2.724e-63 | 6.103e-90 | 6 | n/a (diagnostic) |
| medium | M5b | Bad-tier weight share | 450 | 0.293 | 0.3403 | -0.04729 | -13.9 | 4.948e-93 | 2.268e-67 | 1.187e-91 | 6 | n/a (diagnostic) |
| small | M5b | Bad-tier weight share | 450 | 0.2904 | 0.3403 | -0.04987 | -14.66 | 1.611e-87 | 1.863e-62 | 1.289e-86 | 6 | n/a (diagnostic) |
| large | M3 | accuracy | 450 | 0.3754 | 0.3694 | 0.006035 | 1.634 | 0.0165 | 0.01283 | 0.02829 | 610 | GOOD (significant) |
| medium | M3 | accuracy | 450 | 0.4066 | 0.3999 | 0.006681 | 1.671 | 0.002852 | 0.0009559 | 0.01204 | 393 | GOOD (significant) |
| small | M3 | accuracy | 450 | 0.3996 | 0.3927 | 0.00698 | 1.778 | 0.01388 | 0.0007111 | 0.02776 | 579 | GOOD (significant) |
| large | M3 | client-drift E_drift | 450 | 0.01288 | 0.02051 | -0.007624 | -37.18 | 6.584e-30 | 1.163e-54 | 1.216e-29 | 24 | GOOD (significant) |
| medium | M3 | client-drift E_drift | 450 | 0.01319 | 0.02036 | -0.007166 | -35.2 | 1.95e-35 | 1.134e-56 | 7.8e-35 | 20 | GOOD (significant) |
| small | M3 | client-drift E_drift | 450 | 0.01225 | 0.02361 | -0.01136 | -48.1 | 2.594e-23 | 1.592e-57 | 2.594e-23 | 32 | GOOD (significant) |
| large | M3 | drift alignment S_CDA | 450 | 0.3121 | 0.2412 | 0.07087 | 29.38 | 1.794e-78 | 1.363e-64 | 4.305e-78 | 7 | GOOD (significant) |
| medium | M3 | drift alignment S_CDA | 450 | 0.3258 | 0.2508 | 0.07497 | 29.9 | 2.041e-80 | 1.352e-67 | 8.165e-80 | 7 | GOOD (significant) |
| small | M3 | drift alignment S_CDA | 450 | 0.351 | 0.2815 | 0.06945 | 24.67 | 3.1e-64 | 7.482e-61 | 3.916e-64 | 9 | GOOD (significant) |
| large | M3 | reconstruction error | 450 | 0.07855 | 0.108 | -0.02941 | -27.24 | 1.198e-61 | 1.517e-70 | 2.614e-61 | 10 | GOOD (significant) |
| medium | M3 | reconstruction error | 450 | 0.08095 | 0.1105 | -0.02957 | -26.75 | 4.313e-70 | 1.294e-71 | 3.451e-69 | 8 | GOOD (significant) |
| small | M3 | reconstruction error | 450 | 0.08383 | 0.1185 | -0.0347 | -29.28 | 6.908e-49 | 2.591e-70 | 8.726e-49 | 13 | GOOD (significant) |
| large | M3 | active clients | 450 | 9.452 | 9.411 | 0.04118 | 0.4376 | 7.034e-22 | 1.214e-22 | 8.039e-22 | 35 | GOOD (significant) |
| medium | M3 | active clients | 450 | 9.471 | 9.411 | 0.06018 | 0.6395 | 4.213e-57 | 2.966e-46 | 1.011e-56 | 11 | GOOD (significant) |
| small | M3 | active clients | 450 | 9.468 | 9.411 | 0.05723 | 0.6082 | 1.825e-47 | 1.333e-40 | 3.129e-47 | 14 | GOOD (significant) |
| large | M3 | /g_hat///g*/ | 450 | 1.297 | 1.501 | -0.2044 | -13.62 | 1.864e-18 | 4.299e-14 | 2.033e-18 | 43 | n/a (diagnostic) |
| medium | M3 | /g_hat///g*/ | 450 | 1.253 | 1.453 | -0.1998 | -13.76 | 2.8e-23 | 8.444e-16 | 4.2e-23 | 32 | n/a (diagnostic) |
| small | M3 | /g_hat///g*/ | 450 | 1.182 | 1.381 | -0.1984 | -14.37 | 4.483e-27 | 2.704e-20 | 8.277e-27 | 27 | n/a (diagnostic) |
| large | M3 | Bad-tier weight share | 450 | 0.2825 | 0.3347 | -0.0522 | -15.59 | 3.913e-85 | 4.419e-53 | 1.043e-84 | 6 | n/a (diagnostic) |
| medium | M3 | Bad-tier weight share | 450 | 0.293 | 0.3347 | -0.04169 | -12.46 | 1.253e-86 | 1.879e-58 | 5.012e-86 | 6 | n/a (diagnostic) |
| small | M3 | Bad-tier weight share | 450 | 0.2904 | 0.3347 | -0.04427 | -13.23 | 6.87e-81 | 1.589e-52 | 1.178e-80 | 7 | n/a (diagnostic) |
| large | M2 | accuracy | 450 | 0.3754 | 0.3745 | 0.0009642 | 0.2575 | 0.6875 | 0.535 | 0.7348 | 2.18e+04 | good trend (n.s.) |
| medium | M2 | accuracy | 450 | 0.4066 | 0.3992 | 0.007433 | 1.862 | 0.001162 | 0.0005438 | 0.006973 | 331 | GOOD (significant) |
| small | M2 | accuracy | 450 | 0.3996 | 0.3963 | 0.003377 | 0.8521 | 0.2186 | 0.004673 | 0.2786 | 2327 | good trend (n.s.) |
| large | M2 | client-drift E_drift | 450 | 0.01288 | 0.02025 | -0.007372 | -36.4 | 1.222e-29 | 1.601e-57 | 2.095e-29 | 24 | GOOD (significant) |
| medium | M2 | client-drift E_drift | 450 | 0.01319 | 0.02052 | -0.007333 | -35.73 | 2.623e-36 | 1.374e-59 | 1.259e-35 | 19 | GOOD (significant) |
| small | M2 | client-drift E_drift | 450 | 0.01225 | 0.02371 | -0.01146 | -48.32 | 1.251e-24 | 6.101e-62 | 1.43e-24 | 30 | GOOD (significant) |
| large | M2 | drift alignment S_CDA | 450 | 0.3121 | 0.2477 | 0.06439 | 26 | 1.054e-78 | 2.016e-62 | 3.162e-78 | 7 | GOOD (significant) |
| medium | M2 | drift alignment S_CDA | 450 | 0.3258 | 0.2567 | 0.06907 | 26.91 | 3.61e-81 | 1.726e-66 | 1.733e-80 | 7 | GOOD (significant) |
| small | M2 | drift alignment S_CDA | 450 | 0.351 | 0.2834 | 0.0676 | 23.86 | 6.055e-71 | 1.256e-62 | 1.118e-70 | 8 | GOOD (significant) |
| large | M2 | reconstruction error | 450 | 0.07855 | 0.1072 | -0.0286 | -26.69 | 1.316e-63 | 7.689e-72 | 3.51e-63 | 9 | GOOD (significant) |
| medium | M2 | reconstruction error | 450 | 0.08095 | 0.1107 | -0.02971 | -26.85 | 8.33e-77 | 2.082e-73 | 1.999e-75 | 7 | GOOD (significant) |
| small | M2 | reconstruction error | 450 | 0.08383 | 0.1186 | -0.03477 | -29.31 | 1.222e-52 | 5.886e-72 | 1.956e-52 | 12 | GOOD (significant) |
| large | M2 | active clients | 450 | 9.452 | 9.411 | 0.04118 | 0.4376 | 7.034e-22 | 1.214e-22 | 8.039e-22 | 35 | GOOD (significant) |
| medium | M2 | active clients | 450 | 9.471 | 9.411 | 0.06018 | 0.6395 | 4.213e-57 | 2.966e-46 | 1.011e-56 | 11 | GOOD (significant) |
| small | M2 | active clients | 450 | 9.468 | 9.411 | 0.05723 | 0.6082 | 1.825e-47 | 1.333e-40 | 3.129e-47 | 14 | GOOD (significant) |
| large | M2 | /g_hat///g*/ | 450 | 1.297 | 1.566 | -0.2696 | -17.21 | 1.648e-30 | 1.991e-31 | 4.396e-30 | 24 | n/a (diagnostic) |
| medium | M2 | /g_hat///g*/ | 450 | 1.253 | 1.513 | -0.2598 | -17.17 | 3.863e-38 | 7.106e-33 | 1.159e-37 | 18 | n/a (diagnostic) |
| small | M2 | /g_hat///g*/ | 450 | 1.182 | 1.427 | -0.2447 | -17.15 | 3.362e-41 | 1.445e-37 | 1.153e-40 | 16 | n/a (diagnostic) |
| large | M2 | Bad-tier weight share | 450 | 0.2825 | 0.3347 | -0.0522 | -15.59 | 3.913e-85 | 4.419e-53 | 1.043e-84 | 6 | n/a (diagnostic) |
| medium | M2 | Bad-tier weight share | 450 | 0.293 | 0.3347 | -0.04169 | -12.46 | 1.253e-86 | 1.879e-58 | 5.012e-86 | 6 | n/a (diagnostic) |
| small | M2 | Bad-tier weight share | 450 | 0.2904 | 0.3347 | -0.04427 | -13.23 | 6.87e-81 | 1.589e-52 | 1.178e-80 | 7 | n/a (diagnostic) |
| large | CDQ | accuracy | 450 | 0.3754 | 0.3685 | 0.006881 | 1.867 | 0.00301 | 5.572e-05 | 0.01204 | 397 | GOOD (significant) |
| medium | CDQ | accuracy | 450 | 0.4066 | 0.4025 | 0.004126 | 1.025 | 0.1079 | 0.2377 | 0.1618 | 1362 | good trend (n.s.) |
| small | CDQ | accuracy | 450 | 0.3996 | 0.3974 | 0.002279 | 0.5735 | 0.3577 | 0.65 | 0.4292 | 4166 | good trend (n.s.) |
| large | CDQ | client-drift E_drift | 450 | 0.01288 | 0.02835 | -0.01547 | -54.56 | 3.085e-32 | 4.096e-60 | 6.732e-32 | 22 | GOOD (significant) |
| medium | CDQ | client-drift E_drift | 450 | 0.01319 | 0.02972 | -0.01653 | -55.62 | 6.611e-40 | 1.436e-71 | 1.587e-38 | 17 | GOOD (significant) |
| small | CDQ | client-drift E_drift | 450 | 0.01225 | 0.03411 | -0.02186 | -64.08 | 8.604e-39 | 1.98e-74 | 1.032e-37 | 18 | GOOD (significant) |
| large | CDQ | drift alignment S_CDA | 450 | 0.3121 | 0.2839 | 0.02817 | 9.923 | 5.04e-33 | 1.379e-30 | 5.761e-33 | 21 | GOOD (significant) |
| medium | CDQ | drift alignment S_CDA | 450 | 0.3258 | 0.2879 | 0.03787 | 13.16 | 2.639e-57 | 8.567e-48 | 3.167e-57 | 11 | GOOD (significant) |
| small | CDQ | drift alignment S_CDA | 450 | 0.351 | 0.2989 | 0.05211 | 17.44 | 1.709e-82 | 9.075e-59 | 1.368e-81 | 7 | GOOD (significant) |
| large | CDQ | reconstruction error | 450 | 0.07855 | 0.1089 | -0.0303 | -27.84 | 2.33e-48 | 3.2e-59 | 2.663e-48 | 13 | GOOD (significant) |
| medium | CDQ | reconstruction error | 450 | 0.08095 | 0.1193 | -0.03831 | -32.12 | 1.261e-62 | 2.432e-74 | 3.027e-62 | 10 | GOOD (significant) |
| small | CDQ | reconstruction error | 450 | 0.08383 | 0.1315 | -0.04766 | -36.25 | 1.239e-63 | 1.02e-74 | 3.51e-63 | 9 | GOOD (significant) |
| large | CDQ | active clients | 450 | 9.452 | 9.452 | -0.0004506 | -0.004767 | 0.8054 | 0.8726 | 0.8054 | 5.813e+04 | bad trend (n.s.) |
| medium | CDQ | active clients | 450 | 9.471 | 9.47 | 0.0006296 | 0.006648 | 0.7394 | 0.7538 | 0.7715 | 3.187e+04 | good trend (n.s.) |
| small | CDQ | active clients | 450 | 9.468 | 9.467 | 0.0005926 | 0.006259 | 0.7244 | 0.711 | 0.7715 | 2.838e+04 | good trend (n.s.) |
| large | CDQ | /g_hat///g*/ | 450 | 1.297 | 1.713 | -0.4166 | -24.32 | 3.11e-55 | 9.672e-63 | 1.493e-54 | 11 | n/a (diagnostic) |
| medium | CDQ | /g_hat///g*/ | 450 | 1.253 | 1.619 | -0.3667 | -22.64 | 1.218e-61 | 6.658e-65 | 9.741e-61 | 10 | n/a (diagnostic) |
| small | CDQ | /g_hat///g*/ | 450 | 1.182 | 1.554 | -0.3722 | -23.94 | 1.819e-72 | 3.891e-73 | 4.365e-71 | 8 | n/a (diagnostic) |
| large | CDQ | Bad-tier weight share | 450 | 0.2825 | 0.2824 | 0.0001524 | 0.05397 | 0.2769 | 0.2219 | 0.2769 | 2980 | n/a (diagnostic) |
| medium | CDQ | Bad-tier weight share | 450 | 0.293 | 0.2927 | 0.0002854 | 0.09748 | 0.07224 | 0.1615 | 0.07538 | 1088 | n/a (diagnostic) |
| small | CDQ | Bad-tier weight share | 450 | 0.2904 | 0.2898 | 0.0006171 | 0.2129 | 2.704e-05 | 0.0001801 | 3.09e-05 | 197 | n/a (diagnostic) |

## Figures

| no | file | caption |
|---|---|---|
| 1 | figures/04_accuracy_curves_alpha100.png (.pdf) | Test accuracy versus federated round, per scale, arm and variant (alpha=100) |
| 2 | figures/04_accuracy_curves_alpha25.png (.pdf) | Test accuracy versus federated round, per scale, arm and variant (alpha=25) |
| 3 | figures/04_accuracy_curves_alpha50.png (.pdf) | Test accuracy versus federated round, per scale, arm and variant (alpha=50) |
| 4 | figures/04b_drift_curves_alpha100.png (.pdf) | Client drift E_drift versus round (alpha=100) |
| 5 | figures/04b_drift_curves_alpha25.png (.pdf) | Client drift E_drift versus round (alpha=25) |
| 6 | figures/04b_drift_curves_alpha50.png (.pdf) | Client drift E_drift versus round (alpha=50) |
| 7 | figures/20_00_metric_acc_tail.png (.pdf) | Final accuracy per scale, arm and variant |
| 8 | figures/20_02_metric_drift.png (.pdf) | Client drift E_drift per scale, arm and variant |
| 9 | figures/20_04_metric_scda.png (.pdf) | Drift alignment S_CDA per scale, arm and variant |
| 10 | figures/06_forest_accuracy.png (.pdf) | Paired effect on accuracy of CD-QFed against each baseline (95% intervals) |
| 11 | figures/06_forest_client-drift.png (.pdf) | Paired effect on client drift of CD-QFed against each baseline |
| 12 | figures/06_forest_drift.png (.pdf) | Paired effect on drift alignment S_CDA |
| 13 | figures/06c_forest_channel_accuracy.png (.pdf) | Paired effect on accuracy, split by channel quality |
| 14 | figures/06b_forest_arm_accuracy.png (.pdf) | Paired effect on accuracy, split by experimental arm |
| 15 | figures/08_ablation_lit.png (.pdf) | Per-innovation ablation anchored on CD-QFed |
| 16 | figures/11_shrinkage_ablation.png (.pdf) | Gauss-Markov orphan-shrinkage ablation |
| 17 | figures/12_trend_acc_tail_by_channel.png (.pdf) | Accuracy versus channel quality |
| 18 | figures/12b_trend_acc_tail_by_alpha.png (.pdf) | Accuracy versus data heterogeneity alpha |
| 19 | figures/12_trend_drift_by_channel.png (.pdf) | Client drift versus channel quality |
| 20 | figures/09_heatmap_acc_tail_vs_base.png (.pdf) | Accuracy gain over the baseline, per scale x arm x channel x alpha |
| 21 | figures/33_weight_matrix_runs.png (.pdf) | Effective aggregation weight per client and round (showcase runs) |
| 22 | figures/34_drift_memory_matrix.png (.pdf) | Fed-QDrift memory per client (showcase runs) |
| 23 | figures/00_acceptance_gates.png (.pdf) | Acceptance gates 1-9 |
| 24 | figures/13_power.png (.pdf) | Statistical power: observed effect against the number of pairs |
| 25 | figures/15_seed_spread_acc_tail.png (.pdf) | Accuracy spread across seeds |
| 26 | figures/16_paired_diff_acc_tail.png (.pdf) | Distribution of paired accuracy differences |
| 27 | figures/14_drift_vs_accuracy.png (.pdf) | Client drift against accuracy |

## Reproducibility

See `reproducibility.json` (configuration, hyper-parameters, compiles, lambda calibration, gates, software, hardware, SHA-256 of the results file).  Per-run raw data: `supplementary/results_cdqfed_paper_torchcuda.csv`.