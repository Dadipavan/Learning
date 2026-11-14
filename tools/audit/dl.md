# Audit: study/dl (Deep Learning)

## Verdict
A strong, unusually hands-on document. It covers the full skill map for the ai domain (perceptron to diffusion, ONNX, DDP). It is built on real computed outputs with a steps-table-per-problem pattern. Beginner clarity is good through ch01-ch04 and ch06. Weaknesses:
- Modern-LLM-era "expert" topics (FlashAttention, GQA, MoE, KV-cache math, LoRA, RLHF/DPO pointers, torch.compile, FSDP) are one-paragraph awareness items with no worked example.
- ch05 and ch10 have no figures, and ch05 plus most PyTorch code is "not run here".
- Practice sets are short (about 5-8 items, 1 details block each). Ch15/16 projects have zero worked problems, and the appendix is answers only.
- The ch08 classic OpenCV chapter is long (9.3k words) with 0 figures despite being visual.
- Interpretability (Grad-CAM, saliency) is absent.
- Several concepts get only 1-2 worked examples, not 3 varied ones.

Counts come from regex. "problem" counts class="problem" elements, and each has a steps table. Figures counts svg/img/figure. Practice sets were read for ch03, ch05 and ch11.

## Per-chapter table
| Ch | Topic | Words | h2 | Problems | Code | Figures | Beginner | Expert |
|---|---|---|---|---|---|---|---|---|
| 01 | Perceptron, MLP, activations | 4592 | 6 | 7 | 19 | 6 | 5 | 2 |
| 02 | Forward/backprop, NumPy net | 5439 | 7 | 9 | 24 | 4 | 5 | 3 |
| 03 | Loss, optimizers, init/norm, regularization | 5501 | 7 | 11 | 19 | 2 | 4 | 3 |
| 04 | Debugging training | 4633 | 6 | 8 | 14 | 4 | 4 | 3 |
| 05 | PyTorch | 4751 | 6 | 7 | 20 | 0 | 4 | 3 |
| 06 | CNNs | 5981 | 7 | 13 | 27 | 2 | 5 | 3 |
| 07 | Transfer learning, augmentation | 5464 | 6 | 5 | 13 | 2 | 4 | 3 |
| 08 | Classical vision (OpenCV) | 9329 | 8 | 13 | 37 | 0 | 4 | 3 |
| 09 | Detection, segmentation, OCR | 8909 | 8 | 11 | 27 | 2 | 4 | 3 |
| 10 | RNN/LSTM/seq2seq/attention | 8528 | 7 | 8 | 29 | 2 | 4 | 3 |
| 11 | Transformers | 7369 | 8 | 10 | 22 | 4 | 4 | 3 |
| 12 | ViT, SSL, CLIP | 5791 | 7 | 9 | 22 | 4 | 4 | 3 |
| 13 | AE, VAE, GAN, diffusion | 6946 | 7 | 9 | 23 | 4 | 4 | 3 |
| 14 | Quantization, pruning, deploy, distributed, capstones, interview | 7826 | 9 | 8 | 23 | 2 | 3 | 3 |
| 15 | Projects A | 5811 | 6 | 0 | 17 | 0 | 3 | 3 |
| 16 | Projects B | 6271 | 6 | 0 | 20 | 0 | 3 | 3 |
| App | Answers | 1793 | 11 | 0 | 0 | 0 | n/a | n/a |

