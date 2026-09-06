# Context Folding: A Graph-Based Architecture for Infinite-Horizon AI Agent Memory

> **Research Briefing & Prototype Roadmap**
> Prepared for: Fable 5 (Anthropic)
> Researcher: Lucas Oliveira
> Date: July 2026

---

## 1. Executive Summary

This document presents the theoretical and architectural groundwork for a novel approach to AI agent memory management that we term **Context Folding**. The core insight is simple but powerful: instead of treating an LLM's context window as a linear buffer that fills and overflows, we model the agent's accumulated knowledge as a **continuously evolving, graph-based knowledge structure** that is dynamically folded and unfolded based on relevance, recency, and task-specific demands. A dedicated background agent - call it the **Context Manager** - is solely responsible for maintaining this graph, freeing the interaction agent to reason purely over the most relevant, surgically curated subset of its knowledge.

The hypothesis: **if context management is sufficiently intelligent and precise, the primary reasoning engine can be a significantly smaller, cheaper, and faster model without a loss in task performance.** This decoupling of reasoning power from memory scale is the central claim and the key impetus for this research.

---

## 2. The Problem: Context is a Finite Resource

Modern LLMs, despite having context windows of 200K to 1M tokens, remain fundamentally stateless. Every API call is independent; the application (e.g., Claude Code, Opencode) must re-send the entire conversation history. This leads to three critical problems:

### 2.1. Context Rot
As the number of tokens in the context window increases, the model's ability to accurately recall information from that context degrades. This is known as **"context rot" or "context poisoning."** The model's attention budget - its capacity to manage pairwise token relationships - becomes stretched thin as `n^2` relationships must be tracked for `n` tokens.

### 2.2. The "Append-Only" Fallacy
Accumulating raw experience (appending every message) is a poor approximation of learning. When humans learn, we create memories, but also **refine, consolidate, and compress them over time.** Append-only context captures none of this. It defers all representational work to inference time, forcing the model to re-process raw logs on every forward pass.

### 2.3. Economic and Latency Constraints
For a real-time coding agent, latency matters. Every extra token in the prompt increases time-to-first-token and cost. The dominant strategy today - sliding windows and periodic compaction - is a brute-force solution that loses information and provides no semantic understanding of what was lost.

---

## 3. The Vision: A Dual-Agent Architecture

We propose a fundamental architectural split:

```
+-------------------+      +-------------------------+
|  Agent 1:         |      |  Agent 2:               |
|  INTERACTION       |      |  CONTEXT MANAGER         |
|  (The "Brain")     |      |  (The "Librarian")       |
|                   |      |                         |
|  - Receives input |      |  - Manages the knowledge |
|  - Reasons over    | <-- |    graph                 |
|    curated context |      |  - Decides what to fold/ |
|  - Outputs response  |      |    unfold                |
|  - Blind to full   |      |  - Assigns tags/weights  |
|    graph           |      |  - Handles defragmentation|
|                   |      |  - Runs asynchronously   |
+-------------------+      +-------------------------+
         |                            |
         +----> [Graph DB / File DB] <----+
```

### 3.1. Agent 1: The Interaction Agent
This is the agent the user talks to. Its context window at any given moment contains:
- **Active Context:** The most recent, highly relevant conversation turns.
- **Folded Tags:** Lightweight identifiers (tags, file paths, query strings) representing dormant knowledge areas, not the knowledge itself.

It is **strictly blind** to the full graph. It only ever operates on what the Context Manager injects into its prompt.

### 3.2. Agent 2: The Context Manager
This is a background agent whose sole purpose is memory management. It operates continuously and asynchronously:
- **Placement:** When an Interaction Agent turn completes, the Manager takes the new information, classifies it, links it to existing graph nodes, and places it in the graph.
- **Tagging/Weighting:** It assigns semantic tags and recency/centrality weights to each node and edge.
- **Folding/Unfolding:** It decides which dormant nodes to surface (unfold) into the next prompt based on the user's incoming query and the current task state. It also decides what to fold away.
- **Defragmentation/Compaction:** Periodically, it restructures the graph to remove redundancy, merge duplicates, and create higher-level summary nodes, a process analogous to garbage collection or database reindexing.

### 3.3. The Knowledge Graph
The persistent memory is not a log or a vector DB, but a **weighted, directed graph**.
- **Nodes:** Can represent concepts, code files, conversation snippets, facts, or tasks.
- **Edges:** Represent semantic relationships ("is a part of", "depends on", "is related to", "contradicts").
- **Properties:** Each node has properties for content, summary, creation time, last access time, and access frequency.

