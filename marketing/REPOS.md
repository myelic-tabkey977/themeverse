# 📣 Full Repo Marketing Playbook

Covers **all** repos on the account (50+), tiered by how marketable they actually are. Theme pack playbook stays in `MASTER.md` — this file is everything else.

---

## Tier 1 — ready to promote now (real README, real code, real audience)

### 1. prompt-vcs — *the strongest non-theme repo you own*
> Version control, A/B testing, and automatic rollback for LLM prompts.

**Why it can win:** every AI team with prompts in string literals has this exact pain. "git for prompts" is a pitch people instantly get. No dependency on any specific LLM vendor.

**X:**
```
git for LLM prompts.
Every prompt change becomes a commit. A/B test two prompts against a golden dataset, and auto-rollback when the new one regresses. No more "which prompt was serving user 4471 last Tuesday".
github.com/thanvish21/prompt-vcs
```

**Show HN:**
`Show HN: Prompt-VCS — version control, A/B testing and auto-rollback for LLM prompts`

**Where:** Show HN · r/LocalLLaMA · r/MachineLearning · HN "Ask" threads about prompt management · X AI engineering crowd. This is the repo to put real effort into — it's a tool, not a skin pack.

---

### 2. llm-judge-ci — *the CI-gate angle*
> Run LLM evaluations in CI and block merges when quality regresses.

**Pitch:** "CI for prompt quality." Same audience as prompt-vcs — they complement each other (cross-link them).

**X:**
```
Your prompts changed, your tests passed, but is the output actually better?
llm-judge-ci makes eval a first-class CI step: golden dataset → judge scores every answer → merge blocked on regression.
github.com/thanvish21/llm-judge-ci
```

**Where:** r/LocalLLaMA · r/ExperiencedDevs · HN · X #LLM #MLOps crowd.

---

### 3. local-toxic-block — *the safety angle*
> An offline guardrail for text entering or leaving an LLM. Detects leaked credentials, PII, prompt injection, and abuse — no model calls, no network, no state.

**Pitch:** "A guardrail that works without calling a model." This is a *security* product pitch — the audience is security engineers and anyone shipping LLM apps. Free alternative to paid guardrail services.

**X:**
```
Shipping an LLM app? You need a guardrail that doesn't cost an API call per message.
local-toxic-block: offline credential/PII/prompt-injection detection. No model. No network. No state.
github.com/thanvish21/local-toxic-block
```

**Where:** r/netsec · r/security · r/LocalLLaMA · X security crowd. Security people love open source they can audit.

---

### 4. gold-dominator (trading) — *niche but passionate audience*
> XAU/USD Gold Dominator Pro strategy + crypto arbitrage bot.

**Pitch:** Open-source trading strategies are *the* most-starred category of "money" repos, but also the most scrutinized. You must be squeaky clean about methodology.

**Where:** r/algotrading · r/forex · r/quant · X trading community · **with full backtest methodology + disclaimer, always.** Never promise returns, never post PnL without drawdown.

Draft in `twitter.md` (see the gold-dominator section there).

---

### 5. claude-config — *the credibility play*
> Claude Code skills, agents, workflows & MCP config.

**Pitch:** "Here's my whole Claude Code setup, open-sourced." The AI-coding-tool crowd (r/ClaudeAI, X, Discords) *loves* config dumps. It cross-promotes every other repo you own.

**X:**
```
Open-sourced my entire Claude Code setup: skills, agents, workflows, MCP servers.
It's the config behind the theme pack everyone starred — the part that makes the agent actually good.
github.com/thanvish21/claude-config
```