## Top 12 gaps (by learner value)
1. **Ch11, LLM-efficiency worked examples (about 1200 words).** Worked KV-cache memory calculator: 2 x layers x heads x d_h x T x bytes for a 7B model. Add a FlashAttention tiling and online-softmax example (compute softmax in blocks by hand, show it equals the full result). Add GQA and MoE parameter and FLOP counts (8 experts, top-2 routing, active vs total params). These are currently a single paragraph.
2. **New section after ch07 or ch11, LoRA/QLoRA/PEFT (about 1500 words).** Derive the low-rank update W + (alpha/r)BA. Count trainable parameters for rank 8 on a 4096x4096 layer (65k vs 16.7M). Add a NumPy merge check and a PEFT code example. Link to the genai docs.
3. **Ch14 or new chapter, Post-training and alignment bridge (about 1200 words).** SFT, reward model, a worked DPO loss on one preference pair with numbers, and PPO vs DPO. Currently pointer-only.
4. **Ch05, PyTorch run-ability and depth (about 1000 words).** Add a verified figure of the training loop and autograd graph. Add worked torch.compile, DDP and FSDP memory (ZeRO stage 1/2/3 bytes per parameter), a profiler example, and checkpoint/resume. Add a Colab-ready notebook link, since nothing PyTorch ran locally.
5. **Ch03, normalization and optimizers (about 1200 words).** RMSNorm, GroupNorm and BatchNorm vs LayerNorm are mentioned only briefly. Add a numeric comparison on one tensor (3 norms, same input), the AdamW vs L2 decoupled-decay example, warmup plus cosine schedule by hand, and label smoothing worked (three varied examples each).
6. **Ch13, diffusion depth (about 1500 words).** Derive the closed-form forward x_t = sqrt(abar) x0 + sqrt(1-abar) eps with a numeric example. Add a worked classifier-free guidance combination (eps_u + w(eps_c - eps_u)). Add latent diffusion shape and compression math (512x512x3 to 64x64x4), DDIM vs DDPM step counts, and a noise-schedule plot. Also add WGAN and mode collapse examples.
7. **Ch09, modern detection and segmentation (about 1000 words).** DETR Hungarian matching on a 3x3 cost matrix, anchor-free heads (FCOS/YOLOv8) and the decode math, a Mask R-CNN ROIAlign example, and a SAM prompt-flow figure. Add mAP@[.5:.95] with 3 images and a COCO evaluation code sample.
8. **Missing interpretability (new 4.4 or 6.5, about 1200 words).** Saliency, Grad-CAM (worked on a tiny CNN), integrated gradients, attention-visualisation pitfalls and probing. Also add calibration (ECE, temperature scaling) as a worked example.
9. **Ch15 and ch16, projects need rubrics and worked checkpoints (about 1500 words total).** They have 0 worked problems. Add expected metric ranges, a debugging log from a failed run, and an evaluation checklist. Add a small worked error analysis (confusion matrix, top-loss samples).
10. **Ch10, sequence-model visuals and state-space models (about 800 words).** Ch10 has two figures for 8.5k words. Add an unrolled RNN/LSTM gate diagram, a beam-search tree figure and a worked beam-search example (width 2). Expand Mamba/SSM from one sentence to a recurrence (h_t = A h_{t-1} + B x_t) example.
11. **Ch07, transfer learning variety (about 800 words).** It has only 5 worked problems. Add learning-rate discrimination per layer group, a feature-extraction vs fine-tune accuracy comparison, mixup/cutmix/RandAugment worked examples, handling class imbalance and domain shift, and a few-shot or linear-probe example.
12. **Practice sets and visuals across the document (about 3000 words).** Expand each practice set to 10-12 items (easy to hard, including debugging and "what is the output" items). Add figures for ch05, ch08 (filters and edge maps), ch15 and ch16. Add 3 varied examples to under-served concepts (ch04 loss spikes, ch12 SSL: MAE masking arithmetic, DINO, SimCLR augmentations).

Total recommended additions: 12 (about 16,700 words).

## Errors and issues found
No hard technical errors found in the spot-checked formulas. Checked: Xavier/He variance, DDPM reverse step, VAE KL, CLIP InfoNCE, 16 bytes per parameter (7B = 112 GB), YOLOv1 output 1470, momentum v update. These are correct. Items to fix or verify:
- ch03 Xavier is given as "variance 1/fan_in (or 2/(fan_in+fan_out))". The first form is the LeCun form. Label it as such, since Glorot proper is the second.
- ch05 and others: many PyTorch snippets are marked "not run here" (ch05 has 9, ch08 has 11). That is honest, but it means the PyTorch code is unverified. Consider running it in an environment with torch.
- ch09: YOLO is explained through YOLOv1 and a one-line mention of v3 onward and YOLOv8. Update to current Ultralytics generations (v11 and later) and anchor-free heads. Avoid "widely used" wording that will date.
- ch10: Mamba is "awareness only". Fine, but it needs a version-dated caveat.
- ch11: FlashAttention, GQA and MoE are listed in the intro and prompt pack as covered topics but have only one paragraph. The claims of coverage are overstated.
- ch14: the FSDP/LoRA memory answer is one line ("reduce with sharding, LoRA..."). It should be a worked calculation.
- ch15 and ch16 are labelled as chapters but contain no worked problems or answers, which breaks the pattern used elsewhere.
- Appendix is answers only, with 0 code or figures. Consider a glossary, a formula cheat sheet and a topic-to-skill-map crosswalk.
- Skill-map check (domain "ai"): all listed DL items map to a chapter, except the ones in gaps 2, 3 and 8 (LoRA/QLoRA, SFT/RLHF/DPO, interpretability/calibration). Normalizing flows are covered at awareness level only.