---

## 4. Core Mechanisms: How It Works

### 4.1. Folding and Unfolding
- **Folding:** When a part of the conversation or a piece of knowledge is no longer actively relevant to the current task, the Context Manager replaces it in the Interaction Agent's prompt with a compact **tag** (e.g., `FOLDED: user-preferences`, `FOLDED: auth-module-design`). The full text is not lost; it is stored in the graph.
- **Unfolding:** Before the Interaction Agent processes a new user message, the Context Manager analyzes the user's intent, scans the graph for relevant dormant nodes, and dynamically injects their full text back into the prompt as active context.

### 4.2. Progressive Disclosure (Hierarchical Memory)
The graph supports hierarchical organization. A high-level node (e.g., "System Architecture") might have children for "Authentication", "Database", and "API". When the user asks about the database, the Manager might unfold the "Database" parent's summary and the most relevant children's full content, while leaving "Authentication" as a folded tag.

### 4.3. Defragmentation (Sleep-Time Compute)
Inspired by the concept of "sleep-time compute", the Context Manager can run background tasks during idle periods to:
- **Summarize:** Compress long chains of conversation into a single, dense summary node.
- **Re-organize:** Move information to a more logical location in the graph.
- **Identify Contradictions:** Find and flag nodes that hold contradictory information.
- **Create Abstractions:** Generate new higher-level concept nodes that link to multiple lower-level ones.

---

## 5. Why This Enables Smaller Models (The Core Hypothesis)

The central claim of this research is that **intelligent context curation is more valuable than raw model capacity** for complex, long-horizon tasks.

### 5.1. Precision over Power
A standard large model (e.g., Claude Opus, GPT-4) operating on a full, uncurated 200K token dump must use its massive capacity to perform two difficult tasks simultaneously:
1. **Filtering:** Figuring out which parts of the 200K tokens are relevant.
2. **Reasoning:** Solving the user's actual problem using that relevant information.

A Context Folding architecture decouples these tasks. The Context Manager, which can be a larger, slower, and more deliberate model, handles the heavy lifting of filtering and retrieval. The Interaction Agent, now operating on a much smaller, highly relevant, and precisely curated context window (e.g., 20K-50K tokens), can be a **smaller, faster, and cheaper model** (e.g., Kimi K2.5, GLM-5.2, or a distilled local model).

### 5.2. Recommended Model Tiering
Based on the Letta Model Leaderboard and general industry benchmarks, we propose the following model tiers for a Context Folding prototype:

| Agent Role | Recommended Model Tier | Rationale |
|---|---|---|
| **Interaction Agent** | **Efficient Frontier** (e.g., Kimi K2.5, Claude Haiku, GPT-4o-mini) | Must be fast and cheap for real-time interaction. Relies on curated context for accuracy. |
| **ContexteredFrontier** (e.g., Claude Sonnet, GPT-4o) | Needs strong comprehension to build and query the graph accurately. Can tolerate higher latency. |
| **Sleep-Time Agent** | **Deep Reasoning** (e.g., Claude Opus, o3-mini) | Runs asynchronously during idle time. Handles complex summarization, contradiction detection, and graph re-organization. |

---

## 6. State of the Art & Related Work

### 6.1. Letta / MemGPT (UC Berkeley)
The closest existing system. Letta (formerly MemGPT) introduces the concept of virtual context management and background "sleep-time" agents that rewrite their own memory. Their Context Repositories (Feb 2026) use a git-backed filesystem for memory.
- **Alignment:** They pioneered the dual-agent (primary + sleep-time) architecture and the concept of progressive disclosure.
- **Gap:** Their memory is file-based and hierarchical, not a true graph. Their background agent runs on a schedule, not per-prompt. The interaction agent is not fully blind to memory operations.

### 6.2. GraphRAG (Microsoft, Neo4j)
A system that builds a knowledge graph from a corpus and uses it for RAG (Retrieval-Augmented Generation).
- **Alignment:** Uses a graph structure for information retrieval.
- **Gap:** It is typically a static, read-only index built from a fixed corpus, not a continuously evolving memory system managed by a background agent.

### 6.3. Claude Code / Opencode
Current state-of-the-art coding agents.
- **Context Management:** Uses compaction (summarization at boundaries) and structured note-taking (e.g., `NOTES.md`).
- **Gap:** No persistent graph memory; no background context manager; context loss on session restart.