**Where:** r/ClaudeAI · X · Claude Code / OpenCode Discords (#configs channels).

---

## Tier 2 — portfolio content, market to recruiters (not to devs)

These are *credibility* repos. Nobody stars a RAG demo, but they fill a portfolio page beautifully. Market them on **LinkedIn + your portfolio + resume**, not Reddit.

| Repo | Hook for LinkedIn/portfolio |
|------|----------------------------|
| `retrieval-lab` | "RAG pipeline where chunking/retrieval/generation are driven by a CI-gated eval harness" |
| `rag-grounding-eval` | "Eval harness for grounding/hallucination — the thing everyone ships and nobody measures" |
| `semantic-chunk-ninja` | "Semantic chunking — chunk-quality eval for RAG" |
| `synthetic-user-sim` | "Simulated users to test recommendation/agent systems before going live" |
| `melody-match` | "Session-aware recommender with offline ranking metrics + simulated online A/B" |
| `azure-mlops-fraud` | "Real-time fraud scoring with champion/challenger promotion, drift monitoring, fairness audits" |
| `agent-memory-kv` | "Key-value memory for agents" |
| `llm-cost-guard` | "Cost control for LLM calls" |
| `mcp-postgres-inspector` | "Inspect Postgres through MCP" |
| `mcp-github-reviewer` | "Review PRs through MCP" |

**LinkedIn post template:**
```
Shipped [X] this week — [1-sentence what it does].
The part I'm proud of: [one non-obvious technical detail, e.g. "drift monitoring so the model doesn't silently rot"].
Open source: github.com/thanvish21/[repo]
#MLOps #LLM #RAG #backend
```

---

## Tier 3 — stubs, NOT ready to promote

These have no README, no description, or both. Posting them now = zero conversions and a bad look. **Fix before promoting:**

- Empty-ish: `plugin-test-generator-pro`, `plugin-performance-profiler`, `plugin-github-pr-reviewer`, `plugin-auto-debugger`, `plugin-architecture-mapper`, `synthetic-user-sim`, `semantic-chunk-ninja`, `rag-grounding-eval`, `mcp-postgres-inspector`, `mcp-github-reviewer`, `llm-cost-guard`, `agent-memory-kv`
- All the `ai-*` project repos (50+ AI projects monorepo is fine; each tiny repo is not)

**The 5-minute fix per repo (only for the ones worth keeping):**

```bash
gh repo edit thanvish21/<name> --description "<one line: what it does, who it's for>"
# then write a 20-line README: what, why, quick start, screenshot if visual
```

**Template README for a tier-3 repo:**
```markdown
# <Name>

<One sentence: what it does. One sentence: who it's for.>

## Why
<The pain it solves — one paragraph, specific.>

## Quick start
```bash
# install / run instructions, copy-pasteable
```

## How it works
<3-5 bullets, technical but short.>

## Status
<What works now, what's next. Honest beats polished.>
```

**The `ai-projects` monorepo** (50 AI/ML projects) is worth one LinkedIn/portfolio post by itself: *"50 AI projects — NLP, vision, generative AI — monorepo"*. Recruiters love volume; that's its audience.

---

## The one-file-per-repo template (for anything tier 1–2 you expand later)

Copy `REPO_TEMPLATE.md` beside this file, fill in, done.

---

## Cross-promotion strategy (the multiplier)

1. **Theme pack** (themeverse) is the front door → README "More from me" section linking `prompt-vcs`, `llm-judge-ci`, `claude-config`.
2. **claude-config** links everything (it's literally your config — mention the tools you built in it).
3. **prompt-vcs + llm-judge-ci** cross-link each other ("use both: prompt-vcs tracks, llm-judge-ci gates").
4. GitHub **profile README** (create `thanvish21/thanvish21`) with pins + one-line blurbs. This is the hub that makes every repo discovery feed the others.
5. Every repo's README gets a "More from me" footer pointing to the two best ones. One star → four repos discovered.

---

## Priority order (limited energy → best ROI)

1. `themeverse` (the flagship, kit in `MASTER.md`)
2. `prompt-vcs` (Show HN candidate — the highest-ceiling repo after the theme pack)
3. `llm-judge-ci` + `local-toxic-block` (same week, complementary)
4. `claude-config` (credibility, cheap)
5. `gold-dominator` (separate audience, careful with claims)
6. Tier-2 LinkedIn posts
7. Tier-3: README/description fixes before anything else
