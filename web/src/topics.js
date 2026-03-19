export const TOPIC_LIBRARY = [
  {
    field: "Distributed / Efficient LLM",
    topics: [
      "Tensor Parallelism vs Pipeline Parallelism vs MoE: what is the best strategy to scale LLMs to trillions of parameters?",
      "FlashAttention and IO-aware techniques: is memory bandwidth truly the bottleneck for LLM inference?",
      "Quantization (INT4/INT8) vs Pruning vs Distillation: which trade-off is best for production deployment?",
      "Is speculative decoding the future of LLM inference, or just a temporary workaround?",
    ],
  },
  {
    field: "LLM Training & Alignment",
    topics: [
      "RLHF vs DPO vs Constitutional AI: which alignment approach is truly effective and scalable?",
      "Do Chinchilla-style scaling laws still hold for GPT-4-scale and beyond?",
      "Instruction tuning vs few-shot prompting: when should you fine-tune vs just prompt?",
      "Catastrophic forgetting in continual learning: is this still an unsolved core problem?",
    ],
  },
  {
    field: "AI Reasoning & Agents",
    topics: [
      "Does chain-of-thought prompting produce real reasoning, or just sophisticated pattern matching?",
      "RAG vs Long Context vs Fine-tuning: which strategy is best for knowledge-intensive tasks?",
      "Can LLM agents achieve autonomous problem-solving, or will they always need humans-in-the-loop?",
      "Tool use and function calling: genuine progress, or duct tape for LLM limitations?",
    ],
  },
  {
    field: "AI Safety & Ethics",
    topics: [
      "Does interpretability research help us understand LLMs, or create an illusion of understanding?",
      "AI Safety vs AI Capabilities: a real trade-off, or can we achieve both?",
      "Emergent abilities in LLMs: a real phenomenon, or a benchmark measurement artifact?",
      "Are open-source LLMs riskier than closed-source models from a safety perspective?",
    ],
  },
  {
    field: "Multimodal & Vision-Language",
    topics: [
      "Vision-language models: unified architectures vs modality-specific encoders — which will win?",
      "Diffusion vs autoregressive models for image generation: which will dominate long-term?",
      "Video understanding with LLMs: is the real bottleneck compute, data, or architecture?",
    ],
  },
]