### 6.4. Anthropic Context Engineering (Sep 2025)
Anthropic advocates for "just-in-time" context strategies where agents use lightweight identifiers and tools to navigate and retrieve context at runtime.
- **Alignment:** Strongly supports the progressive disclosure model.
- **Gap:** Describes the philosophy but does not provide an architectural implementation for a formal graph or a dedicated background manager.

---

## 7. A Path to Prototype

### 7.1. Technology Stack
| Component | Technology |
|---|---|
| **Graph Database** | Neo4j, Memgraph, or ArangoDB |
| **Interaction Agent** | Claude Sonnet 4.6 or Kimi K2.5 (via API) |
| **Context Manager** | Claude Opus 4.6 (for reasoning) or GPT-4o |
| **Orchestration** | Python (LangGraph/LangChain) or Node.js (if building on Letta) |
| **Storage** | Graph DB for nodes/edges; Object storage (e.g., Redis, file system) for raw content |

### 7.2. Minimum Viable Prototype (MVP)
1. **Dual-Agent Loop:** Build a system with two LLM agents. One handles the user. The other receives the conversation log after every turn.
2. **Graph Ingestion:** The Context Manager parses the conversation and creates/updates a simple graph in Neo4j.
3. **Tag Injection:** The Manager passes a list of `FOLDED: tag` entries to the Interaction Agent.
4. **Unfold Trigger:** If the Interaction Agent's response contains a specific token (e.g., `UNFOLD: auth-module`), the Manager retrieves that node from the graph, injects its content into the prompt, and re-queries the Interaction Agent.
5. **Simple Defragmentation:** A nightly cron job (or a scheduled task) runs the Context Manager in "sleep mode" to summarize old nodes and merge duplicates.

### 7.3. Evaluation Metrics
- **Task Resolution:** Same coding tasks, same model, with and without Context Folding. Does the smaller model + folding beat the larger model + full context?
- **Latency:** Time to first token (TTFT) and total time for interaction agent to respond.
- **Cost:** Total token spend (Interaction + Context Manager + Sleep-Time).
- **Graph Quality:** Human evaluation of how well the graph captures the conversation's semantic structure.

---

## 8. References and Further Reading

### Foundational Papers and Articles
1. **Packer et al. (2023).** "MemGPT: Towards LLMs as Operating Systems." *arXiv:2310.08560*.
   - *Seminal work on virtual context management for LLMs.*
2. **Letta Research (2025).** "Continual Learning in Token Space." *Letta Blog*.
   - *Argues for learning through updates to context, not weights.*
3. **Anthropic Engineering (2025).** "Effective context engineering for AI agents." *Anthropic Blog*.
   - *Advocates for just-in-time retrieval and progressive disclosure.*
4. **Lin et al. (2025).** "Sleep-time compute: Beyond inference scaling at test-time." *arXiv:2504.13171*.
   - *Formalizes the concept of using idle time for background memory processing.*
5. **Cherny-Shahar & Yehudai (2026).** "Repository Intelligence Graph: Deterministic Architectural Map for LLM Code Assistants." *arXiv:2601.10112*.
   - *Proposes a graph-based approach for repository-level context, closely aligned with our vision.*
6. **Gloaguen et al. (2026).** "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" *arXiv:2602.11988*.
   - *Empirical evaluation of structured context files, relevant to folding logic.*

### Industry Projects and Tools
- **Letta Code:** github.com/letta-ai/letta-code
- **Letta Server:** github.com/letta-ai/letta
- **Neo4j Graph Database:** neo4j.com
- **LangGraph:** langchain-ai.github.io/langgraph/

---

## Appendix A: Separate Recommendation - Try Letta Code Now

Regardless of whether you decide to build a custom prototype, **I strongly recommend installing and experimenting with Letta Code.** It is the closest existing implementation of the dual-agent, sleep-time compute vision, and it is fully open-source.

### Why Try It Now:
- **Model Flexibility:** You can switch the primary agent's model to Kimi K2.5, a local model via Ollama, or any other supported provider.
- **Architecture Inspiration:** Observing how its sleep-time agent works will provide direct, practical insights for designing your own Context Manager.
- **Low Friction:** It is a single `npm` command to install and can run entirely locally.
- **Foundation for Prototype:** You can write a custom **Mod** (Letta's harness-level customization system) to intercept the context assembly pipeline and implement your graph-based logic on top of their existing infrastructure.

### Getting Started:
```bash
npm install -g @letta-ai/letta-code
letta --new-agent
```
Configure it to use Kimi K2.5 as the primary agent and Claude Opus as the sleep-time agent to directly test our model-tiering hypothesis.

---

*End of Report*
