# AI Literacy Tutorial: Glossary

*AI Integration Committee · Fall 2026 · Slides: aquastar.github.io/ai-literacy-faculty*

## The model

- **LLM (large language model):** a machine-learning model trained on next-token-prediction. The core tech supporting the current "AI" trend.
- **Transformer / attention:** the 2017 neural network architecture innovation behind nearly every LLM (the T in GPT).
- **Token:** a chunk of text mapped to an integer id, then to a vector which is processed by the LLM. LLMs consume and produce tokens, not strings.
- **Autoregressive / next-token prediction:** how LLMs are used to *generate* text. Predict the next token, append it, repeat.
- **Context / context window:** the string the model is continuing, and the most tokens it can hold at once.
- **Prompt engineering:** arranging the text (including a hidden **system prompt**) so the continuation you want is the most likely one.
- **Chain of thought / reasoning model:** writing out steps before answering. Reasoning models do it on their own, hidden from the user.
- **Multi-modal models:** models that process not just text tokens but also audio tokens or image tokens. These models can do things like (attempt to) answer a qustion about the contents of an image.

## Training

- **Weights / parameters:** the parameters of the LLM itself that are pre-trained on lots and lots and lots of data.
- **Pretraining:** predicting the next token over a huge corpus. The bulk of the model's "knowledge" is baked in here.
- **Supervised fine-tuning (SFT):** further training on example conversations to teach the LLM to produce tokens complying to the chat format.
- **RLHF:** Reinforcement Learning from Human Feedback. Further refine the weights of the LLM to produce things that humans seem to like. (A cause of **sycophancy**).
- **RLVR:** Reinforcement Learning with Verifiable Rewards. An automatic checker (unit tests, a math answer) supplies the reward. This is how models get super-human abilities in math and code.

## Other terms to know

- **Hallucination:** fluent, confident output that is false. Happens because models output one token at a time without backtracking or checking. All "knowledge" the model has is implicit in its weights.
- **Reward hacking:** a term from reinforcement learning where an agent gets the prize but not in the intended way. Here, Agents satisfy the checker instead of the intent, e.g. editing the tests or hacking HuggingFace for an answer-key.
- **Prompt injection:** instructions hidden in content the agent reads (a web page, an email, a student's file).

## Software around the LLMs

- **Harness:** the ordinary program around the model. Builds the context with simple string-substitution and pattern-matching. Calls the LLM's generative capabilities in a loop as a subroutine.
- **Tool call:** the model writes a request for a named function as text, and the harness detects this and actually runs it. Includes things like searching the web, executing a shell command, reading a file, writing a file, inspecting an image, etc.
- **Agent:** a model and a harness in a loop of think → tool → result, until the model "decides" it is done.
- **RAG (retrieval-augmented generation):** a special kind of tool call that searches documents for relevant passages and paste them into the context. Often a **semantic search** that queries documents based on their semantic closeness to the current context.
- **MCP (Model Context Protocol):** a standard for publishing tools: APIs documented in plain English for the model, usable by any harness.
- **Instruction file / skill:** `CLAUDE.md`, `AGENTS.md`, `SKILL.md`. Markdown files that (some) harnesses know to look for. They steer an agent by adding file contents to the context. It's all prompt-engineering; these files can only suggest a behavior or if/then protocol, not enforce it.
- **Sub-agent:** another model instance with a fresh context, delegated by some other agent.
