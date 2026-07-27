# MEPF Framework Skeleton

This is a lightweight code framework for the paper:

**Beyond RAG-fake: Multi-Expert Pre-Verification and Planned Fact-Retrieval for Robust Multimodal Fake News Detection**

The structure follows the paper:

- Stage I: Multi-Expert Pre-Verification
  - Cross-modal semantic relevance evaluation
  - Visual media forensics analysis
  - Reliability gating and early exit
- Stage II: Planned Fact-Retrieval
  - Think-Act-Observe planning loop
  - Tool execution
  - Evidence-chain based final verdict
- Experiments
  - Evaluation
  - Ablation
  - Threshold sensitivity
  - Efficiency and cost analysis


Run the demo:

```bash
python mepf_framework/scripts/run_demo.py --input mepf_framework/examples/sample.json
```

The demo uses placeholder scores. Replace the predictor implementations in `mepf/stage1` and retrieval/reasoning implementations in `mepf/stage2` with the trained models and APIs from the original experiment code.
