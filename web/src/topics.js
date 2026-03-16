export const TOPIC_LIBRARY = [
  {
    field: "Distributed / Efficient LLM",
    topics: [
      "Tensor Parallelism vs Pipeline Parallelism vs MoE: đâu là chiến lược tối ưu để scale LLM lên hàng nghìn tỷ tham số?",
      "FlashAttention và các kỹ thuật IO-aware: liệu memory bandwidth có phải bottleneck thực sự của LLM inference?",
      "Quantization (INT4/INT8) vs Pruning vs Distillation: trade-off nào tốt nhất cho production deployment?",
      "Speculative Decoding có thực sự là tương lai của LLM inference hay chỉ là giải pháp tạm thời?",
    ],
  },
  {
    field: "LLM Training & Alignment",
    topics: [
      "RLHF vs DPO vs Constitutional AI: phương pháp alignment nào thực sự hiệu quả và scalable?",
      "Scaling Laws của Chinchilla có còn đúng với các mô hình GPT-4 scale trở lên không?",
      "Instruction tuning vs few-shot prompting: khi nào nên fine-tune, khi nào chỉ cần prompt?",
      "Catastrophic forgetting trong continual learning: đây có phải vấn đề cốt lõi chưa được giải quyết?",
    ],
  },
  {
    field: "AI Reasoning & Agents",
    topics: [
      "Chain-of-Thought prompting có thực sự tạo ra reasoning hay chỉ là pattern matching tinh vi?",
      "RAG vs Long Context vs Fine-tuning: chiến lược nào tối ưu cho knowledge-intensive tasks?",
      "LLM Agents có thể đạt được autonomous problem-solving hay luôn cần human-in-the-loop?",
      "Tool use và function calling: đây là bước tiến thực sự hay chỉ là duct tape cho LLM limitations?",
    ],
  },
  {
    field: "AI Safety & Ethics",
    topics: [
      "Interpretability research có thực sự giúp chúng ta hiểu LLM hay chỉ tạo ra illusion of understanding?",
      "AI Safety vs AI Capabilities: đây có phải trade-off thực sự hay có thể đạt được cả hai?",
      "Emergent abilities trong LLM: hiện tượng thực sự hay artifact của cách đo benchmark?",
      "Open-source LLM có nguy hiểm hơn closed-source về mặt safety không?",
    ],
  },
  {
    field: "Multimodal & Vision-Language",
    topics: [
      "Vision-Language Models: unified architecture hay modality-specific encoders — hướng nào sẽ thắng?",
      "Diffusion models vs Autoregressive models cho image generation: ai sẽ thống trị dài hạn?",
      "Video understanding trong LLM: bottleneck thực sự là compute, data hay architecture?",
    ],
  },
]
