# Concepts

1. [Large Language Model (LLM)](#large-language-model-llm)
2. [Tokenization](#tokenization)
3. [Vectors & Vectorization](#vectors--vectorization)
4. [Attention Mechanism](#attention-mechanism)
5. [Self-Supervised Learning](#self-supervised-learning)
6. [The Transformer](#the-transformer)
7. [Fine-Tuning](#fine-tuning)
8. [Few-Shot Prompting](#few-shot-prompting)
9. [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
10. [Vector Databases](#vector-databases)
11. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
12. [Context Engineering](#context-engineering)
13. [Context Summarization](#context-summarization)
14. [Agents](#agents)
15. [Reinforcement Learning with Human Feedback (RLHF)](#reinforcement-learning-with-human-feedback-rlhf)
16. [Chain of Thought (CoT)](#chain-of-thought-cot)
17. [Reasoning Models (Large Reasoning Models / LRMs)](#reasoning-models-large-reasoning-models--lrms)
18. [Multimodal Models](#multimodal-models)
19. [Small Language Models (SLMs) & Knowledge Distillation](#small-language-models-slms--knowledge-distillation)
20. [Quantization](#quantization)

### 1. Large Language Model (LLM)

A neural network trained specifically to predict the next token in an input sequence.

* **Example:** If you pass the input `"All that glitters"`, the model predicts and returns `"is not gold"`.

### 2. Tokenization

The process of breaking down raw input text into discrete pieces called **tokens** before feeding them into an LLM.

* Rather than breaking text purely by spaces, tokenization splits words into meaningful sub-words or suffixes (like parsing `"shimmers"`, `"murmurs"`, and `"flickers"` to recognize the common action suffix `"-ers"`, or identifying `"-ing"` in `"eating"`, `"dancing"`, and `"singing"`).
* This allows the model to process natural language structures efficiently and grasp grammatical mechanics.

### 3. Vectors & Vectorization

While tokens dictate *what* the model should focus on, **vectors** represent the underlying *meaning*.

* **Vectorization** is the process of mapping a token into a coordinate within an $N$-dimensional space.
* In this vector space, words with similar or related semantic meanings are clustered close together, while words with opposite meanings are placed far away.

### 4. Attention Mechanism

A breakthrough mechanism (popularized in 2017) that allows a model to look at surrounding words in a sentence to resolve ambiguity and establish context.

* **The Ambiguity Problem:** The word `"Apple"` has the exact same spelling across different contexts:
* *"A tasty apple"* $\rightarrow$ refers to the fruit.
* *"Apple's revenue"* $\rightarrow$ refers to the company.
* *"The apple of my eye"* $\rightarrow$ refers to an object of affection.


* **How it works:** The attention operation dynamically shifts a word's vector based on nearby contextual vectors. Performing an attention operation on `"Apple"` $+$ `"revenue"` pushes the resulting vector toward tech companies like Google, Meta, and Microsoft. Conversely, `"Apple"` $+$ `"tasty"` pushes it toward banana, chiku, and guava.

### 5. Self-Supervised Learning

A training methodology where data provides its own supervision, removing the need for expensive, human-labeled datasets.

* **The Concept:** A section of data is hidden, and the model must predict the missing piece based on the surrounding structure.
* **Text Example:** Given the sentence `"Et tu, Brutus"`, the system automatically generates parallel training puzzles behind the scenes without human intervention:
1. Input: `"Et"` $\rightarrow$ Target Output: `"tu"`
2. Input: `"Et tu"` $\rightarrow$ Target Output: `"Brutus"`
3. Input: `"Et tu, Brutus"` $\rightarrow$ Target Output: `"[STOP]"` or `","`


* If the model predicts incorrectly, it is penalized (increasing *loss*), and its internal neural network weights are updated. This method is incredibly scalable and is used across text, images (predicting hidden image patches), and video (predicting object movement).

### 6. The Transformer

Often confused with LLMs, the **Transformer** is not the final product—it is the specific engine/algorithm under the hood.

* An LLM is the "car," while the Transformer is the "engine."
* **Architecture:** Input tokens pass through an attention block to handle disambiguation, forward to a feedforward neural network, and repeat across stacked layers (anywhere from 12 to hundreds of layers).
* Each successive layer extracts more complex relationships, such as sarcasm, implications, or deeper inferences (e.g., inferring a crab is fearful when reading *"a crane was hunting a crab"*).
* *Note: The attention block scales at $O(N^2)$, meaning future LLMs could swap out Transformers for newer engine architectures like State Space Models or Diffusion architectures.*

### 7. Fine-Tuning

The process of taking a generic, self-supervised base model and training it further on specialized question-and-answer pairs to adjust how it outputs answers.

* **Why it matters:** A base model might look at a prompt like *"Who is the president of the USA?"* and give plausible but undesirable text-completion responses like *"I would like to know that too"*.
* Fine-tuning penalizes unwanted output styles and forces the model to follow a preferred format, speak in domain-specific jargon (such as medical or financial terms), or behave as a helpful customer support representative.

### 8. Few-Shot Prompting

An **inference-time** technique where you augment a plain user query by embedding illustrative examples directly inside the prompt before sending it to the LLM.

* **Example Structure:**


```

User Query: Where is my parcel?
[Example 1 Input]: Where is my order? -> [Example 1 Output]: Your order is on the way...
[Example 2 Input]: Track package -> [Example 2 Output]: Let me check that tracking ID...
Actual User Prompt: Where is my parcel?

```
* This acts as "example prompting," instantly increasing response quality in production without altering the underlying model weights.

### 9. Retrieval-Augmented Generation (RAG)
A system architecture that fetches real-time, external documentation relevant to a user's prompt and appends it to the LLM's context window during runtime.
* **Workflow:** When a customer triggers an API call, your server dynamically fetches up-to-date information (like company policies, flight schedules, or terms and conditions documents), combines it with the user's prompt and few-shot examples, and hands the complete package to the LLM. 
* This allows the model to produce highly accurate, context-aware responses without relying entirely on its static training weights.

### 10. Vector Databases
A highly specialized database used to store and quickly retrieve context documents for RAG systems using similarity searches.
* **The Problem:** A user submits a query: *"I am upset with your payment system. I expect a refund."* Traditional keyword search looks for the word "upset," which might not exist in your formal corporate policies.
* **The Vector Solution:** Because vectors store semantic meaning, the coordinate distance between the token `"upset"` and documents mentioning `"low rating"` or `"user drop off"` is very small. The vector database performs a spatial distance calculation (using algorithms like *Hierarchical Navigable Small World / HNSW*) to rapidly find and extract these contextually relevant documents.

### 11. Model Context Protocol (MCP)
An open standard/protocol that acts as an intelligent client-server wrapper, enabling an LLM to dynamically connect to and read from external databases or run third-party tools.
* **Workflow Example:**
  1. A user asks to book a flight.
  2. The LLM tells the **MCP Client** it needs flight availability information.
  3. The MCP Client hits external, native **MCP Servers** hosted by various entities (e.g., Air India's database wrapper and Indigo's database wrapper).
  4. The real-time flight data is returned to the client and fed back to the LLM as fresh context.
  5. The LLM decides on a flight path (e.g., *"Book Indigo 1020"*), which triggers a follow-up API call via the MCP server to execute the real-world booking.

### 12. Context Engineering
An umbrella discipline for engineers that encompasses managing, preparing, and dynamically optimizing the text context injected into a model. This includes combining few-shot prompts, pulling live files via RAG, handling external MCP server workflows, and preserving user preferences over time.

### 13. Context Summarization
A core component of context engineering designed to keep context windows lean and reduce costly API usage. 
* Techniques include using a **sliding window** where only the last 100 chat turns are sent raw to the LLM, while the older historical interactions are condensed into a neat 5-sentence summary.
* Engineers often use cheaper, distilled small language models to summarize incoming documents or histories first, passing only the optimized summaries into the expensive, flagship LLM.

### 14. Agents
An autonomous, long-running server process capable of breaking down complex user goals, executing multi-turn workflows, and coordinating actions independently.
* An agent can query an LLM for planning, connect to external systems, and talk to other agents to satisfy a user request.
* **Example:** A smart travel agent monitoring flight prices across a week. The moment it detects a drop in fare matching your explicit preferences, it automatically triggers an API call to purchase the ticket and updates your calendar.

### 15. Reinforcement Learning with Human Feedback (RLHF)
A training technique that optimizes a model’s generation pathways based on human ratings, scoring paths with positive ($+1$) or negative ($-1$) values.
* **The Process:** When an LLM generates two alternative responses for a single query, a human selects the better option. The path taken to generate the winning response gets a $+1$ across its vector token sequences, while the bad path gets a $-1$.
* Over thousands of iterations, this maps a complex terrain of rewards, training the model to prioritize paths that result in peak user satisfaction (similar to biological conditioning like *Pavlov's Dog*).

> ⚠️ **Limitation of RLHF:** Reinforcement learning optimizes based on statistical patterns and historic outcomes, but it **cannot construct true mental or physical models**. 
> For example, if you flip a perfectly fair coin and it lands on *Heads* six times in a row, an RL system might over-index on predicting *Heads* because it was heavily reinforced by outcomes. A human utilizes a mental understanding of probability and physics to know that the next flip still remains a strict $50/50$ split.

### 16. Chain of Thought (CoT)
A prompting and training technique where a model is explicitly trained to write out its step-by-step reasoning and logical deductions before spitting out a final answer. By breaking a problem down sequentially, the model drastically minimizes calculation errors and delivers much more robust answers.

### 17. Reasoning Models (Large Reasoning Models / LRMs)
Newer, state-of-the-art architectures (such as OpenAI's $o1$/$o3$ series or DeepSeek) capable of native problem-solving and algorithmic reasoning. 
* Rather than providing a flat, immediate response, these models adjust their compute time based on difficulty—running more inference steps for hard, multi-variable logic puzzles and fewer steps for straightforward queries.

### 18. Multimodal Models
Models engineered to simultaneously process, map, and generate multiple modes of data beyond raw text, including images, audio, and video assets.
* **Engineering Advantage:** Training a model natively on text *and* images actually increases its overall linguistic performance. Showing a model what a cat physically looks like reinforces its structural understanding of textual tokens like `"cat"` and `"feline"`.

### 19. Small Language Models (SLMs) & Knowledge Distillation
To lower operational infrastructure costs and achieve data privacy, the industry is shifting toward smaller, company-specific or task-specific models.
* **Parameter Scale Comparison:**
  * **LLM:** 3 Billion to 300+ Billion parameters.
  * **SLM:** 3 Million to 300 Million parameters.
* **Knowledge Distillation:** The primary method for building highly accurate SLMs. A large "Teacher LLM" and a small "Student SLM" are fed the same inputs simultaneously. The student model tries to mimic the teacher's exact distribution output. If it misses, its weights are iteratively adjusted. This packs complex, foundational information into a hyper-condensed footprint that is cheaper to host and incredibly fast at runtime.

### 20. Quantization
A post-training production compression technique that optimizes an existing model's mathematical weights to shrink its memory footprint.
* **How it works:** The floating-point numbers representing model weights are converted from high-precision formats (like 32-bit values) down to lower-precision formats (like 8-bit values). 
* This can save upwards of 75% of your system memory requirements during inference time, significantly reducing the hardware cost of running AI models in a production environment.

***

```