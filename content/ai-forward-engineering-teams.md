# Building a Small AI-Forward Engineering Team

**Lighthouse teams, evidence, and an engineering operating system**

Research date: **November 6, 2026**. Intended audience: founders, CTOs, and engineering leads building or upgrading a team of roughly **3-8 engineers**.

**Adversarial revision:** the initial synthesis was challenged against ten additional sources, including contrary empirical findings and a negative operating case. The largest changes concern instruction files, staffing, platform investment, review, maintainability, and the difference between producing code and creating customer value. See the [adversarial evidence review](#36-counterevidence-that-changes-the-recommendations), [assumption ledger](#37-adversarial-assumption-ledger), and [revised operating recommendation](#20-final-recommendation-after-the-adversarial-pass). The resulting model is a set of conditional decisions, not a proven universal AI-native organization.

This report distinguishes **using AI to engineer software** from **engineering AI products**. The first is relevant to almost every software team; the second adds requirements for evaluations, data, probabilistic behavior, and agent safety. Recommendations assume a small commercial software team, not a frontier-model training lab.

**Reading paths:** start with the [lighthouse teams](#1-start-here-the-lighthouse-teams), then the [executive synthesis](#2-executive-synthesis-what-to-build) and [evidence review](#3-what-the-evidence-actually-supports). For implementation, use the [team design](#4-design-the-human-team-around-responsibilities), [system blueprint](#5-the-engineering-system-a-concrete-reference-design), [AI-product requirements](#9-additional-requirements-when-the-product-itself-uses-ai), [scorecard](#14-metrics-a-balanced-engineering-scorecard), and [90-day roadmap](#17-a-90-day-implementation-roadmap). The [source register](#22-annotated-source-register) documents provenance and limitations.

**Using the references:** source markers such as [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) link directly to the underlying article, paper, or guidance. Grouped citations list each source separately. The [annotated source register](#22-annotated-source-register) explains what was consulted and the limitations. Staffing maps, templates, risk classes, budgets, and numerical operating targets are this report's recommendations unless explicitly attributed; nearby references explain their basis, not empirical validation of every proposed detail.

## 1. Start here: the lighthouse teams

There is no defensible public league table of the world's "best AI engineering teams." Private teams rarely disclose comparable quality, revenue, reliability, or fully loaded cost data. The useful question is: **which teams have documented systems worth learning from, and under what conditions do those systems transfer?**

The following are lighthouse examples for specific capabilities, not an overall ranking. Large companies are included because their infrastructure patterns are informative, not because a five-person company should copy their organizational structure.

**Selection warning:** these are unusually visible organizations, predominantly model/tool vendors or well-capitalized technology companies. Public accounts select for publishable successes; failed deployments and ordinary small non-vendor teams are underrepresented. A three-person experimental unit also inherits its parent's infrastructure, capital, model access, customer relationships, and specialist support. Its headcount is not its fully loaded production system. Repeated practices suggest hypotheses worth testing, not causal proof that those practices are necessary or sufficient.

| Lighthouse | Why study it | Public evidence | What a small team should borrow | What not to copy blindly |
|---|---|---|---|---|
| **OpenAI's harness-engineering team** | A small team reorganized engineering around agent execution | A five-month internal-product account, starting with three engineers and later growing to seven; roughly 1,500 PRs and a million lines across code, tooling, and docs [S01](https://openai.com/index/harness-engineering/) [S02](https://www.engineering.fyi/article/harness-engineering-leveraging-codex-in-an-agent-first-world) | Agent-readable architecture, runnable environments, executable constraints, observability, continuous cleanup | Its estimated development-speed multiplier, minimal blocking gates, or code volume as a success target |
| **Anthropic / Claude Code** | Individual workflow discipline and an increasingly explicit distinction between instructions and enforcement | Internal use cases, current operational documentation, harness research, and a reported workflow from Boris Cherny [S03](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code) [S04](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/) [S05](https://code.claude.com/docs/en/best-practices) [S06](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) [S07](https://www.anthropic.com/research/managed-agents) | Give agents checks they can run; use concise context; isolate work; preserve learning | Treating one person's session count, model preference, or old prompting recipe as a universal standard |
| **Stripe / Minions** | Unattended implementation inside a serious existing codebase | February 2026 engineering posts describe over 1,000, then over 1,300, minion-produced PRs merged weekly, with human review [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) | Deterministic workflow steps around flexible agent work; isolated environments; bounded retries; scoped tools | Building Stripe's platform, hundreds of integrations, or its entire developer environment from scratch |
| **Ramp / Inspect** | Full-stack background agents and collaborative verification | A technical implementation account and later launch account; the original account reported about 30% of merged frontend/backend PRs [S10](https://builders.ramp.com/post/why-we-built-our-background-agent) [S11](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal) [S12](https://ramp.com/blog/introducing-inspect) | Complete runnable environments, screenshots and previews, shared sessions, fast startup | Equating adoption or PR share with causal productivity; assuming "effectively free" infrastructure is literally free |
| **Shopify / River, Aquifer, Reflex, Sidekick** | Shared organizational learning, durable agent infrastructure, and agent-testable product architecture | Detailed accounts of reproducible environments, shared sessions, session/harness/sandbox separation, headless mobile testing, and production agent evaluation [S13](https://shopify.engineering/under-the-river) [S14](https://shopify.engineering/reflex) [S15](https://shopify.engineering/building-production-ready-agentic-systems) | Shared reviewed skills, durable state, fast behavior checks, product-expert involvement in evals | A monorepo migration, Nix adoption, native-mobile rewrite, or public-by-default treatment of sensitive work solely to imitate Shopify |
| **StrongDM's three-person AI team** | The most provocative small-team experiment: specifying and validating rather than reading every implementation | First-party software-factory description, released artifacts, and an outside observer's account [S16](https://factory.strongdm.ai/) [S17](https://simonwillison.net/2026/Feb/7/software-factory/) [S18](https://github.com/strongdm/attractor) | Separate acceptance scenarios, independent outcome validation, service simulators | A blanket ban on human code review, a token-spend quota, or assuming simulation establishes production security |
| **Cursor's autonomous-coding experiments** | Concrete lessons about agent coordination at large scale | A published account of long-running experiments, including failed coordination designs, a browser prototype, a migration still needing review, and a reported merged optimization [S19](https://cursor.com/blog/scaling-agents) | Explicit responsibilities, bounded tasks, evidence-based model selection, removing unnecessary orchestration | Hundreds of agents, shared-branch concurrency, or browser code volume as proof of production readiness |

**The common pattern is not "write more prompts." It is "build an environment in which agents can understand the work, act safely, and gather evidence about whether they succeeded."**

### 1.1 OpenAI: engineering the harness instead of manually producing the implementation

**What was reported.** Ryan Lopopolo's February 11, 2026 account describes building an internal beta product with internal daily users and external alpha testers. The team deliberately constrained itself to no manually written code. It reported roughly 1,500 opened-and-merged PRs over five months and a codebase on the order of a million lines, including infrastructure, documentation, and utilities. The team estimated about one-tenth the manual development time. That estimate is not a controlled comparison. [S01](https://openai.com/index/harness-engineering/)

**The actual engineering system matters more than the headline:** [S01](https://openai.com/index/harness-engineering/)

- An approximately 100-line `AGENTS.md` served as a map into structured documentation, not an encyclopedia.
- Product intent, architectural decisions, execution plans, and quality expectations lived in discoverable, versioned artifacts.
- Dependency directions, boundary parsing, logging conventions, and other invariants were checked mechanically.
- Each worktree could boot the application and its observability stack. Agents could inspect the UI, query logs and metrics, reproduce failures, and rerun checks.
- Repeated quality problems became automated checks or recurring cleanup tasks rather than recurring human reminders.

**What changed in human work.** Engineers specified outcomes, diagnosed missing capabilities in the environment, and maintained the feedback system. A failed agent run was often treated as evidence of missing context, tooling, or constraints rather than a reason to append "try harder."

**Transferable lesson.** If the agent cannot start the app, discover the right architectural boundary, or see a failed user journey, a better prompt has limited leverage. Fix the environment.

**Important boundary.** This was a particular greenfield product with substantial investment in its harness. The account explicitly does not establish architectural coherence over years. Its relaxed merge philosophy is especially unsuitable as a default for payments, permissions, irreversible data changes, or a team without strong rollback capability.

**Source-access limitation.** The original OpenAI URL returned HTTP 403 during this research. The detailed account was read through a third-party Markdown reproduction and compared with an engineering summary. These are not independent replications of the results. Treat the quantitative claims as company-reported with an additional source-access caveat. [S01](https://openai.com/index/harness-engineering/) [S02](https://www.engineering.fyi/article/harness-engineering-leveraging-codex-in-an-agent-first-world)

### 1.2 Anthropic: verification, concise instructions, and learning loops

Anthropic's internal examples span codebase navigation, test creation, debugging, prototyping, runbooks, and non-engineering tools. Its security engineers describe a more test-driven workflow; product engineers use the agent to locate relevant code before implementing changes; designers explore error states and use iterative build/test loops. These are qualitative company accounts, not a measured productivity trial. [S03](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code)

Boris Cherny's January 2026 workflow, as reported by InfoQ with links to his original posts, included multiple isolated sessions, plan refinement, shared repository guidance, reusable commands, formatting hooks, and browser-based verification. He also reported abandoning some sessions. The useful lesson is not "run fifteen agents"; it is **make delegation cheap, verify the result, and discard unproductive attempts without becoming committed to them**. [S04](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/)

Current Claude Code guidance makes an important distinction: prompts, skills, and instruction files influence model behavior, whereas tests, hooks, deny rules, managed settings, and branch protection can enforce parts of the workflow. Critical controls should not depend exclusively on whether the model follows prose. [S05](https://code.claude.com/docs/en/best-practices)

Anthropic's harness publications also illustrate why recipes expire. An earlier long-running setup used initialization, explicit feature state, progress artifacts, and incremental work. Its later Managed Agents discussion describes removing workarounds that became unnecessary with better models, while separating the durable session from the replaceable harness and sandbox. [S06](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) [S07](https://www.anthropic.com/research/managed-agents)

**Borrow:** executable verification, focused context, reviewed shared procedures, explicit state across long tasks, and periodic deletion of obsolete scaffolding.

**Do not infer:** a stable Anthropic-wide team-size ratio, a universal generated-code percentage, or a permanent best model from a personal workflow. This research did not establish those facts.

### 1.3 Stripe: a production-minded pattern for unattended coding

Stripe's Minions are particularly relevant to teams maintaining real existing software rather than creating unconstrained demos. A typical run starts with a request, operates unattended, and ends with a branch and PR ready for a human to inspect. Stripe explicitly retains human review. [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

The implementation combines:

| Element | Stripe's account | Small-team equivalent |
|---|---|---|
| Execution environment | Prewarmed, standardized devboxes, targeted to be ready within about ten seconds | A reproducible container or managed sandbox; optimize startup when it becomes a measured bottleneck |
| Orchestration | "Blueprints" combine deterministic nodes and flexible agent nodes | A job runner that always executes required checks and records results |
| Context | Scoped rules, repository knowledge, and selected internal tools | A short instruction entry point, module documentation, issue context, and a small tool allowlist |
| Feedback | Fast local linting, selected CI tests, automatic fixes where appropriate | Cheap checks before expensive integration runs |
| Stopping policy | At most two CI rounds before returning the branch to a human | An explicit retry/time/cost budget with useful escalation |
| Safety | QA environments without production data, production services, or arbitrary network egress | Separate worker identity, synthetic data, least privilege, constrained network access |

Stripe's February 19 post reports over 1,300 minion-produced PRs merged per week, up from over 1,000 in the February 9 account. These are counts at Stripe's scale, not a percentage of all work or a causal estimate of engineering acceleration.

**Best lesson:** use an LLM where the next step requires judgment; use ordinary software where the required step is already known.

**Why not build all of this immediately?** Stripe benefits from years of developer-tool investment and a codebase with unusual scale and internal conventions. A small team should first test whether commercially available agents plus a reproducible environment solve the problem.

### 1.4 Ramp: close the verification gap and make the session collaborative

Ramp's original Inspect account is unusually concrete. Sessions run in sandboxed environments with the services needed to exercise the application. Images are prepared periodically so cloning, dependency installation, and initial builds are mostly removed from the interactive path. The agent can run tests, inspect telemetry, use a browser, and provide screenshots or previews. Humans can participate from different interfaces and continue the same session. [S10](https://builders.ramp.com/post/why-we-built-our-background-agent)

**What this fixes:** an agent that produces plausible code but cannot run the database, reproduce the bug, or inspect the frontend leaves the expensive part of the task to a human.

The adoption claims also show why research needs timestamps and definitions. The original implementation account reports about **30% of merged frontend/backend PRs**. A later infrastructure-vendor case study reports roughly half. Ramp's later launch page reports **74% of merged PRs**, 99% recent use among engineering/design/product staff, and six times as much code shipped per person versus a year earlier. These are different accounts and observation windows, not a single consistent experimental dataset. None establishes that Inspect caused a sixfold improvement in customer value or quality-adjusted throughput. [S10](https://builders.ramp.com/post/why-we-built-our-background-agent) [S11](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal) [S12](https://ramp.com/blog/introducing-inspect)

**Borrow:** full-stack execution, fast feedback, shareable sessions, and a handoff containing evidence.

**Modify for a small team:** start with one agent interface and one supported environment. Add multiplayer or Slack integration only when it reduces actual coordination cost. Enforce spend and concurrency caps even if a case study describes capacity as effectively unlimited.

### 1.5 Shopify: infrastructure, shared learning, and architecture designed for verification

Shopify contributes three distinct lessons.

**River and Aquifer: make knowledge compound.** Shopify describes a monorepo and reproducible Nix substrate beneath River, its shared Slack agent. The account reports one in eight merged PRs coauthored by River; a specified recent 30-day window includes 59,918 sessions and 3,536 merged coauthored PRs. These are operational adoption figures, not a small-team productivity comparison. [S13](https://shopify.engineering/under-the-river)

More transferable than those counts is the architecture: a durable session/event log, a replaceable harness, and a disposable sandbox. Reviewed skills, runbooks, and instruction changes preserve lessons beyond a private chat. A new agent configuration becomes a profile on a common substrate rather than a separate platform.

**Reflex: make product behavior cheap to exercise.** Shopify's mobile account separates headless application logic from rendering and platform integration. ViewModels expose actions and state through a consistent contract, allowing a CLI to drive behavior tests on iOS and Android implementations. It reports more than 1,700 behavior tests finishing in about four minutes on CI across the two platforms. This is a concrete feedback-loop measurement, not evidence that native rewrites are universally preferable. [S14](https://shopify.engineering/reflex)

The broader lesson is architectural: **build interfaces that make behavior inspectable without forcing every check through a slow GUI**. Keep device, rendering, accessibility, and real integration testing where those properties matter; headless logic tests cannot establish them.

**Sidekick: production agent quality requires calibrated evaluation.** Shopify describes instruction bloat, just-in-time guidance, production-derived evaluation sets, product-expert labels, calibrated model judges, user simulation, and reward hacking. Its account explicitly advises avoiding multi-agent architectures early. [S15](https://shopify.engineering/building-production-ready-agentic-systems)

**Borrow:** reproducibility, durable state, shared procedures, headless behavioral contracts, and human-calibrated evals.

**Do not cargo-cult:** monorepo conversion, Nix, moving from React Native to native code, or recording all internal work publicly. Security, privacy, and the team's existing competence should determine those decisions.

### 1.6 StrongDM: specify intent, validate independently, interrogate the economics

StrongDM's first-party account describes a three-person AI team formed on July 14, 2025, and a software factory in which specs and scenarios drive agents that implement and validate software without human code review. [S16](https://factory.strongdm.ai/)

Two ideas deserve attention:

1. **Acceptance scenarios outside the implementation workspace.** If an agent can redefine the tests to match its implementation, green tests provide weaker evidence. A separate scenario/evaluation boundary reduces this problem.
2. **Behavioral service simulators.** Its "Digital Twin Universe" models services such as Okta, Jira, Slack, and Google Workspace so agents can exercise many workflows and failure modes without real-service limits or side effects.

Simon Willison's account adds an outside observer's description of working demos and released artifacts. He also calls out the economics of StrongDM's provocative suggestion to spend at least $1,000 per engineer per day on tokens. At twenty workdays, that would be $20,000 per engineer per month before other costs. That is not a sensible default budget for a small team. [S17](https://simonwillison.net/2026/Feb/7/software-factory/)

The public Attractor repository provides detailed specifications for a coding-agent system, making it a useful design artifact. It is not, by itself, an independently verified production implementation or evidence of reliability. [S18](https://github.com/strongdm/attractor)

**Borrow:** separation between implementation and acceptance, realistic scenario testing, simulator use for dangerous or rate-limited workflows.

**Do not conclude:** "no review" is established best practice. A simulator can share the same misunderstandings as the implementation. A model judge can be fooled. Real integration tests, security analysis, authorization invariants, and human accountability still matter.

### 1.7 Cursor: coordination is an engineering problem, not an agent-count contest

Cursor reports trying flat coordination through shared files and locks, then optimistic concurrency, before adopting planner/worker responsibilities and end-of-cycle judging. Failure modes included lock contention, brittle state, risk avoidance, and work churning without end-to-end progress. [S19](https://cursor.com/blog/scaling-agents)

Its browser experiment generated over a million lines across about a thousand files in close to a week. That is a demonstration of sustained autonomous work, not a browser conformance, security, maintainability, or business-success benchmark. The same account says a large Solid-to-React migration still needed careful review. A separate video-rendering improvement was reported as merged, with a 25-fold performance improvement in that particular workload.

These experimental counts and the workload-specific performance claim come from Cursor's account, not independent benchmarking. [S19](https://cursor.com/blog/scaling-agents)

**Borrow:** assign responsibility, define bounded work, use clean state, test model/harness combinations, and remove orchestration that adds bottlenecks.

**Small-team default:** one implementation agent per independent task, plus focused review when useful. Add more only when measured cycle time improves without growing review queues, integration failures, or cost.

## 2. Executive synthesis: what to build

<keyidea>A small AI-forward team should be a product team with a reliable software-production system, not a miniature research lab or a collection of people supervising unrelated chat windows.</keyidea>

The revised default is **a small product team with end-to-end ownership, hands-on technical judgment, access to the relevant domain expertise, and named responsibility for its engineering system**. There is no established optimal AI-era headcount or seniority ratio. For a five-engineer team, leadership and system work should initially be responsibilities within the team, not automatically separate full-time positions. Hire against the actual constraint: customer discovery, domain knowledge, delivery, reliability, or assurance.

Start with an approved coding tool and the smallest safe existing delivery path. Do not construct the full reference architecture before using AI. Interactive assistance, read-only investigation, and one bounded implementation workflow can be valuable without a custom background-agent platform.

The system should make the following loop cheap and observable:

```text
Customer evidence
  -> bounded intent + acceptance examples + risk class
  -> isolated development environment
  -> agent-assisted implementation
  -> executable checks + independent acceptance evidence
  -> accountable review
  -> staged release + production observation
  -> incident/failure converted into a better test, tool, or procedure
```

The ten highest-priority decisions are:

| Priority | Decision | Rationale |
|---|---|---|
| 1 | Optimize for customer outcomes and quality-adjusted delivery, not generated code | Faster creation is not automatically faster useful delivery |
| 2 | Give every task a named human owner | Agents do not absorb accountability |
| 3 | Remove the setup and verification failures that actually block eligible work | A reproducible path helps humans and agents; a platform transformation is not a prerequisite for every use |
| 4 | Supply only missing, useful context; test instruction changes | Context files can increase cost without improving task success [S33](https://arxiv.org/html/2602.11988v3) |
| 5 | Enforce critical invariants outside the model | Instructions are not authorization or branch protection |
| 6 | Make acceptance evidence appropriately independent and audit the checks themselves | Separate permissions do not prevent shared specification errors |
| 7 | Default to small changes and controlled work in progress | Review and integration are finite-capacity systems |
| 8 | Prefer an approved existing tool; build only against a demonstrated gap | Procurement, data restrictions, and maintenance costs can change the buy/build decision |
| 9 | Measure local gains with review, rework, reliability, and cost included | Public studies disagree because settings and interventions differ |
| 10 | Preserve human expertise and shared institutional memory | Oversight is meaningless without understanding |

These are a synthesis of the sources, not a claim that every lighthouse follows exactly this operating model.

**Basis for this synthesis:** production workflow accounts [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), the conflicting productivity evidence [S20](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/) [S21](https://arxiv.org/abs/2507.09089) [S22](https://metr.org/blog/2026-02-24-uplift-update/), delivery-system research [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S24](https://research.google/pubs/dora-ai-capabilities-model/) [S25](https://dora.dev/ai/roi/report/), and the later counterevidence [S33](https://arxiv.org/html/2602.11988v3) [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3) [S36](https://www.nber.org/papers/w35275).

## 3. What the evidence actually supports

### 3.1 Evidence hierarchy and research method

This is a structured research synthesis, **not an exhaustive systematic review** and not an independent audit of any company.

Sources were sought across lighthouse engineering accounts, original productivity research, delivery research, agent-evaluation guidance, and risk-management guidance. Search summaries were used for discovery; substantive claims were checked against retrieved source text wherever possible. Unverified team-size and generated-code-percentage claims were excluded. The OpenAI source-access exception is disclosed above.

Evidence types should not be collapsed:

| Evidence type | Useful for | Principal limitation |
|---|---|---|
| Randomized trial | Estimating the effect of a specific intervention in a defined population | May be small, dated, narrow, or unlike the team's workflow |
| Matched event study / difference-in-differences | Adoption patterns and longitudinal effects under explicit identification assumptions | Adoption is not randomized; unmeasured differences and pre-trends can undermine causal interpretation |
| Controlled benchmark / ablation | Isolating a tool, prompt, or architecture change under repeatable conditions | Test validity, contamination, task selection, and transfer to real work remain open |
| Large organizational survey | Associations and system-level patterns | Selection, self-report, confounding, and no automatic causal interpretation |
| First-party engineering account | Concrete implementation patterns and operational experience | Selective disclosure and commercial/reputational incentives |
| Outside practitioner review | Scrutiny, comparison, and demonstration context | Usually not a controlled audit or independent reproduction |
| Documentation / standards guidance | Interfaces, controls, and repeatable practices | Not proof of a quantified productivity benefit |
| Recommendation in this report | A practical decision under uncertainty | Must be tested locally; not a measured universal optimum |

Publication date, retrieval date, and measurement window are different. Live documentation can change. Numbers in this report belong to the cited account, not necessarily to the company's state on November 6. No verified November-wide industry census or comprehensive 2026 DORA annual report was established; the report uses identifiable 2025 research and the 2026 ROI framework rather than relabeling them.

### 3.2 Positive and negative productivity results can both be true

| Study / account | Finding | What it establishes | What it does not establish |
|---|---|---|---|
| Three developer field experiments, Microsoft/Accenture/another Fortune 100 company | Across 4,867 developers, the analysis reports 26.08% more completed tasks, standard error 10.3% [S20](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/) | A positive pooled effect in those coding-assistant experiments | A universal agentic-team multiplier or unchanged downstream quality |
| METR, early-2025 randomized trial | 16 experienced contributors completed 246 tasks; allowing AI increased task time by 19% [S21](https://arxiv.org/abs/2507.09089) | A slowdown in that mature-codebase setting with those tools | That current tools always slow developers, or that greenfield results match |
| METR, February 2026 follow-up | Raw estimates moved toward speedup, but selection effects and concurrent-agent time measurement made the signal unreliable [S22](https://metr.org/blog/2026-02-24-uplift-update/) | Why updating the original estimate is methodologically difficult | A reliable new universal speedup or a clean reversal of the original result |
| DORA 2025 | Positive associations with delivery throughput and product performance, but a negative association with stability [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S24](https://research.google/pubs/dora-ai-capabilities-model/) | AI value depends on the surrounding delivery system | A causal per-engineer percentage gain |
| Lighthouse adoption figures | Many agent-produced or agent-coauthored PRs | These workflows are used at material scale | Incremental customer value, avoided hiring, defect rates, or full ROI |

METR's original participants believed they were faster even when the experiment measured a slowdown. That is a strong reason not to use enthusiasm or perceived speed as the primary success measure.

The follow-up deserves precision: returning developers had an estimated task-time change of -18%, with an interval from -38% to +9%; newly recruited developers had -4%, with an interval from -15% to +9%. Both include no effect. METR explicitly warns that selection effects make the results an unreliable current-productivity signal. [S22](https://metr.org/blog/2026-02-24-uplift-update/)

**Practical conclusion:** AI assistance can create substantial value; the magnitude depends on task selection, baseline skill, codebase familiarity, tool generation, and whether the rest of the system can absorb the work.

### 3.3 DORA: AI amplifies the system it enters

DORA's 2025 account draws on nearly 5,000 survey respondents and over 100 hours of qualitative data. Its central framing is that AI amplifies organizational strengths and weaknesses. A team with slow CI, tightly coupled architecture, unclear priorities, and fragile releases can produce more change without improving delivery. [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report)

The associated capabilities model emphasizes a clear AI stance, healthy data, AI-accessible internal context, version control, small batches, user-centricity, and a quality internal platform. [S24](https://research.google/pubs/dora-ai-capabilities-model/)

For five engineers, "internal platform" should initially mean **a reliable paved path**, not a platform department: reproducible setup, shared scripts, CI, environment policies, telemetry, and a release mechanism.

DORA's 2026 ROI material also frames the initial learning and process-adjustment cost as a J-curve and recommends reinvesting capacity rather than equating AI gains with headcount cuts. Its financial scenarios are models, not guaranteed returns. [S25](https://dora.dev/ai/roi/report/)

**Adversarial qualification:** "AI amplifies the system" is a useful diagnostic, not a complete causal theory. It does not identify which investment has the highest marginal return, establish a universal maturity threshold, or imply that a team must fix all engineering debt before trying AI. An agent may itself remove a setup or test bottleneck. Compare that targeted experiment with improving CI, reducing scope, or spending the same time with customers.

### 3.4 Learning is part of the production system

Anthropic's randomized study of 52 mostly junior Python developers learning Trio reported average quiz scores of 50% with AI versus 67% without: a **17-percentage-point difference**, not merely a 17% relative decline. The completion-time difference was not statistically significant. [S26](https://www.anthropic.com/research/AI-assistance-coding-skills)

The result concerns immediate comprehension of a new library, not years of engineering development. Qualitative patterns associated conceptual questions and explanation-seeking with better mastery, but those interaction-pattern comparisons were not randomized causal findings.

**Team implication:** do not maximize delegation at the expense of the ability to diagnose failures. Pair AI-assisted output with comprehension, debugging practice, and meaningful production ownership.

### 3.5 Where confidence is high, medium, and low

Confidence in a control's protective rationale is different from confidence in its incremental productivity or financial return. The ratings below are judgments from this synthesis, not probabilities or meta-analytic estimates.

| Recommendation | Revised confidence | Why |
|---|---|---|
| Reproducible execution and executable feedback | Strong engineering rationale; local ROI conditional | Useful across humans and agents; recurrence in cases does not isolate a causal productivity effect |
| Explicit ownership and protected authority boundaries | Strong protective rationale | They make responsibility and permissions explicit; they do not prove a specific approval process is efficient |
| Small changes and controlled work in progress | Strong starting heuristic, not an absolute | Usually improves inspectability; excessively fragmented changes can add coordination and review overhead |
| Repository instruction files improve success | Unproven as a general claim | Controlled evidence found no significant overall task-success benefit and increased inference cost [S33](https://arxiv.org/html/2602.11988v3) |
| Scoped tools and least privilege | Strong protective rationale | Limits possible damage; this is separate from the empirical claim about context files |
| Separate acceptance checks and calibrated evaluators | Strong rationale; effectiveness conditional | Reduces some self-validation failures, but the specification and evaluator can both be wrong [S40](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) |
| More parallel agents improve team throughput | Conditional | Task structure matters; benchmark gains and large regressions both occur [S37](https://arxiv.org/html/2512.08296v3) |
| Automatic merge for narrowly bounded tasks | Conditional | Plausible with strong controls; local evidence required |
| An internal custom agent platform is worth building | Conditional | Strong at some companies; maintenance economics differ sharply for small teams |
| AI necessarily degrades maintainability | Not established | Observational warning/complexity signals coexist with a controlled downstream study finding no systematic harm [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3) |
| Eliminate all human implementation review | Low as a general recommendation | Public experiments do not establish universal safety or economics |
| Replace a fixed percentage of engineers with agents | Unsupported | Available studies do not establish such a staffing rule |

### 3.6 Counterevidence that changes the recommendations

The adversarial question is not "can we find negative AI stories?" It is **which plausible findings would make the original recommendations wrong, too expensive, or insufficient?** The evidence below includes results against both AI enthusiasm and blanket skepticism.

#### A. Repository instruction files: common advice is not established effectiveness

Gloaguen et al.'s September 29, 2026 revision evaluates four model/agent settings using 300 SWE-bench Lite tasks and 138 CTXbench tasks from 12 Python repositories with developer-committed context files. It compares no context file, generated files, and developer-written files where available. Neither generated nor developer-written files significantly improved overall resolution against the no-file baseline. Generated files increased average inference cost by about 20% on SWE-bench and 23% on CTXbench. Developer files beat generated files, but that is not evidence that they reliably beat no file. [S33](https://arxiv.org/html/2602.11988v3)

Agents did follow instructions, test more, and explore more. Those additional activities did not translate into a significant task-resolution benefit. **Instruction adherence and visible diligence are not the same as better outcomes.**

**Counterargument to the counterargument:** this is Python issue resolution with particular models, one completion per setting, and test-based outcomes. CTXbench uses generated task descriptions and tests, manually inspected and corrected by the researchers. The experiment does not establish that instructions cannot improve security, organizational compliance, unfamiliar tooling, or long-term collaboration. Nonsignificance is not proof of equivalence; the paper also does not establish that shorter files alone cause better results.

**Revision:** retain only genuinely additional conventions and necessary commands, avoid generated repository summaries by default, and compare optional instruction changes against a minimal baseline. Do not remove mandatory safety controls to create that baseline. Keep human-facing documentation useful without assuming its automatic inclusion improves every agent run.

#### B. More autonomous is not necessarily more productive than an existing copilot

Agarwal et al.'s repository-level study distinguishes observable agent-first adoption from adoption after observable AI-IDE use. Its matched, staggered difference-in-differences analysis uses 401 agent-first repositories and 606 controls, plus 117 IDE-first repositories and 73 controls. It reports larger, front-loaded activity gains in the former and little sustained marginal gain in the latter. It also reports roughly 18% more static-analysis warnings and 39% more cognitive complexity. [S34](https://arxiv.org/html/2601.13597v2)

**Reasons not to overclaim:** adoption is inferred from public artifacts, not randomized; prior IDE use is inferred from configuration traces; unobserved adoption can be missed; outcomes are repository activity and static-analysis proxies. The authors acknowledge concerning pre-treatment coefficients in some quality outcomes. The percentages do not mean 18% more production bugs or 39% higher maintenance cost. Nor do the results establish that autonomous agents never help experienced copilot users.

An important opposing result comes from Chen et al.'s controlled within-participant comparison of Copilot and OpenHands. Twenty university-recruited participants who regularly used Copilot, many with professional experience, attempted paired task types with randomized tool order. Agents improved correctness and reduced active user effort in that setting. However, the short April-May 2025 sessions, selected tasks, differing tool/model arrangements, and vendor-affiliated authors limit generalization. [S42](https://arxiv.org/html/2507.08149v2)

**Synthesis:** compare against the team's actual current workflow, not an obsolete no-AI counterfactual. Evaluate tool, model, environment, task selection, and interaction mode as a bundle. Reorganizing work can unlock capability; buying an "agent" label is not independently sufficient.

#### C. Maintainability: neither inevitable debt nor proven harmlessness

Borg et al.'s preregistered two-phase study involved 151 participants, about 95% professionals. In the randomized second phase, new developers extended code produced with or without AI, without using AI themselves. The study did not detect a systematic downstream completion-time or quality disadvantage. Its frequently cited first-phase speed gains are observational: assignment to AI use partly followed participants' preferences, rather than a randomized AI productivity intervention. The work was conducted in late 2024, before current autonomous workflows. [S35](https://arxiv.org/html/2507.00788v3)

This is a meaningful counterweight to "AI code inevitably creates technical debt." It does not invalidate warning signals in [S34](https://arxiv.org/html/2601.13597v2): the interventions, populations, tasks, outcome measures, and horizons differ. Conversely, [S34](https://arxiv.org/html/2601.13597v2) cannot substitute static metrics for observed downstream maintenance cost.

**Revision:** retain maintainability guardrails but test the mechanism. Inspect change amplification, time to modify unfamiliar code, incidents, repeated repair, and dependency growth. Do not accept or reject a change solely because AI wrote it. Absence of detected harm in bounded follow-up is not proof of lifetime equivalence.

#### D. Code-output gains attenuate before releases and customer usage

Demirer, Musolff, and Yang's June 2026 NBER working-paper abstract describes a matched event study of more than 500,000 GitHub developers linked to AI usage telemetry. It reports cumulative coding-activity effects of 30% for autocomplete, 180% for interactive agents, and 240% for autonomous agents. The last figure attenuates to 80% for project count and 30% for releases. Across four software marketplaces it reports more new apps but no increase in total usage. [S36](https://www.nber.org/papers/w35275)

These are **cumulative estimates**, not three additive gains or a 240% incremental benefit from upgrading an existing copilot. The design is observational. This synthesis consulted the original abstract and metadata, not the full paper's identification checks; the figures should be treated as reported working-paper findings.

**Counterargument:** a release count is also an imperfect value measure; fewer, better releases can win. Aggregate marketplace usage can mask valuable gains for individual companies, changes in app quality, or redistribution. The study does not establish that AI-created software has no business value.

**Revision:** trace value through the whole chain: completed useful change, safe release, actual use, customer outcome. If code generation is no longer the constraint, redirect the next investment toward discovery, integration, adoption, or reliability rather than another generation tool.

#### E. Multi-agent gains and regressions are both real possibilities

Kim et al.'s April 2026 revision compares 260 configurations across six benchmarks, five architectures, and three model families with standardized tools, prompts, and compute. Reported relative changes range from +80.8% on decomposable financial reasoning to -70.0% on sequential planning. These are benchmark-specific effects, not software-team productivity forecasts; the predictive model's cross-validated explanatory power is limited. [S37](https://arxiv.org/html/2512.08296v3)

**Revision:** a single agent is an inexpensive baseline, not a moral preference. Test decomposition where work is genuinely separable and integration is observable. A small team may rationally run many agents for a cheap, bounded search or migration batch while using one for a tightly coupled diagnosis. Match the topology to the work and compare at a fair resource budget.

#### F. Human review: accountability is necessary, effective inspection is not automatic

A JetBrains/Lund participatory design study involved 17 practitioners, seven returning for design work, and a 43-person follow-up survey. It proposes overview, file-level risk analysis, and selective snippet inspection to improve trust calibration. This is a conceptual workflow with perceived usefulness ratings, **not an experiment demonstrating fewer defects or faster review**. [S38](https://doi.org/10.4230/LIPIcs.ESEM.2026.89)

It nevertheless challenges the idea that putting "human reviewed" on every PR is sufficient. Reading a fluent summary and clicking approve may add delay without finding important defects. A second model's confident risk scores are not automatically calibrated either.

**Revision:** preserve named accountability, but select review depth using impact, uncertainty, reversibility, and demonstrated control quality. Ask what defect the review is supposed to detect. Measure queueing, substantive findings, rework, and escaped defects. Human review also transfers knowledge and coordinates design; eliminating it can remove benefits beyond defect detection.

#### G. Invisible labor and costs imposed on others

An observational analysis of 20,574 publicly logged sessions across 1,639 repositories identifies effort/trust costs in 90.50% of extracted misalignment episodes. Among the small subset with visible resolutions, 91.49% required explicit developer correction. These percentages concern **identified episodes and visible resolutions**, not the fraction of all sessions that failed. Public opt-in logs, pushback-based detection, and LLM-assisted annotation constrain the inference; silent failures and unrecorded resolutions can be missed. [S39](https://arxiv.org/html/2605.29442v2)

The curl maintainer's January 2026 account provides a negative operating case. The project ended its bug bounty after rising low-quality reports and a confirmation rate below 5% during 2025. He attributes the burden to AI-generated noise, deteriorating human submissions, and incentives. He explicitly notes that comparable projects were not seeing the same report-volume increase and that curl's PR process had not suffered the same problem. [S41](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)

**Revision:** include prompt repair, monitoring, attention switching, and other people's triage in cost. Require reproduction and actual evidence before submitting an AI-generated issue or vulnerability claim. Do not generalize curl's bounty experience to every open-source contribution or make affected maintainers subsidize a team's claimed productivity.

#### H. The evaluator is also a fallible engineering artifact

OpenAI audited 138 SWE-bench Verified problems that its model did not consistently solve, a deliberately difficult subset of a 500-task benchmark. It reports material test/specification problems in 59.4% of that audited subset, and evidence of benchmark exposure in models from multiple providers. **That is not a representative estimate that 59.4% of all coding tests are flawed.** The source is a model vendor auditing a benchmark it helped create and recommending alternatives. [S40](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)

**Revision:** deterministic execution can repeatedly enforce the wrong requirement. Hidden tests can reject valid alternatives; public tests can leak into training; private holdouts can become effectively public through repeated tuning. Independently validate the behavior contract, audit disagreements, rotate genuinely fresh cases, and verify some real-world outcomes. A good test suite is evidence, not an oracle.

### 3.7 Adversarial assumption ledger

This ledger separates what survives from what must change. The counterarguments are analytical judgments informed by the cited evidence, not additional measured effects.

| Original assumption or tempting inference | Strongest challenge | What survives the challenge | Verdict and operating consequence |
|---|---|---|---|
| Lighthouse systems reveal the best organization | Visibility, vendor incentives, inherited infrastructure, and survivorship bias distort the sample | Detailed cases expose workable mechanisms | **Narrow:** borrow a mechanism only after identifying the matching local problem and total enabling cost |
| Recurring practices are causal necessities | Successful teams can share unnecessary habits; controls arrive bundled | Recurrence raises plausibility and suggests testable hypotheses | **Revise:** distinguish reported practice, causal evidence, protective rationale, and local recommendation |
| More agent-readable context improves work | Context-file ablations do not show general success gains [S33](https://arxiv.org/html/2602.11988v3) | Missing nonstandard information can matter; mandatory restrictions still apply | **Revise:** minimal additional instructions, with evaluated changes rather than context accumulation |
| Five engineers imply a lead, three delivery engineers, and a platform engineer | That can allocate 40% of capacity to leadership/system work before demand is validated | Someone must own priorities, reliability, and tooling | **Revise:** assign responsibilities first; dedicated capacity follows measured load |
| Generalists and seniors are always the right hires | Domain expertise, design, customer access, or a specialist constraint may dominate | End-to-end ownership and judgment remain useful | **Unproven ratio:** choose the next hire against the constraint, not an AI-team archetype |
| Build the full harness before delegating | Platform work can consume the benefit and postpone learning | Safe execution and enough feedback for the actual task are necessary | **Revise:** start with a bounded real task, add infrastructure against observed failures |
| All controls are additive improvements | Redundant reviews, flaky tests, and permission ceremonies impose queues and confusion | Important risks still need effective controls | **Narrow:** give each control an owner, failure mode, evidence of operation, and maintenance cost |
| Independent acceptance establishes correctness | Separate runners can share a wrong specification; secrecy can hide unfair tests [S40](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) | Permission separation prevents some tampering | **Retain with limits:** distinguish authority independence from independent evidence and real-world fidelity |
| Humans in the loop make generated work safe | Automation bias, time pressure, and large diffs can defeat review [S38](https://doi.org/10.4230/LIPIcs.ESEM.2026.89) | Humans retain domain judgment and accountability | **Revise:** deliberate risk-weighted review, not universal line-reading or universal removal |
| AI necessarily causes technical/cognitive debt | Controlled downstream evidence does not show systematic maintenance harm [S35](https://arxiv.org/html/2507.00788v3); comprehension evidence is narrow [S26](https://www.anthropic.com/research/AI-assistance-coding-skills) | Some observational signals and learning risks warrant attention | **Unresolved:** measure actual repair and understanding; do not convert plausible risks into universal facts |
| More autonomous agents provide additive gains | Existing AI use, task coupling, and verification bottlenecks change returns [S34](https://arxiv.org/html/2601.13597v2) [S37](https://arxiv.org/html/2512.08296v3) | Some controlled interaction evidence favors agents [S42](https://arxiv.org/html/2507.08149v2) | **Conditional:** compare against the current workflow and include active effort, elapsed time, cost, and quality |
| Maximum caution is costless | Approval queues, delayed learning, and uneconomic review can destroy real benefits | Consequential authority still needs boundaries | **Revise:** experiment rapidly where blast radius is bounded; do not demand production-level process for a disposable synthetic prototype |
| Faster implementation means more business value | Releases, adoption, and demand can remain bottlenecks [S36](https://www.nber.org/papers/w35275) | Useful capacity and previously infeasible work can create value | **Conditional:** measure downstream conversion and compare with the best non-AI investment |
| A modular monolith is the AI-era answer | Existing boundaries, deployment constraints, team expertise, and assurance needs can dominate | Cohesion and inexpensive testing are good design goals | **Starting heuristic:** do not rewrite healthy architecture to match this report |

### 3.8 Challenge the skeptical case too

An adversarial pass should not simply replace vendor optimism with pessimistic cherry-picking.

**Fixed-task studies can miss expansion of the feasible set.** An agent may make an otherwise unaffordable prototype, migration, or analysis possible. Counting only minutes saved on existing tickets misses this value. However, a previously infeasible artifact is valuable only if it answers a real question or serves a real need; generation volume is still not the outcome. [S42](https://arxiv.org/html/2507.08149v2)

**First-use friction is not necessarily steady-state cost.** Training and workflow redesign may initially obscure a real gain. A short bake-off can understate that potential. Conversely, "we are on the learning curve" must not become an unfalsifiable explanation for indefinite losses. Timebox the learning investment and look for a decreasing intervention burden.

**Controls can be redesigned, not merely added.** Better executable contracts, smaller reversible changes, and production signals can replace a redundant low-value gate for an eligible class. Removal should be a measured decision with retained accountability and recovery, not an assertion that the model has become trustworthy.

**Old negatives and old positives both expire.** Tool improvements, changed tasks, and learned workflows can alter results. Re-evaluate the relevant local configuration without treating every model release as a reason to reset all evidence or postpone all decisions.

**The balanced conclusion is asymmetric:** be ambitious about experiments with bounded consequences, but demanding about evidence before expanding authority, fixed operating costs, or irreversible commitments. This is not a demand for certainty before use, nor permission to treat uncertainty as proof of unlimited upside.

## 4. Design the human team around responsibilities

### 4.1 An illustrative five-engineer responsibility map

This is a **coverage map**, not a scientifically established ideal or a full-time allocation. The initial version over-specified the lead/three-delivery/one-platform split. The evidence does not establish that ratio, and a dedicated system role can be an expensive mistake for a small early-stage product.

**Basis and limits:** the responsibilities adapt the system-capability concerns in DORA [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S24](https://research.google/pubs/dora-ai-capabilities-model/) and the operational responsibilities in the lighthouse accounts [S07](https://www.anthropic.com/research/managed-agents) [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2). The role allocations and hiring work sample below are this report's proposals, not staffing findings from those sources.

| Responsibility | Typical owner | What they must own |
|---|---|---|
| Technical/product leadership | Hands-on lead or founding engineer | System boundaries, priorities, risk acceptance, major technical decisions, coaching |
| End-to-end product delivery | All engineers, with overlapping strengths | Customer problem through implementation, evidence, rollout, and operation |
| Engineering-system quality | Named engineer or rotating owner, with explicitly budgeted time | Reproducible environments, CI, release safety, agent permissions, workflow evaluation |
| Product/design/domain judgment | Founder, embedded designer/PM, or a shared partner | Discovery, interaction quality, acceptance examples, prioritization |
| Specialist assurance | Named internal owner plus fractional specialists when warranted | Security, privacy, legal, compliance, and domain-specific review |

The system owner still ships product and understands the system under test. Product engineers still maintain tests and participate in operation. Avoid a wall between "people who prompt," "people who review," and "people who run the system."

Make system work visible for a few weeks before reserving a large permanent fraction of the team for it. If recurring environment, CI, release, and control work demonstrably exceeds the shared budget and improvements repay their cost, dedicate more capacity. If the real constraint is domain correctness or customer discovery, hire or allocate there instead. No study here establishes that a senior generalist substitutes for a necessary security, data, design, or domain specialist.

For an AI product, explicitly assign **evaluation and data ownership**. It may initially be a product engineer plus a domain expert, rather than a separate ML department.

### 4.2 How this changes with team size

| Team size | Recommended shape | Guard against |
|---|---|---|
| 2-3 engineers | Everyone ships; one person owns the paved path; use managed services and a narrow product scope | Single-person production knowledge, pretending there is independent review when there is not |
| 4-6 engineers | Broad product ownership with a visible reliability/platform responsibility and overlapping domain expertise | A lead who must approve every low-risk decision |
| 7-10 engineers | Consider two outcome-oriented groups with shared standards and a lightweight enablement function | Premature platform organization or siloed frontend/backend/AI queues |

If only two people can operate the product, a 24/7 service promise may be a larger risk than coding speed. Choose support commitments, managed infrastructure, and customer expectations accordingly.

### 4.3 Hire for judgment and system leverage

Look for engineers who can:

- Translate a vague problem into falsifiable acceptance examples.
- Navigate unfamiliar code and identify the correct change boundary.
- Evaluate generated code rather than trusting its confidence.
- Debug across application behavior, data, logs, and infrastructure.
- Design interfaces that make testing and safe delegation easy.
- Notice when ordinary code is preferable to another model call.
- Explain tradeoffs, preserve institutional knowledge, and collaborate with customers.

Do not make "knows many prompt tricks" the central hiring criterion. Tools change faster than sound engineering judgment.

**Suggested work sample:** give a candidate a small existing service, an ambiguous bug report, access to a coding agent, and a realistic timebox. Ask them to diagnose, fix, show evidence, and describe rollback. Then introduce a plausible but incorrect agent suggestion. Evaluate whether they investigate it.

Score problem framing, correctness, evidence, simplicity, operational awareness, and communication. Add a short unaided code-reading/debugging discussion to distinguish genuine understanding from polished agent output. Publish tool-use expectations and accommodate candidates consistently.

### 4.4 Keep an apprenticeship path

An all-senior team can be a reasonable early-stage choice, but it is not a durable industry-wide talent strategy. Junior engineers need bounded ownership, not permanent confinement to AI-produced low-context tickets.

Use paired review, incident shadowing, explanation-first sessions for unfamiliar systems, and periodic debugging without agent-generated solutions. Ask the engineer to predict behavior before running a test and to explain why an alternative is wrong. The goal is retained judgment, not banning assistance.

The learning-risk motivation comes from Anthropic's immediate-comprehension experiment [S26](https://www.anthropic.com/research/AI-assistance-coding-skills); the proposed apprenticeship practices are a response to that risk, not interventions validated by that experiment.

### 4.5 Management and culture

Keep management close to actual work. The lead should inspect the review queue, flaky checks, recurring agent failures, customer outcomes, and operational load, not just tool utilization.

Make it safe to say "this task was faster manually," "the agent made this worse," or "we do not know." Mandatory AI percentages create incentives to conceal mistakes and inflate generated output.

Credit engineers for removing an unnecessary feature, deleting unused code, improving the harness, and preventing an incident. These actions can be more valuable than a large visible implementation.

For further reading on learning-oriented operations, see Google's [blameless postmortem guidance](https://sre.google/sre-book/postmortem-culture/). It addresses surfacing failures and improving systems rather than punishing individuals. [S44](https://sre.google/sre-book/table-of-contents/)

## 5. The engineering system: a concrete reference design

**Read this as a menu of capabilities, not a procurement or implementation checklist.** For interactive work, many layers already exist in Git, the developer environment, CI, and the deployment service. Keep essential data/permission boundaries from the start; add durable sessions, custom sandboxes, scenario services, and orchestration only when the workflow needs them and their cost is justified. Section 20 gives stage-specific minimum configurations.

### 5.1 Separate intent, execution, evidence, and authority

| Layer | Contents | Authority boundary |
|---|---|---|
| Intent | Issue, customer evidence, acceptance criteria, risk class, constraints | A named human owns the problem and scope |
| Knowledge | Architecture map, runbooks, decisions, API contracts, skills | Reviewed/versioned; sensitive information remains access-controlled |
| Execution | Agent runtime, tools, isolated workspace, temporary services | Restricted credentials, network, resource, and file access |
| Evidence | Check results, traces, UI artifacts, scenario outcomes, cost | Some checks run outside the implementer's write boundary |
| Integration | PR, merge queue, branch protection, required reviews | Worker identity cannot waive requirements |
| Release | Deployment identity, flags, migrations, canary, rollback | Separate from ordinary code-generation authority |
| Learning | Incident actions, regression cases, reviewed workflow changes | Proposed updates are reviewed before becoming shared instructions |

The human is not required to approve every local edit. The human and the system must retain authority over meaningful risk.

This layer model is a synthesis of the session/execution separation described by Anthropic and Shopify [S07](https://www.anthropic.com/research/managed-agents) [S13](https://shopify.engineering/under-the-river), Stripe's controlled integration workflow [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), and risk-management guidance [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook).

### 5.2 Repository and knowledge design

A useful starting structure for a product repository:

```text
README.md                    setup and entry points
AGENTS.md                    short map, commands, critical gotchas
docs/
  architecture.md            components, boundaries, data flow
  decisions/                 important tradeoffs and their rationale
  product/                   user journeys and acceptance examples
  runbooks/                  deploy, rollback, incident, recovery
  security/                  threat model and data classification
  engineering/               checks, environments, contribution workflow
src/                         coherent domain modules
tests/                       unit, integration, and journey checks
evals/                       AI-product tasks and grading, if applicable
tools/                       repeatable checks and developer commands
```

This is illustrative, not a mandate to reorganize a healthy repository or create every directory. Keep one authoritative knowledge source per subject. If agent-specific files are needed, reference authoritative material rather than duplicating it into contradictory rulebooks. Automatically generating a repository summary is not the default recommendation after the context-file findings. [S33](https://arxiv.org/html/2602.11988v3)

Candidate always-loaded context consists of necessary non-obvious commands, misleading legacy patterns, and constraints the agent cannot readily infer. Include an architecture map only if it demonstrably helps; ordinary discoverable repository structure is not automatically useful extra context. Longer procedures belong in discoverable skills or runbooks. Test optional instruction changes against a minimal baseline on representative tasks, including cost and intervention burden, not only instruction adherence. [S33](https://arxiv.org/html/2602.11988v3)

For important documents, record an owner and review trigger. A database-access change should trigger a runbook/security-document check; a deployment change should trigger release-document review. "Updated recently" alone does not establish accuracy.

### 5.3 Reproducible development environments

A fresh human or agent should be able to:

1. Obtain the right runtime and dependencies from pinned configuration.
2. Start the application's required services.
3. Load deterministic synthetic seed data.
4. Run a focused check and a smoke journey.
5. Inspect failures without guessing which credentials or hidden local settings are missing.

Use the simplest reliable mechanism your team can maintain: containers, a devcontainer, a package-manager toolchain, Nix, managed remote environments, or a combination. Reproducibility is the requirement; a particular technology is not.

Per-task isolation must include more than Git. Unique databases/schemas, service ports, object-store prefixes, queues, and feature-flag state prevent agents from contaminating each other's evidence. A worktree alone is not a security sandbox.

Prewarming and image snapshots become useful when setup latency is materially limiting adoption. An occasional ten-minute dependency restore is different from every task waiting ten minutes.

**Operational examples:** Stripe's devboxes [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), Ramp's complete environments and snapshots [S10](https://builders.ramp.com/post/why-we-built-our-background-agent) [S11](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal), and Shopify's reproducible environments [S13](https://shopify.engineering/under-the-river). These demonstrate implementations, not a mandate to adopt their exact infrastructure.

### 5.4 Architecture that is legible to humans and agents

Prefer a **modular monolith or a small number of cohesive services** unless deployment, isolation, scaling, or domain boundaries justify more. Agents may lower implementation cost; they do not erase distributed-system complexity.

Use explicit contracts and mechanically enforce the important ones:

| Boundary | Recommended mechanism |
|---|---|
| Module dependencies | Import/layer rules and architectural tests |
| Request and event shape | Typed contracts plus runtime validation at trust boundaries |
| Database access | Centralized authorization/tenant constraints, migrations, query tests |
| External services | Typed adapters, contract tests, explicit timeout/retry behavior |
| Side effects | Idempotency keys, transactions where possible, compensating actions where needed |
| Error handling | Structured errors/logs, no success-shaped fallback for failed work |
| Product behavior | Headless state/action interfaces plus real user-journey checks |

Do not proliferate abstractions just because an agent can generate them quickly. An interface is useful when it clarifies a boundary, makes a substitution safe, or materially improves verification.

The boundary-enforcement examples draw on OpenAI's harness account [S01](https://openai.com/index/harness-engineering/) and Shopify's headless behavior-testing architecture [S14](https://shopify.engineering/reflex). The monolith recommendation is a simplicity heuristic from this synthesis, not a comparative architecture result established by those cases.

### 5.5 Keep deterministic machinery deterministic

Formatting, dependency-graph validation, access checks, status transitions, artifact collection, and budget enforcement generally do not need language-model judgment.

Stripe's deterministic blueprints around agent execution are the clearest operational example of this pattern. The workflow below adapts that pattern rather than reproducing Stripe's implementation. [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

An effective coding job can be:

```text
Validate task and permissions
Provision clean environment at a recorded commit
Gather authorized task context
Agent: investigate and implement
Runner: execute required checks
Agent: repair bounded failures
Runner: collect evidence and enforce budgets
Publish branch/PR or explicit blocked result
Human / protected workflow: authorize integration and release
```

The runner must report failed or unexecuted checks as such. "The agent says it ran tests" is not equivalent to a recorded runner result.

## 6. A practical task-to-production workflow

### 6.1 A task contract

Use a lightweight contract instead of a giant up-front specification. For a meaningful change, capture:

The following is this report's template, informed by bounded delegation [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), acceptance scenarios [S16](https://factory.strongdm.ai/), and outcome-based evaluation [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

```text
Problem: whose workflow is broken or missing?
Evidence: customer report, reproduction, telemetry, or product hypothesis
Outcome: what observable behavior should change?
Acceptance: examples, counterexamples, and important edge cases
Scope: what must not change?
Risk: data, permissions, money, external actions, migration, availability
Checks: executable validation and any independent acceptance check
Owner: accountable engineer and required domain reviewer
Release: flag/canary plan, observation window, rollback or recovery
Budget: time/cost/retry limit and escalation condition
```

For a trivial typo, this can be a few sentences. For a tenant-isolation change, it should include explicit negative tests and an authorization review.

**Example:** "Add project export" is weak. Better: "An authorized project admin can export only that project's records; a member and a different tenant cannot. Exports must not contain deleted records or secrets. Large exports run asynchronously, with status and a retriable failure path. Confirm deletion/expiry behavior and file-access authorization."

### 6.2 Match the mode to the uncertainty

| Work | Preferred mode | Why |
|---|---|---|
| Product ambiguity or new interaction design | Human + agent exploration | Acceptance is not yet sufficiently clear |
| A reproducible bounded bug | Agent implementation with a test-first reproduction | Success is executable |
| A routine migration with known semantics | Deterministic codemod first; agent for exceptions | Avoid unnecessary stochastic changes |
| A cross-cutting architectural change | Human-led design, staged implementation | Requires tradeoffs, sequencing, and compatibility decisions |
| Incident diagnosis | Read-only agent investigation with an incident commander | Speed matters, but production authority must remain controlled |
| A low-risk mechanical cleanup | Bounded background task | Low interaction need and inexpensive validation |

Do not force a planning phase onto every small task. Do not start a large autonomous build when the product question is still unresolved.

The workflow-versus-agent distinction is developed in Anthropic's effective-agents guidance [S27](https://www.anthropic.com/research/building-effective-agents); the exact mode choices in this table are recommendations from this synthesis.

### 6.3 Implementation and review

The implementation agent should locate prior art, inspect the actual system, make a coherent change, and run the narrowest meaningful checks before escalating to broader validation.

Its handoff should include:

- What changed and which requirement it addresses.
- The exact base commit and resulting branch/commit.
- Checks actually executed and their results.
- UI or runtime evidence when relevant.
- Known gaps, failed checks, and behavior not exercised.
- Risk, migration, and rollback notes appropriate to the change.

For the handoff and evidence pattern, compare Anthropic's long-running-agent guidance [S06](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents), its session architecture [S07](https://www.anthropic.com/research/managed-agents), and Stripe's PR-based workflow [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2).

The reviewer checks **intent, correctness, boundaries, and operability**, not whether the generated code reads confidently. Agent review can help find issues and prepare a summary, but a second invocation of the same model is not independent assurance by itself.

A reviewer needs the original task contract and access to evidence, not only the author's explanation. For high-risk changes, inspect the implementation directly and probe negative cases.

Begin with the behavioral change, affected boundaries, and missing evidence; then inspect the relevant files and code. Do not allocate attention from the model's self-reported confidence. A review requirement should buy something concrete: detection of an untested permission failure, domain validation, design coordination, or shared operational understanding. If it only duplicates a reliable mechanical check, simplify it for the eligible class rather than preserving ceremony. The proposed trust-calibrated workflow is promising design research, not a proven replacement for review. [S38](https://doi.org/10.4230/LIPIcs.ESEM.2026.89)

### 6.4 Merge and release

Use protected branches, required checks, and a merge queue when concurrent changes make pre-merge results stale. The worker must not be able to change branch rules or approve its own protected changes.

Build a versioned release artifact once and promote that artifact. Keep deployment credentials out of ordinary coding workspaces. Use gradual exposure and a monitored observation window proportional to risk.

A rollback should not be imaginary. Database changes may be irreversible; use expand/contract migrations and a tested recovery or forward-fix plan. A feature flag does not undo a destructive write.

**Further reading:** Google's [release-engineering chapter](https://sre.google/sre-book/release-engineering/) covers reproducible builds, access-controlled release operations, artifact identity, canarying, and rollback. This report's migration-specific advice is an engineering recommendation, not a claim that a flag can recover data. [S44](https://sre.google/sre-book/table-of-contents/)

### 6.5 Close the loop

After release, the owner checks the intended behavior and relevant guardrails. If customer impact is worse, revert/disable/repair according to the pre-agreed plan.

When a failure repeats, choose the correct durable response:

| Repeated failure | Better response than a stronger prompt |
|---|---|
| Wrong module/layer | Architectural check with actionable error output |
| Forgotten edge case | Regression/acceptance case |
| Repeated setup confusion | Environment or bootstrap fix |
| Missing domain rule | Authoritative documentation plus executable validation if feasible |
| Unsafe tool action | Authorization/policy boundary outside the model |
| Long unproductive loops | Budget, escalation rule, and failure classification |

This feedback-loop synthesis is informed by OpenAI's recurring cleanup/checks [S01](https://openai.com/index/harness-engineering/), Claude Code's executable verification guidance [S05](https://code.claude.com/docs/en/best-practices), and Shopify's production-derived evaluation lessons [S15](https://shopify.engineering/building-production-ready-agentic-systems).

## 7. A risk-based autonomy policy

Autonomy should be earned **per task class and tool capability**, not granted because an engineer likes a model.

| Class | Examples | Default implementation authority | Integration / release |
|---|---|---|---|
| A: low-risk mechanical | Documentation links, formatting, generated artifacts with deterministic provenance | Unattended in a restricted environment | Auto-merge only for explicitly allowlisted changes with required checks and auditability |
| B: ordinary bounded behavior | Small UI fix, routine API feature without new sensitive authority | Unattended implementation; no production credentials | Human review and normal protected delivery |
| C: sensitive or cross-cutting | Authentication, tenant isolation, billing, schema migration, public contract change | Design checkpoint, constrained implementation, independent checks | Named domain reviewer; staged rollout and recovery plan |
| D: irreversible / externally consequential | Destructive production operations, money movement, bulk customer communications | Agent may propose and gather evidence; execution through separately authorized tools | Explicit approval scoped to the exact action; stronger controls or prohibition where appropriate |

These are recommended categories, not an industry standard. They adapt bounded agent delivery [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) and risk/authority guidance [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook); those sources do not prescribe this exact four-class policy. Classify combinations, not filenames alone: a "documentation" change can alter a release script or embed malicious agent instructions.

**Promotion requirements:** representative task history, acceptable escaped-defect/revert rates, independent evidence, bounded blast radius, tested recovery, and a named policy owner.

**Demotion triggers:** unexplained failures, attempts to bypass tests or permissions, new tool authority, changed data sensitivity, or a materially changed model/harness. A model upgrade does not automatically inherit every prior autonomy permission.

Auto-merge is not auto-deploy, and auto-deploy is not permission for an agent to perform arbitrary production actions.

## 8. Verification: make correctness cheaper than confidence

### 8.1 Build a layered evidence system

| Layer | Purpose | Typical examples | Limitation |
|---|---|---|---|
| Static checks | Cheap structural feedback | Types, lint, formatting, import rules, secret scans | Cannot establish runtime semantics |
| Unit / property tests | Domain invariants | Money arithmetic, state transitions, parsers, idempotency | Can mirror implementation assumptions |
| Integration / contract tests | Real boundaries | Database constraints, SDK compatibility, API responses | Environment coverage is incomplete |
| Behavioral acceptance | User-visible outcome | Export permissions, checkout journey, failed retry | Needs realistic setup and meaningful assertions |
| Independent holdouts | Detect overfitting and test rewriting | Protected evaluator jobs, external scenario runner | Secrecy alone does not make a test fair or sufficient |
| Human/domain review | Intent and nuanced judgment | Security design, usability, legal implications | Expensive and variable |
| Production observation | Real distribution and operational behavior | Canary outcomes, SLOs, user reports, rollback signals | Detects harm after some exposure |

Keep these complementary. "We use evals" is not a reason to remove authorization tests; "all tests pass" is not a claim that an AI assistant is useful.

**Basis for the layers:** NIST's secure-development framework provides broad SDLC guidance [S43](https://csrc.nist.gov/pubs/sp/800/218/final); Anthropic discusses complementary graders and agent outcomes [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents); Shopify describes calibrated evaluations and reward hacking [S15](https://shopify.engineering/building-production-ready-agentic-systems). The layer table is this report's organization of those concerns.

### 8.2 Independent does not mean mysterious

The implementation should know the behavior contract. It need not see every held-out fixture or have permission to change the evaluator.

For example, describe tenant isolation explicitly, then test many tenant/role combinations outside the writable workspace. Do not fail an otherwise correct implementation because a secret test assumed an undocumented filepath or exact phrasing.

Protect changes to test harnesses, CI permissions, evaluator code, and security-sensitive configuration. A change that deletes coverage or weakens an assertion requires explicit review rather than being accepted as "fixing the tests."

Distinguish three kinds of independence: **authority** (the worker cannot alter the gate), **reasoning/evidence** (the check is not merely repeating the implementer's assumptions), and **environment** (the scenario represents the deployed system). A protected runner provides the first, not automatically the other two. Using a different model also does not establish independent errors.

Audit evaluators with known bad implementations, legitimate alternative solutions, and expert review of disputed failures. Keep a fresh validation set separate from cases repeatedly used to tune prompts and harnesses; repeated feedback can contaminate a nominal holdout. A failed hidden test should be appealable against the documented contract. OpenAI's audit illustrates why a deterministic, hidden check can still reject a correct solution. [S40](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)

### 8.3 Simulators and digital twins

Start with the smallest simulator that exercises an expensive or dangerous boundary. For a third-party billing service, that may mean realistic retries, duplicate webhooks, expired credentials, partial failures, and idempotency behavior, not a complete clone of the vendor.

Validate the simulator against official schemas, SDKs, recorded sanitized behavior, and a small real sandbox contract suite. Periodically check for drift.

The failure to avoid is **a correct simulation of the team's mistaken understanding**. Both the implementation and the simulator can agree while production disagrees.

StrongDM's Digital Twin Universe is the lighthouse example [S16](https://factory.strongdm.ai/) [S17](https://simonwillison.net/2026/Feb/7/software-factory/); Shopify's Sidekick account also describes simulation and its relationship to evaluation [S15](https://shopify.engineering/building-production-ready-agentic-systems). The small billing simulator above is an illustrative design, not a reported deployment.

### 8.4 Suggested feedback-loop targets

These are initial service objectives to tune locally, not measured industry requirements:

| Signal | Starting target | If it is missed |
|---|---|---|
| Common format/static checks | Seconds, ideally below 30 seconds | Cache or narrow scope; do not make every edit wait on broad CI |
| Focused domain checks | Around 1-2 minutes | Improve fixtures and dependency isolation |
| Ordinary change CI | Aim for roughly ten minutes or less | Profile the bottleneck; separate fast required signal from slower suites |
| Fresh task environment | Aim for a few minutes or less | Automate setup first; prewarm when frequency justifies it |
| Review queue | No persistent growing backlog | Reduce task admission/concurrency before adding generators |

Do not hit a latency target by deleting the only meaningful correctness check. Measure flakiness separately and repair it; repeated retries must not disguise an unreliable test suite.

## 9. Additional requirements when the product itself uses AI

### 9.1 Start simpler than "multi-agent"

Choose the least complex system that meets the need:

| Product problem | Starting approach |
|---|---|
| Structured extraction or classification | One model call with schema validation and evaluation |
| Answering over documents | Retrieval plus an evaluated response path, with provenance and access checks |
| A predictable business process | A deterministic workflow with narrow model steps |
| Open-ended tool-based problem solving | A bounded agent loop |
| Independent research or genuinely separable expertise | Multiple agents only after evaluating a simpler baseline |

Anthropic's effective-agents guidance and Shopify's Sidekick account converge on starting with simple, composable systems. Additional agents add communication, coordination, latency, cost, and failure modes. [S15](https://shopify.engineering/building-production-ready-agentic-systems) [S27](https://www.anthropic.com/research/building-effective-agents)

### 9.2 Treat the deployable unit as more than a model name

Version the **model identifier, prompts, tool schemas, retrieval configuration, policies, memory behavior, and harness** together. Record the evaluated combination.

Avoid silently changing the default model behind a production feature when behavior is material. If a provider's alias moves, detect it and run regression/canary checks. Preserve the last known acceptable configuration where the provider allows it.

If using a fallback provider/model, evaluate it. A response-shaped fallback that is materially worse, bypasses data policy, or takes a risky action is not graceful degradation.

These configuration-management recommendations follow from evaluating the whole agent system, as discussed in Anthropic's evaluation guidance [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) and Shopify's production account [S15](https://shopify.engineering/building-production-ready-agentic-systems). The specific version record proposed here is a synthesized implementation checklist.

### 9.3 Build evaluations from real work

Anthropic recommends starting with a small set of realistic tasks, including actual failures; its guidance suggests 20-50 can be a useful initial seed. This is a bootstrap size, not evidence that fifty cases can establish rare-event safety. [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)

For a small team:

1. Write concrete success and failure examples with a product/domain owner.
2. Include ordinary, difficult, ambiguous, and intentionally unauthorized requests.
3. Preserve a development set and a held-out evaluation set.
4. Prefer deterministic final-state checks where possible.
5. Add calibrated model grading for genuinely subjective properties.
6. Repeat trials to expose instability.
7. Inspect failed and unexpectedly successful traces.
8. Convert production failures into new cases without exposing private data unnecessarily.

A useful task record includes:

```text
Task ID and category
Input and environment fixture
Authorized user/tenant/role
Expected outcome and forbidden outcomes
Deterministic assertions
Rubric for subjective quality, if any
Latency/cost budget
Model, prompt, tool, policy, and dataset versions
Human label and adjudication notes
```

### 9.4 Grade outcomes, not claims

An agent saying "the invoice was corrected" is not evidence that the invoice exists with the right amount and audit trail.

For state-changing tasks, inspect database state, external sandbox state, permissions, and duplicate-action behavior. For research tasks, inspect source support, coverage, citation fidelity, and unsupported assertions. For UI tasks, inspect behavior and accessibility as well as screenshots.

Use separate grading dimensions: task completion, factual correctness, authorization, side-effect safety, communication quality, latency, and cost. A high average score must not compensate for an unauthorized transaction.

For outcome-versus-transcript evaluation and grader choice, see Anthropic's agent-evaluation guide [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents); for production judge calibration, see Shopify's Sidekick account [S15](https://shopify.engineering/building-production-ready-agentic-systems).

### 9.5 Handle stochasticity and statistical uncertainty honestly

Report first-attempt success, repeated-attempt success, and consistency separately. Anthropic distinguishes "at least one success in several trials" from "all trials succeed." The former can help developer tools; the latter matters more when each customer expects a reliable action. [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)

With independent attempts and constant per-attempt success, a 90% success rate would yield only about 59% probability that all five attempts succeed. Real attempts can be correlated, so do not treat that simple illustration as a production reliability estimate.

Use paired comparisons on the same task set when comparing candidates. Show task-level distributions, sample sizes, and uncertainty. Small score differences on a tiny suite are not a decisive model ranking.

Keep critical security constraints as release gates, not weighted average quality points. Expand test coverage for high-impact rare failures; observe that zero failures in a small sample does not establish zero risk.

### 9.6 Calibrate model judges

Shopify describes learning that a vague "rate this 0-10" judge was insufficient. It used product-expert labels, agreement measures, and iterative judge calibration. It also documents reward hacking. [S15](https://shopify.engineering/building-production-ready-agentic-systems)

For a small team, use explicit rubrics, examples of pass/fail/borderline cases, blinded comparison when appropriate, and a human-adjudicated sample. Check false acceptance and false rejection separately.

Protect against verbosity and style bias, evaluator prompt injection, familiarity with training examples, and a judge rewarding the same misconception as the generator. Another model family can add diversity but does not guarantee independence.

Record disagreements and revise an ambiguous task rather than repeatedly tweaking the prompt to satisfy an unreliable grader.

### 9.7 Retrieval, memory, and data

Start with the retrieval method that actually works: ordinary search and metadata filters may be enough before a vector database is justified.

Enforce access controls at retrieval and tool execution, not just in the prompt. Attach provenance, document version, and freshness where relevant. Evaluate whether the right material was retrieved separately from whether the answer was good.

Treat memory writes as durable data changes. Store source, scope, owner, timestamp, and retention. Do not let an untrusted conversation silently update shared instructions or global memory.

Keep customer data out of general examples, shared agent memories, and evaluation sets unless approved and appropriately de-identified. Account for deletion requests in traces, caches, datasets, and derived memory.

**Further reading:** Anthropic on just-in-time context and retrieval [S32](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), Willison on untrusted content plus private data and external communication [S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/), and OWASP/NIST on broader agent and data-risk management [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook). The retention and memory fields above are this report's proposed controls, not a legal compliance determination.

### 9.8 Fine-tuning and research staffing

Do not begin with fine-tuning because the product is "AI-native." First characterize failures in retrieval, instructions, tool design, data, and evaluation.

Fine-tune when repeated evidence shows a stable capability or behavior gap, you have lawful high-quality data, and the measured gain justifies training/serving/maintenance complexity. Retain holdouts and compare against a stronger general model and a better workflow.

Hire specialized ML/research capability when model/data optimization is a core differentiator or a demonstrated bottleneck, not merely because the application calls an LLM.

## 10. Security, privacy, and governance

This section is system-design guidance, **not a security audit of the repository or the named companies**.

### 10.1 The critical threat model

Coding and product agents can combine private data, untrusted input, and external communication. Simon Willison's "lethal trifecta" describes why that combination creates an exfiltration risk through indirect prompt injection. OWASP's agentic guidance and NIST's risk framework provide broader organizing structures. [S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)

Untrusted content includes issues, dependency documentation, web pages, logs, PR comments, retrieved documents, emails, images, and tool output. Helpful-looking instructions embedded there do not become authorized policy.

### 10.2 Minimum controls

| Risk | Required design response |
|---|---|
| Prompt injection changes tool behavior | Treat source content as data; authorize actions outside the model |
| Coding agent steals secrets | Keep production and orchestration secrets outside the worker; use short-lived scoped access |
| Agent exfiltrates source/customer data | Approved providers, data classification, egress restrictions, narrow tool access |
| Agent broadens its own authority | Protected policy/configuration; worker cannot edit its runtime permissions or branch rules |
| Malicious dependency or tool | Review provenance, pin versions, scan packages, restrict install sources |
| Cross-tenant leakage | Server-side authorization and tenant-scoped retrieval/tool calls |
| Evaluation tampering | Separate evaluator identity/write boundary, review harness changes |
| Unauthorized external side effect | Preview/propose/approve/commit flow for sensitive actions |
| Runaway work or cost | Enforced time, token/spend, concurrency, and child-task limits |
| Shared-memory poisoning | Provenance, scope, review, expiry, and deletion controls |

Prompt-injection detection and safety classifiers can be useful layers. They are not a substitute for authorization or a proof that a broadly privileged agent is safe.

The control table is an engineering synthesis informed by OWASP's agentic risk guidance [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), NIST AI RMF [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook), NIST SSDF [S43](https://csrc.nist.gov/pubs/sp/800/218/final), and the concrete threat model in [S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). It is not a verbatim control mapping or a certification checklist.

### 10.3 Separate control plane from execution plane

For longer-running or higher-risk systems, keep the durable session, credential brokerage, and policy enforcement outside the environment executing generated code. Anthropic and Shopify describe versions of this separation. [S07](https://www.anthropic.com/research/managed-agents) [S13](https://shopify.engineering/under-the-river)

A minimal small-team implementation can use a managed runner and ordinary durable storage. It does not require a bespoke distributed agent operating system.

Be precise about what a proxy protects. Hiding a raw token does not make every action safe: the proxy must still enforce which resource, operation, tenant, and destination the session can use.

### 10.4 Treat AI-generated dependencies and code as a supply-chain input

Require dependency manifests and lockfiles, secret scanning, dependency vulnerability checks, licensing review appropriate to the product, and provenance for release artifacts. Prefer trusted package registries and approved connectors.

Agents can invent packages or recommend a lookalike. Verify package identity and actual API behavior before adoption.

Track who requested work, which agent/runtime produced it, and which commit contains it. Attribution supports diagnosis; it does not shift legal or operational responsibility away from the organization.

For the secure-development and software-supplier basis, see NIST SSDF's publication and downloadable framework [S43](https://csrc.nist.gov/pubs/sp/800/218/final). The AI-specific implementation details here are recommendations layered onto that broader SDLC guidance.

### 10.5 Write a short, usable AI policy

Specify approved products/providers, allowed data classes, retention/training settings, regional requirements, permitted integrations, tool-installation rules, and escalation paths.

Examples:

- Public documentation may use the approved general service.
- Confidential source may use approved enterprise tooling under the organization's contractual settings.
- Regulated/customer data requires the specific approved path and cannot be copied into an arbitrary chat.
- Production write access is not available in normal implementation sessions.
- Policy exceptions require a named owner and expiry.

Get qualified advice for legal and regulatory applicability. NIST's AI RMF is voluntary guidance, not a compliance certificate. [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)

## 11. Observability and operations

### 11.1 Instrument the product and the engineering process

Product telemetry should include user-journey success, errors, latency, saturation, deployment version, tenant-safe correlation, and the relevant business outcome.

Agent telemetry should include:

| Category | Useful fields |
|---|---|
| Identity and provenance | Task/session ID, owner, base commit, model/harness/prompt/tool versions |
| Execution | Tool calls and results, retries, timeouts, permission denials, lifecycle state |
| Evidence | Checks run, artifacts, evaluator versions, final-state outcome |
| Economics | Tokens, model charges, sandbox/CI cost, total elapsed time, human intervention |
| Safety | Sensitive tool requests, policy decisions, attempted prohibited actions |

Store observable interaction records and tool evidence as appropriate; do not assume hidden internal model reasoning is available or necessary. Apply redaction, access control, and retention. Logs are another sensitive data store.

**Further reading:** Google's [monitoring chapter](https://sre.google/sre-book/monitoring-distributed-systems/) explains service signals and alert quality [S44](https://sre.google/sre-book/table-of-contents/); Anthropic and Shopify describe agent-session state and evidence [S07](https://www.anthropic.com/research/managed-agents) [S13](https://shopify.engineering/under-the-river); Anthropic's evaluation guidance explains why trajectories and final outcomes both matter [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents).

### 11.2 Durable execution and side effects

Long-running jobs need persisted state, cancellation, timeout handling, retry policy, and crash recovery.

Do not promise exact deterministic replay of a probabilistic model interacting with a changing world. Aim for **reconstructable evidence and controlled re-execution**.

Before retrying a state-changing tool, reconcile whether the original action succeeded. Use operation IDs and idempotency keys; separate "request accepted" from "action completed." A crash after an external action but before a local event write is a classic duplicate-action risk.

Anthropic's durable-session architecture [S07](https://www.anthropic.com/research/managed-agents) and Shopify's session/harness/sandbox separation [S13](https://shopify.engineering/under-the-river) are concrete system references. The retry/reconciliation rules above are this report's reliability recommendations, not a guarantee of exactly-once behavior from either platform.

### 11.3 Release gates and incident response

For ordinary product changes, define success/error signals and rollback criteria before shipping. For AI changes, include behavior and authorization metrics, not only HTTP availability.

Agents may summarize incidents, correlate telemetry, draft fixes, and propose runbook actions. The incident commander retains authority over consequential production changes unless a narrowly approved remediation policy already exists.

After an incident, identify whether the failure came from specification, implementation, evaluator, environment, tool, model behavior, authorization, or release design. "The AI hallucinated" is not an adequate root cause.

For operational foundations, read Google's [incident-management chapter](https://sre.google/sre-book/managing-incidents/) and [postmortem chapter](https://sre.google/sre-book/postmortem-culture/). The agent-specific failure classification above adapts those practices. [S44](https://sre.google/sre-book/table-of-contents/)

## 12. Toolchain: buy the commodity layers, own the differentiating controls

The following is a selection framework, not a benchmark ranking. Vendor availability, enterprise controls, and pricing change; verify them at purchase.

| Layer | Sensible small-team starting point | Build/customize when |
|---|---|---|
| Interactive coding | A supported editor/CLI agent such as Copilot, Claude Code, Codex, or Cursor | Repository guidance and thin integrations are insufficient for a demonstrated need |
| Background implementation | A hosted coding-agent capability or a managed sandbox plus existing runtime | Unique environment/context requirements materially limit results |
| Source control / CI | Existing Git host and CI, protected branches, standard job runners | A real scale or compliance requirement exceeds the platform |
| Environments | Containers/devcontainers, managed environments, or an established reproducible toolchain | Setup latency or isolation requirements justify additional work |
| Product AI orchestration | Direct API calls or a thin, understandable SDK | Durable state, retries, complex workflows, or portability needs are real |
| Evaluation | Tests plus a task dataset and a lightweight runner; managed/open-source eval tools if useful | Repeated eval operations require better collaboration or scale |
| Telemetry | Existing error tracking and OpenTelemetry-compatible observability | Specific trace/data requirements are unmet |
| Context / integration | Repository docs and selected existing APIs/CLI tools; MCP where valuable | Repeated integration work justifies a shared adapter |
| Retrieval | Existing database/search with access-aware filtering | Measured retrieval quality or scale requires a specialist index |

A tool purchase should pass a real task trial, data/security review, export/exit review, and cost review. Do not compare products only through demo videos or benchmark leaderboards.

This selection framework synthesizes workflow/evaluation guidance [S27](https://www.anthropic.com/research/building-effective-agents) [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), context guidance [S32](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents), and fully loaded ROI considerations [S25](https://dora.dev/ai/roi/report/). It is not a tested product ranking or a source-prescribed shopping list.

### 12.1 A practical bake-off

Choose a representative backlog slice: a familiar bug, an unfamiliar-codebase task, a UI change, a test repair, and a small cross-cutting change. Add adversarial/authorization tasks if tool power makes them relevant.

Use the same starting commits and acceptance criteria. Record model/tool versions, human intervention, elapsed time, review minutes, defect/rework outcomes, and cost. Randomize or counterbalance task/tool order where practical to reduce learning effects.

A small bake-off is directional, not a statistically decisive product ranking. Keep raw failures, not just best runs.

Do not let a participant solve the same issue twice and treat the second attempt as an independent comparison: remembered solutions contaminate the result. Use different, comparable tasks, counterbalanced assignments, and multiple people where feasible. Preserve the current capable copilot workflow as a baseline, not just manual coding. Distinguish a tool comparison from a bundle comparison when model, environment, or task allocation also changes.

For examples of experimental design and its pitfalls, compare METR's original trial and follow-up [S21](https://arxiv.org/abs/2507.09089) [S22](https://metr.org/blog/2026-02-24-uplift-update/) with Chen et al.'s within-participant tool comparison [S42](https://arxiv.org/html/2507.08149v2). The proposed local bake-off is a practical adaptation, not a replication of any one study.

### 12.2 Avoid premature multi-provider infrastructure

A second approved provider can help with resilience and comparison, but routing, credentials, feature differences, caching, and regression testing add work.

Keep interfaces replaceable and records exportable. Add sophisticated routing when measured cost/reliability gains justify its maintenance. Different models can be appropriate for different tasks; no model ranking in an early-2026 case study should be treated as permanent.

## 13. Parallelism, work in progress, and orchestration

<keyidea>The right number of agents is constrained by how much independent work the team can specify, verify, integrate, and operate, not merely by how many sessions it can launch.</keyidea>

Start with one implementation task per engineer and, where useful, a separate bounded research or mechanical task. This is a conservative starting policy, not a claim that two sessions is optimal.

Benchmark research supports task-dependent coordination rather than monotonic gains from agent count. Its large positive and negative effects are not transferable estimates of team throughput. Compare one and several agents on the actual task class, holding the outcome standard and resource budget reasonably comparable; include integration and orchestration costs. For a cheap, independent batch, more concurrency can be sensible even in a tiny human team. [S37](https://arxiv.org/html/2512.08296v3)

Increase concurrency when:

- Tasks have clear boundaries and do not fight over the same files or interfaces.
- Environments and state are isolated.
- Review wait and rework do not grow.
- Required checks remain reliable and affordable.
- Someone owns integration of the overall outcome.

For dependent work, sequence interfaces and compatibility changes. Parallel agents implementing contradictory assumptions create expensive integration work even when Git merges cleanly.

**When multiple agents help:** independent research, independent modules with explicit contracts, alternate candidate solutions that can be cheaply evaluated, focused read-only review, and broad mechanical changes split into independent slices.

**When they hurt:** a single continuous debugging trace, highly shared state, unclear requirements, a tiny edit, or a situation where every agent must rediscover the same context.

Set hard maximum child tasks, concurrency, runtime, and spend. Do not copy a case study's faith that models will self-limit.

## 14. Metrics: a balanced engineering scorecard

### 14.1 North star and guardrails

The north star is **valuable user outcomes delivered reliably at sustainable total cost**. It is not one perfect scalar. Use a small balanced set:

| Dimension | Metric | Interpretation / caution |
|---|---|---|
| Product | Task success, activation, retention, revenue or customer-specific outcome | Choose the measure tied to the actual product hypothesis |
| Flow | Change lead time, deployment frequency, work-in-progress age | Faster is useful only with stable quality |
| Stability | Change failure rate, recovery time, reverts, escaped defects | Segment by severity and risk class |
| Review | Queue wait, review minutes, number of revision rounds | Detects shifted human burden |
| Reliability | User-journey SLOs, error-budget consumption | A coding speedup does not justify degrading service |
| Agent effectiveness | Useful accepted outcomes per attempted task; abandonment and intervention rates | Include failed runs in the denominator |
| Economics | Fully loaded cost per accepted outcome and per reliable product task | Include human review, retries, CI, and environment cost |
| Maintainability | Recurring architecture violations, duplicate logic, dependency growth, repair burden | Avoid simplistic lines-of-code targets |
| Team health | Interruptions, cognitive load, learning, on-call burden | Prevent apparent gains funded by burnout or deskilling |

Agent-written/coauthored percentages are descriptive adoption measures. They are not individual performance targets.

**Basis for this synthesized scorecard:** DORA's delivery/stability findings and ROI framework [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S24](https://research.google/pubs/dora-ai-capabilities-model/) [S25](https://dora.dev/ai/roi/report/), the code-to-release attenuation reported in [S36](https://www.nber.org/papers/w35275), maintainability evidence [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3), and observed supervision costs [S39](https://arxiv.org/html/2605.29442v2). The exact set of metrics is a recommendation, not a universally validated composite score.

### 14.2 Measure at the right level

Use team-level improvement, not surveillance-based engineer rankings. Task difficulty, domain risk, review work, and enabling work vary too much for raw individual counts to be fair.

Segment greenfield and legacy work; feature, bug, migration, and incident tasks; low and high risk; interactive and unattended modes. Otherwise a changing task mix can look like a model improvement.

### 14.3 A local measurement plan

Gather an initial baseline over a few weeks of ordinary work. Then pilot one intervention, such as a hosted agent with a complete environment, on an eligible task class.

Compare matched task categories and use random assignment where practical and acceptable. Track unfinished/abandoned tasks and at least a short post-merge observation window. Do not stop measurement at "PR opened."

For a small team, sample sizes will often be too low for strong causal claims. Report directional evidence and uncertainty. Avoid treating "not statistically significant" as proof of no effect.

If review time rises enough to erase implementation savings, fix the workflow or narrow the eligible task class rather than forcing adoption.

Predeclare the decision, not just the measurement: which task class, baseline, learning allowance, quality guardrails, recurring cost ceiling, and stop/scale rule? Track active human time separately from wall-clock delay; a slow unattended run can save attention, while apparent parallelism can create expensive interruptions. Record unfinished work and time spent correcting prompts or verifying the agent's claims. [S39](https://arxiv.org/html/2605.29442v2)

Follow a sample of accepted changes through a later modification or operational event. An improvement that merely postpones repair or shifts work to a different person is not a net team gain. Static warnings are diagnostic signals, not measured lifetime costs; supplement them with observed modification and repair burden. [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3)

## 15. Economics and budgeting

### 15.1 Count the complete system

Include subscriptions, API usage, sandbox time, CI, storage/telemetry, evaluator calls, integration maintenance, training, review, rework, and incidents.

The cheapest model per token is not necessarily the cheapest way to finish a task. A more capable model may require less repair; an expensive model may be wasteful for a deterministic transformation.

Distinguish:

- **Cash savings:** actual spending avoided.
- **Capacity gains:** engineering time available for other work.
- **Revenue gains:** customer/business outcomes supported by faster learning or delivery.

Do not count the same saved hour as both reduced payroll and extra feature capacity.

For the distinction between modeled ROI and realized outcomes, see DORA's financial framework [S25](https://dora.dev/ai/roi/report/) alongside the downstream-output findings in [S36](https://www.nber.org/papers/w35275). The cost inventory and worked scenarios here are this report's accounting examples.

Capacity also has a **conversion problem**. Fragmented minutes between interventions may not become usable engineering time; usable time may not become valuable shipped work if demand, integration, or adoption is the constraint. Track what the released capacity actually funds. If it does not displace a cost or advance an important outcome, assigning it a salary-equivalent value overstates realized return. [S36](https://www.nber.org/papers/w35275) [S39](https://arxiv.org/html/2605.29442v2)

### 15.2 An illustrative five-engineer calculation

This is deliberately a transparent scenario, **not a price quote or forecast**.

Assume $200,000 fully loaded annual cost per engineer and 220 working days: approximately $909 per engineer-day.

Suppose a pilot saves eight net engineer-days per month across the team **after task-level review and rework**, worth about $7,272 in capacity. Suppose ongoing platform/training work consumes another two days, about $1,818, and subscriptions, usage, and extra CI total $3,000.

That leaves approximately **$2,454 per month of net capacity value**, before amortizing initial setup and any incremental incident cost. It is not $2,454 of cash saved unless spending actually changes.

If only four net days are saved, the same cost structure loses capacity value. If customer learning improves materially, that may still justify the investment, but measure that separately rather than hiding a negative operating result.

Now include an illustrative **20 engineer-days of initial setup**, approximately $18,180, amortized over six months at roughly $3,030 per month:

| Net task-level days saved per month | Capacity value at about $909/day | After 2 recurring system days and $3,000 usage cost | After monthly setup amortization |
|---|---|---|---|
| 4 | $3,636 | -$1,182 | -$4,212 |
| 8 | $7,272 | $2,454 | -$576 |
| 12 | $10,908 | $6,090 | $3,060 |

These are rounded sensitivity scenarios, not measured results. With these assumptions, the apparent eight-day win is slightly negative after setup. If only half of those eight days become useful capacity, the modeled result falls to about -$4,212. If much cheaper existing tools deliver the gain without substantial setup, economics improve sharply. Give shared infrastructure credit for genuine non-AI benefits rather than charging everything to AI; do not count those benefits twice.

The alternative is not "do nothing." Compare the same 20 days and ongoing budget with simpler CI, removing product scope, customer discovery, reducing operational toil, or a specific domain hire. A J-curve is possible, but it does not establish that the investment will ever repay.

### 15.3 Budget policies

Begin with a bounded discretionary pilot budget and visible per-task costs. Set soft alerts below hard caps, with explicit escalation for valuable long runs. Record why a task exceeded budget.

Reserve funding for environment quality and evaluation, not only model seats. Avoid token-spend quotas: consuming more inference is not an engineering outcome.

## 16. Day-to-day and week-to-week operation

| Cadence | Practice | Intended output |
|---|---|---|
| Daily | Check customer/production signals and the review queue before launching more work | Work admission aligned to current bottlenecks |
| Per meaningful task | Agree on acceptance, risk, owner, and evidence | A bounded contract, not a vague instruction |
| Weekly | Review a small sample of successful, failed, abandoned, and expensive agent runs | One or two concrete system improvements |
| Weekly | Demonstrate a shipped user outcome | Product feedback rather than a code-output celebration |
| Weekly | Check flaky CI, stale dependencies, noisy alerts, and architectural drift | A small maintenance queue |
| Every few weeks | Compare tool/model/harness changes on the local task suite | Evidence-backed upgrade decisions |
| Monthly or risk-triggered | Review permissions, providers, retention, cost, and autonomy classes | Current controls and accountable exceptions |

Keep the process proportional. A five-person team does not need a standing meeting for every row. Many checks can be asynchronous and combined.

Shared learning should produce reviewed improvements, not an ever-growing prompt diary. Delete obsolete instructions and tests that assert implementation trivia rather than behavior.

This cadence adapts shared learning and verification practices [S04](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/) [S05](https://code.claude.com/docs/en/best-practices) [S13](https://shopify.engineering/under-the-river) [S15](https://shopify.engineering/building-production-ready-agentic-systems) and operational learning guidance [S44](https://sre.google/sre-book/table-of-contents/). The daily/weekly/monthly frequencies are proposed management choices, not frequencies established by those sources.

## 17. A 90-day implementation roadmap

The timeline is illustrative. Progress through gates based on evidence, not the calendar. The original sequence waited until the second month to pilot delegation; that is too slow for a team that can safely learn from a real bounded task immediately. Baseline collection and targeted improvements can proceed alongside the experiment.

| Phase | Deliverables | Exit criteria | Owner |
|---|---|---|---|
| Days 1-7: authorize and try | Approved tool/data boundary, one real eligible task, existing checks, named owner, baseline definition and pilot budget | A safe attempt produces inspectable evidence; no mandatory platform build first | Lead + task owner |
| Days 8-30: learn and repair | Comparable baseline/pilot tasks; fix observed setup/check problems; include failed runs, review time, cost, and initial production follow-up | Evidence identifies a useful task class, or the team narrows/stops the intervention | Task owners + system owner |
| Days 31-60: harden a demonstrated win | Reliable isolation for unattended runs, missing acceptance cases, budget/retry limits, targeted shared procedures | Recurring benefits survive the extra controls and do not breach quality guardrails | System owner + product/domain partner |
| Days 61-90: scale, redirect, or retire | Expand only the successful classes; test another binding constraint; remove unused tools and scaffolding | The team can explain gains, losses, full cost, and why this beats the alternative investment | Whole team |

For an AI product, build the initial eval set during the first phase and make model/prompt/tool changes use it before broad release.

The roadmap combines a learning-cost allowance [S25](https://dora.dev/ai/roi/report/), bounded unattended delivery [S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), and early outcome-based evaluation [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Its dates and gates are this report's implementation proposal, not a published 90-day standard.

### 17.1 Greenfield variant

Choose a stack the team can operate, establish boundary contracts and testability early, and make the first meaningful journey executable end to end. Do not let generation speed create an oversized architecture before customer validation.

### 17.2 Existing-codebase variant

Do not begin with a rewrite. Make setup reliable, add characterization tests around the area being changed, document dangerous legacy patterns, and pilot in one domain. Preserve compatibility and migrate incrementally.

### 17.3 Regulated/high-consequence variant

Start with read-only investigation, test generation, documentation, and constrained implementation. Keep independent authorization, audit, change approval, and domain assurance. Tool adoption cannot waive existing obligations.

## 18. Common anti-patterns and how to recognize them

| Anti-pattern | Observable symptom | Correction |
|---|---|---|
| Output theater | Lots of PRs and code, little improvement in customer outcomes | Limit work in progress; review value and reliability [S36](https://www.nber.org/papers/w35275) |
| Prompt as policy | "Never touch production" appears only in instructions | Remove production authority from the worker [S05](https://code.claude.com/docs/en/best-practices) [S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| Self-confirming tests | Agent changes the assertion to match its bug | Protect acceptance checks and review test changes [S15](https://shopify.engineering/building-production-ready-agentic-systems) [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) |
| Agent swarm by default | High token use, repeated context discovery, growing integration backlog | Return to one owner and a smaller task decomposition [S19](https://cursor.com/blog/scaling-agents) [S37](https://arxiv.org/html/2512.08296v3) |
| Context landfill | Huge rule files with conflicting/stale guidance | Minimal additional instructions, evaluated against a baseline [S32](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) [S33](https://arxiv.org/html/2602.11988v3) |
| Infinite repair loop | Repeated CI attempts with no changed hypothesis | Bounded retries and a diagnostic handoff [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) |
| Review rubber stamp | Reviewer reads only the agent summary | Review against the task and independent evidence [S38](https://doi.org/10.4230/LIPIcs.ESEM.2026.89) |
| Unbounded tool catalog | Agent chooses overlapping or overpowered tools | Curate by task, scope credentials, remove unused integrations [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) [S32](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) |
| Platform before product | Team spends months rebuilding generic agent infrastructure | Buy the baseline; build only measured differentiators; compare full costs [S25](https://dora.dev/ai/roi/report/) |
| "No humans write code" as an identity | Manual fixes avoided even during urgent recovery | Optimize outcomes; keep emergency judgment; do not generalize the factory experiment [S16](https://factory.strongdm.ai/) [S17](https://simonwillison.net/2026/Feb/7/software-factory/) |
| Simulator certainty | All scenarios pass but live integrations fail | Validate simulator fidelity against real contracts; separate scenario success from real-world assurance [S15](https://shopify.engineering/building-production-ready-agentic-systems) [S16](https://factory.strongdm.ai/) [S17](https://simonwillison.net/2026/Feb/7/software-factory/) |
| Hidden maintenance tax | Faster implementation, more on-call and repair work | Include downstream cost and stability; recognize mixed maintainability evidence [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3) |
| Automation-induced deskilling | Engineers cannot explain or debug their own changes | Deliberate comprehension and bounded apprenticeship; distinguish immediate learning evidence from long-term risk [S26](https://www.anthropic.com/research/AI-assistance-coding-skills) |
| Memory without governance | Old or malicious statements become durable team policy | Provenance, scope, review, and expiry [S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) |

These are synthesized warning patterns and proposed responses. The cited material explains the motivation or supplies a relevant example; it does not establish that every symptom has a single cause or a universally effective remedy.

## 19. Decision checklist for a small-team lead

Before scaling autonomous implementation, establish that:

The checklist below consolidates the preceding recommendations, informed by controlled integration [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), evaluation guidance [S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents), and risk/secure-development frameworks [S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) [S43](https://csrc.nist.gov/pubs/sp/800/218/final). It is not a compliance attestation or an externally validated readiness score.

- [ ] Each task has a human owner and observable acceptance criteria.
- [ ] A fresh environment can run the actual application and relevant checks.
- [ ] Parallel work isolates service/data state, not just Git files.
- [ ] The worker has no routine production write credentials or arbitrary secret access.
- [ ] Required checks run independently of the model's willingness to invoke them.
- [ ] Security-sensitive checks and policy cannot be silently weakened by the implementation.
- [ ] The handoff distinguishes executed, failed, and unexecuted validation.
- [ ] Human review capacity and a recovery path exist.
- [ ] Failed and abandoned agent tasks count in effectiveness/cost metrics.
- [ ] At least one real customer outcome and reliability guardrail are tracked.
- [ ] Shared context has an owner; shared memory/skills are reviewed.
- [ ] Provider/data/retention policies are explicit.
- [ ] Autonomy is scoped by risk and can be revoked.
- [ ] The chosen workflow beats or plausibly improves on the current capable baseline, with uncertainty stated.
- [ ] Added platform/process work has a budget and a stop rule; the entire reference design is not being built by default.
- [ ] Customer value and reusable capacity are distinguished from raw output and hypothetical salary savings.

For customer-facing agents, additionally establish that:

- [ ] Evals include both actions that should happen and actions that must not happen.
- [ ] Final-state outcomes, repeated-run behavior, latency, and cost are measured.
- [ ] Model grading is calibrated against domain-expert judgment.
- [ ] Tool authorization is enforced outside the model.
- [ ] Retries reconcile side effects rather than blindly repeating them.
- [ ] Model, prompt, tool, retrieval, and policy changes are versioned and evaluated.
- [ ] Production failures feed a privacy-aware regression process.

## 20. Final recommendation after the adversarial pass

### 20.1 The conclusion that survives

Build a **small, accountable, customer-connected product team whose engineering system makes useful changes cheap to attempt, credible to verify, and safe to operate**. Use AI aggressively where it expands useful capability or improves total delivery economics. Do not define the team by agent count, generated-code share, seniority mix, or the absence of manual coding.

The evidence supports substantial capability and some productivity gains, but not a universal multiplier, an optimal staffing ratio, inevitable maintainability collapse, or the superiority of a fully autonomous factory. The strongest practical synthesis is **conditional automation with measured outcomes**, not maximal automation or maximal process.

For the conflicting productivity results, compare [S20](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/) [S21](https://arxiv.org/abs/2507.09089) [S22](https://metr.org/blog/2026-02-24-uplift-update/) and [S42](https://arxiv.org/html/2507.08149v2); for heterogeneous agent-adoption effects and mixed maintainability findings, compare [S34](https://arxiv.org/html/2601.13597v2) [S35](https://arxiv.org/html/2507.00788v3); for downstream value limits, see [S36](https://www.nber.org/papers/w35275).

The original recommendation bundled attractive practices from seven successful teams. The revised recommendation is more selective: identify the actual constraint, borrow the smallest relevant mechanism, and retain it only if its protective value or total benefit justifies its cost. Lighthouse systems are design references, not ingredients that become a validated operating model when combined.

### 20.2 Choose the operating system by stage and consequence

The configurations below are recommendations under uncertainty, not empirically established maturity levels. All require appropriate data handling and permissions. A disposable prototype with synthetic data has a different verification burden from an experiment involving real customers or production authority.

Their stage/risk distinction applies the simplicity guidance in [S27](https://www.anthropic.com/research/building-effective-agents), the bounded production workflow in [S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2), and the risk-management principles in [S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) [S43](https://csrc.nist.gov/pubs/sp/800/218/final). Those sources do not validate the exact team configurations.

| Team situation | Human emphasis | Minimum useful AI engineering setup | Defer unless evidence or obligations require it |
|---|---|---|---|
| **Searching for a product, low-consequence prototype** | Product discovery, interaction quality, rapid falsification; technical owner can also be the founder | One approved coding tool; version control; existing build/check path; bounded local or hosted workspace; no ordinary production authority; inspectable demo and explicit uncertainty | Custom session service, agent swarm, full simulator, elaborate scorecard, dedicated platform role |
| **Early product with real users and a small team** | End-to-end engineers plus named system/reliability owner and domain access | Reproducible relevant environment, CI, review appropriate to risk, release/recovery path, a few core user-journey checks, one measured delegation workflow | Full-stack sandbox per trivial task, multi-provider routing, organization-wide orchestration, sophisticated private holdouts for every change |
| **Growing demand with repetitive, separable backlog** | Product delivery plus more dedicated enablement if the load earns it | Isolated unattended runs, bounded retries/spend, evidence handoff, protected checks, selected scenarios, measured review/integration capacity | Arbitrary concurrency, broad tool catalogs, a generic platform without a concrete internal customer |
| **Sensitive data, regulated domain, or high-consequence actions** | Domain and assurance expertise alongside implementation; explicit risk owner | Approved data path; least privilege; independently enforced authorization; auditability; validated domain checks; required approvals; staged exposure and credible recovery | Unrestricted autonomous actions, assuming a vendor's defaults satisfy obligations, relaxing controls because a benchmark score rose |

For products containing AI, add the relevant evaluation, data, tool-authorization, and production-monitoring requirements from section 9. These are product requirements, not prerequisites for every ordinary team using a coding assistant.

### 20.3 A minimum viable operating system for five engineers

**People:** one hands-on decision owner; engineers able to own changes through production; named responsibility for the shared delivery path; access to the product/domain expertise the work demands. Responsibilities overlap. Preserve learning and cross-coverage. Add a dedicated platform or specialist role when actual demand, risk, or recurring load establishes the need.

**Tools:** one approved capable coding environment, the existing repository and CI, repeatable relevant setup/check commands, bounded credentials, and a release mechanism with recovery. Add browser access, background sandboxes, or an external scenario runner when the selected workflow needs them. Keep optional instruction files minimal and evaluated rather than auto-generating elaborate repository guidance.

**Work:** a real customer problem, accountable owner, small coherent change, explicit acceptance and risk, recorded validation, proportionate review, and post-release observation. Do not demand a lengthy task contract for a typo or pretend a vague specification is sufficient for a money-moving workflow.

**Measurement:** choose one useful outcome measure and a few guardrails: total human effort, lead time, meaningful defects/rework, and total cost. A lightweight record of failed and successful attempts can be enough initially. Do not build an analytics platform to avoid looking at the work.

**Learning:** periodically inspect a few outcomes and recurring failures. Fix the specific missing capability, simplify a redundant control, or stop a bad workflow. Documentation and shared skills should encode durable facts, not preserve every prompt workaround forever.

The operating-system synthesis draws on human learning evidence [S26](https://www.anthropic.com/research/AI-assistance-coding-skills), the context-file ablation [S33](https://arxiv.org/html/2602.11988v3), supervision costs [S39](https://arxiv.org/html/2605.29442v2), delivery-system research [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) [S24](https://research.google/pubs/dora-ai-capabilities-model/) [S25](https://dora.dev/ai/roi/report/), and the concrete engineering examples in sections 1 and 5. The recommended team allocation remains a design judgment.

### 20.4 Falsifiable adoption hypotheses and stop rules

These are example decision rules, not published industry thresholds. Choose stricter quality and permission requirements where consequences justify them. For a small team, an operational decision can be sensible without a statistically decisive causal estimate, provided uncertainty and reversibility are explicit.

| Hypothesis to test | Evidence needed | Stop, narrow, or redirect when |
|---|---|---|
| A bounded bug class is cheaper with an agent than with the current workflow | Comparable tasks; active engineering plus review/repair time; accepted outcomes; a defined post-release observation window | Gains disappear after supervision, rework, recurring system cost, or downstream repair |
| Extra repository instructions reduce repeated failures | Minimal-versus-proposed context comparison with unchanged mandatory controls; relevant behavior, task success, cost | Instructions add exploration/cost without improving the intended outcome; remove the optional addition |
| Background execution returns useful attention | Intervention counts, uninterrupted time, elapsed delivery, and evidence of what reclaimed capacity enables | Monitoring and task switching fragment the day or create a review queue |
| More parallel agents improve delivery | Comparable task classes, clear integration owner, quality-adjusted cycle time and total resource use | Review/integration wait grows, cost breaches the cap, or independently passing pieces fail together |
| Reduced review is justified for one low-risk class | Strong acceptance checks, bounded impact, recovery, audit sample, and named policy owner | Audit failures or meaningful escaped defects appear; restore review for that class |
| A custom platform has positive marginal value | A documented gap in approved tools, full build/operation estimate, internal users, and opportunity-cost comparison | The platform's setup and maintenance exceed realized benefits or the supposed gap disappears |

For a practical first pilot, set a **two-to-four-week learning allowance** and a specific recurring budget before starting. This is a management timebox, not a statistical guarantee. At the end, choose expand, narrow, extend for a stated unresolved question, or stop. Do not repeatedly extend solely because a new model might rescue the economics.

An illustrative scale criterion is **at least 15% lower total active human effort for the eligible task class**, no unacceptable quality/reliability deterioration, and positive economics after recurring overhead. The 15% is an example of a precommitted business threshold, not an expected effect from the literature. Use a threshold appropriate to measurement noise, risk, and alternative investments; do not claim significance from a handful of tickets.

Immediately suspend the relevant autonomy if the worker exposes restricted data, acts outside its approved authority, or bypasses a required check. If a productivity trial is inconclusive rather than unsafe, keep useful low-cost assistance available while narrowing the experiment. "Do not scale this configuration" is different from "ban AI."

### 20.5 What could still make this synthesis wrong?

**Underestimating the frontier:** rapidly improving agents might make some review and orchestration assumptions obsolete. Watch for independently validated end-to-end outcomes, not only demos. If a simpler autonomous system beats the local guarded workflow on quality, cost, and learning, remove obsolete scaffolding rather than defending it.

**Underestimating delayed harm:** short trials can miss security exposure, architectural drift, or lost operating knowledge. Follow accepted work through later modification and incidents; retain high-consequence safeguards even when the initial ROI looks excellent.

**Measuring the wrong outcome:** fixed-ticket efficiency can miss valuable new capabilities, while release counts can miss actual customer benefit. Allocate some bounded exploratory capacity to work that was previously impractical, but judge it by useful learning or adoption rather than artifacts generated.

**Becoming too process-heavy:** the report itself could become a bureaucratic checklist. If a team spends more time producing contracts, evaluation dashboards, and agent infrastructure than resolving its real customer uncertainty, simplify the operating system. Preserve essential authority and data protections; cut ceremony and unsupported fixed costs.

<keyidea>The durable advantage is not the percentage of code written by AI. It is the ability to turn customer evidence into useful, reliable changes at sustainable total cost, recognize when the evidence is wrong, and adapt both the product and its engineering system.</keyidea>

## 21. Connection to this knowledge base

The [Concepts glossary](../20260913%20Concepts/readme.md) provides several useful lenses:

- **Skills as Operational Units:** reviewed procedures become reusable engineering capabilities rather than private prompting habits.
- **Continuous AI:** background checks and diagnosis can shorten feedback loops, provided actions remain bounded and observable.
- **Capability Aggregator:** a common tool layer can reduce duplicated integrations, but every added capability needs authorization and ownership.
- **Product Overhang:** better environments and verification can unlock capability already present in models before another model upgrade is necessary.

These are conceptual connections, not independent evidence for the recommendations.

## 22. Annotated source register

All sources below were consulted or retrieved on **November 6, 2026**. Dates refer to publication when established; otherwise the source is labeled live/undated rather than assigned a guessed date. Company metrics are company-reported unless stated otherwise. The register includes source-quality and access caveats so later readers can reassess the evidence.

### Lighthouse engineering systems

**[S01](https://openai.com/index/harness-engineering/) OpenAI, Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," February 11, 2026.** [Original](https://openai.com/index/harness-engineering/) · [Markdown reproduction consulted](https://raw.githubusercontent.com/celesteanders/harness/main/docs/research/260211_openai_harness_engineering_codex.md). Primary account by authorship, but direct original retrieval was blocked by HTTP 403. The third-party reproduction supplied the detailed text. Supports the small-team experiment, environment design, architecture enforcement, repository knowledge, cleanup, and reported counts. No independent audit or controlled speed comparison.

**[S02](https://www.engineering.fyi/article/harness-engineering-leveraging-codex-in-an-agent-first-world) Engineering.fyi, "Harness engineering: leveraging Codex in an agent-first world."** [Summary](https://www.engineering.fyi/article/harness-engineering-leveraging-codex-in-an-agent-first-world). Secondary source used to compare the reproduced OpenAI account. Not independent validation of its results.

**[S03](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code) Anthropic, "How Anthropic teams use Claude Code."** [Article](https://claude.com/resources/articles/how-anthropic-teams-use-claude-code). Live company account; the older Anthropic URL redirects here. Supports qualitative internal use cases and cross-functional workflows. Anecdotal time savings are not generalized in this report.

**[S04](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/) Sergio De Simone / InfoQ, "Inside the Development Workflow of Claude Code's Creator," January 2026.** [Report and links to original posts](https://www.infoq.com/news/2026/01/claude-code-creator-workflow/). Secondary practitioner reporting of Boris Cherny's workflow. Supports isolated sessions, shared learnings, planning, verification, and abandonment. Historical model/session preferences are not current universal prescriptions.

**[S05](https://code.claude.com/docs/en/best-practices) Anthropic, "Best practices for Claude Code."** [Live documentation](https://code.claude.com/docs/en/best-practices). Supports concise context, executable checks, and the distinction between model-followed instructions and harness-enforced controls. Product-specific defaults and syntax change; this report does not freeze them as an implementation contract.

**[S06](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) Anthropic, "Effective harnesses for long-running agents."** [Engineering article](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents). Supports initialization, incremental progress, explicit feature state, handoffs, and end-to-end checks. A particular experimental harness, not a universal architecture.

**[S07](https://www.anthropic.com/research/managed-agents) Anthropic, "How we built Claude Managed Agents."** [Engineering article](https://www.anthropic.com/research/managed-agents). Supports separation of durable session, replaceable harness, execution sandbox, and credential brokerage; also documents obsolete harness assumptions. Company architecture experience, not a claim that every small team needs this platform.

**[S08](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents) Alistair Gray / Stripe, "Minions: Stripe's one-shot, end-to-end coding agents," February 9, 2026.** [Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents). Primary implementation/use account. Reports over 1,000 merged minion-produced PRs weekly with human review.

**[S09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) Alistair Gray / Stripe, "Minions: Stripe's one-shot, end-to-end coding agents - Part 2," February 19, 2026.** [Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2). Detailed primary source for blueprints, devboxes, scoped context/tools, security boundaries, and bounded CI iteration; reports over 1,300 PRs weekly.

**[S10](https://builders.ramp.com/post/why-we-built-our-background-agent) Ramp Builders, "Why we built our background agent."** [Technical account](https://builders.ramp.com/post/why-we-built-our-background-agent). Live/updated primary account, retaining the original approximately 30% adoption figure. Supports environment snapshots, full-stack verification, clients, shared sessions, and implementation details. Some recommendations, such as trusting agents to self-limit spawning, are not adopted here.

**[S11](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal) Modal, "How Ramp built a full-context background coding agent on Modal."** [Infrastructure case study](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal). Supplier-authored case study with named Ramp quotations and technical details; reports roughly half of merged PRs. Commercial incentive and differing observation window apply.

**[S12](https://ramp.com/blog/introducing-inspect) Karim / Ramp, "Introducing Inspect."** [Launch account](https://ramp.com/blog/introducing-inspect). Live company launch page. Reports 74% of merged PRs, 99% recent engineering/design/product adoption, and sixfold code volume per person. Publication date was not established from the retrieved text; these are page claims, not independently measured causal results.

**[S13](https://shopify.engineering/under-the-river) Shopify Engineering, "Under the River."** [Architecture and operating account](https://shopify.engineering/under-the-river). 2026 account; exact publication date not established from retrieved text. Supports World/Nix, shared River sessions, Aquifer, session/harness/sandbox separation, and quoted operational counts.

**[S14](https://shopify.engineering/reflex) Shopify Engineering, "Reflex: an architecture for building mobile apps with agents."** [Architecture account](https://shopify.engineering/reflex). Live 2026 account; exact publication date not established from retrieved text. Supports headless Core, ViewModel state/action contracts, cross-platform behavior tests, and the reported 1,700-plus tests in about four minutes. Does not establish visual/device correctness.

**[S15](https://shopify.engineering/building-production-ready-agentic-systems) Andrew McNamara / Shopify Engineering, "Building production-ready agentic systems: Lessons from Shopify Sidekick."** [Technical account](https://shopify.engineering/building-production-ready-agentic-systems). Based on an ICML 2025 talk. Supports just-in-time instructions, production-derived eval sets, human-calibrated judges, simulation, and observed reward hacking.

**[S16](https://factory.strongdm.ai/) Justin McCarthy / StrongDM, "Software Factories and the Agentic Moment."** [First-party account](https://factory.strongdm.ai/). Live factory site. Supports the three-person team, no-human-code/review experiment, scenarios, satisfaction, and Digital Twin Universe. Provocative spend guidance is a claim by the author, not this report's recommendation.

**[S17](https://simonwillison.net/2026/Feb/7/software-factory/) Simon Willison, "How StrongDM's AI team build serious software without even looking at the code," February 7, 2026.** [Outside observer account](https://simonwillison.net/2026/Feb/7/software-factory/). Describes a demonstration he attended, public artifacts, and economic reservations. More informative than a simple repost, but not a production security audit.

**[S18](https://github.com/strongdm/attractor) StrongDM, Attractor repository.** [Specification artifact](https://github.com/strongdm/attractor), linked and described in [S17](https://simonwillison.net/2026/Feb/7/software-factory/). A public design/specification reference. The repository was not independently executed or validated during this research.

**[S19](https://cursor.com/blog/scaling-agents) Cursor, "Scaling long-running autonomous coding," January 2026.** [Experimental engineering account](https://cursor.com/blog/scaling-agents). Primary source for coordination failures, planner/worker roles, model-role differences, browser experiment, migration caveats, and workload-specific optimization. Research experiments must not be presented as equivalent production deployments.

### Empirical research and delivery evidence

**[S20](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/) Cui, Demirer, Jaffe, Musolff, Peng, and Salz, "The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers," June 2025.** [Microsoft Research publication and abstract](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/). Original study summary consulted. Reports the pooled 4,867-developer result and standard error. Intervention concerned coding assistance, not today's complete autonomous-engineering system.

**[S21](https://arxiv.org/abs/2507.09089) METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," July 2025.** [Paper abstract and version history](https://arxiv.org/abs/2507.09089). Original randomized study, 16 developers and 246 tasks; reports 19% longer completion time. Narrow population/tool-period limits are essential.

**[S22](https://metr.org/blog/2026-02-24-uplift-update/) METR, "We are Changing our Developer Productivity Experiment Design," February 24, 2026.** [Methodological update](https://metr.org/blog/2026-02-24-uplift-update/). Original follow-up account. Explicitly warns about recruitment, task selection, changed compensation, and concurrent-agent time-measurement problems.

**[S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) Google Cloud / DORA, "Announcing the 2025 DORA Report."** [Research summary](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report). Primary summary of the 2025 survey/qualitative research. Supports the amplifier framing and throughput/stability associations; not causal RCT evidence.

**[S24](https://research.google/pubs/dora-ai-capabilities-model/) DeBellis et al. / DORA, "DORA AI Capabilities Model," 2025.** [Publication record](https://research.google/pubs/dora-ai-capabilities-model/) · [Report PDF](https://services.google.com/fh/files/misc/2025_dora_ai_capabilities_model.pdf). Publication record and the primary research summary in [S23](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) were consulted; the capability list was also cross-checked through report discovery. Do not interpret the model as proving an exact staffing design.

**[S25](https://dora.dev/ai/roi/report/) DORA, "ROI of AI-assisted Software Development," 2026.** [Report landing page, updated April 22, 2026](https://dora.dev/ai/roi/report/) · [Google Cloud overview](https://cloud.google.com/resources/content/dora-roi-of-ai-assisted-software-development) · [InfoQ review](https://www.infoq.com/news/2026/05/dora-roi-ai-assisted-dev-report/). Primary overview and secondary review consulted. Supports the J-curve, capacity reinvestment, and explicit financial modeling. Illustrative ROI/payback scenarios are not promised outcomes.

**[S26](https://www.anthropic.com/research/AI-assistance-coding-skills) Anthropic, "How AI assistance impacts the formation of coding skills," 2026.** [Original research account](https://www.anthropic.com/research/AI-assistance-coding-skills). Reports the 52-participant Trio study, 50% versus 67% quiz scores, nonsignificant time difference, and limits of immediate assessment. Qualitative interaction-mode associations are not causal estimates.

### Agent engineering and risk guidance

**[S27](https://www.anthropic.com/research/building-effective-agents) Anthropic, "Building effective agents," originally December 2024, subsequently updated.** [Article](https://www.anthropic.com/research/building-effective-agents). Supports the workflow/agent distinction and simple composable patterns. The live article itself warns that tooling has changed.

**[S28](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) Anthropic, "Demystifying evals for AI agents."** [Evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents). Supports outcome versus transcript, deterministic/model/human graders, repeated trials, capability versus regression evals, initial small task sets, and grader validation. Product/vendor guidance rather than a causal productivity study.

**[S29](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) Simon Willison, "The lethal trifecta for AI agents: private data, untrusted content, and external communication," June 16, 2025.** [Threat-model analysis](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). Practitioner security analysis with links to concrete incidents. Used for architectural risk framing, not as a claim about a newly audited vulnerability.

**[S30](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) OWASP GenAI Security Project, "OWASP Top 10 for Agentic Applications for 2026."** [Framework overview](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/). Overview consulted as a broader risk reference; the report's detailed control table is an engineering synthesis, not a verbatim mapping of all OWASP categories.

**[S31](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) NIST, "AI RMF Playbook."** [Official guidance](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook). Based on AI RMF 1.0; page updated June 10, 2026. Supports a Govern/Map/Measure/Manage approach. Voluntary guidance, not legal certification.

**[S32](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) Anthropic, "Effective context engineering for AI agents."** [Engineering guidance](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents). Supports focused high-signal context, just-in-time retrieval, clear tool boundaries, and progressive disclosure. These principles inform the context recommendations in sections 5, 9, and 12; model-specific limits should be reevaluated over time.

### Additional evidence from the adversarial pass

**[S33](https://arxiv.org/html/2602.11988v3) Gloaguen, Mündler-Sasahara, Raychev, and Vechev, "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" v3, September 29, 2026.** [Abstract and version history](https://arxiv.org/abs/2602.11988) · [Version consulted](https://arxiv.org/html/2602.11988v3). Original methods, results, and limitations consulted. Four model/agent settings; SWE-bench Lite and the 138-instance Python CTXbench. No significant overall improvement over no context; generated files increase inference costs about 20-23%. Developer files outperform generated files, not significantly the no-file baseline. Generated tasks/tests, language restriction, particular models, and task-resolution measurement constrain transfer. ETH/LogicStar affiliations are disclosed in the paper. Do not substitute early-version summaries for the current result.

**[S34](https://arxiv.org/html/2601.13597v2) Agarwal, He, and Vasilescu, "AI IDEs or Autonomous Agents? Measuring the Impact of Coding Agents on Software Development," v2, January 27, 2026.** [Record](https://arxiv.org/abs/2601.13597) · [Methods/results consulted](https://arxiv.org/html/2601.13597v2). Matched staggered difference-in-differences using observable repository adoption. Supports heterogeneous incremental activity gains and increased static-analysis/complexity signals. Prior-use detection and agent attribution are imperfect; some quality outcomes have concerning pre-treatment coefficients. Neither randomized productivity evidence nor a measurement of production bugs or lifetime maintenance cost.

**[S35](https://arxiv.org/html/2507.00788v3) Borg et al., "Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability," v3, February 26, 2026.** [Record](https://arxiv.org/abs/2507.00788) · [Original paper consulted](https://arxiv.org/html/2507.00788v3). Preregistered two-phase study, 151 participants, approximately 95% professionals. Randomized downstream evolution phase finds no systematic maintainability advantage/disadvantage; first-phase productivity findings are observational. Task scope, volunteer participation/attrition, short evolution horizon, and late-2024 tool generation limit inference. Author affiliations include CodeScene and Equal Experts; the study uses CodeScene metrics as well as an actual downstream modification task.

**[S36](https://www.nber.org/papers/w35275) Mert Demirer, Leon Musolff, and Liyuan Yang, "Writing Code vs. Shipping Code: Productivity Effects Across Generations of AI Coding Tools," NBER Working Paper 35275, June 2026.** [Original abstract and bibliographic metadata consulted](https://www.nber.org/papers/w35275). More than 500,000 GitHub developers with usage telemetry; matched event-study design. Reports cumulative activity gains attenuating toward releases, and increased app supply without increased aggregate usage across four marketplaces. This research consulted the abstract, not the full methods/robustness analysis. Working-paper status and observational identification matter. Not proof of no private business value or an incremental 240% gain from upgrading an existing copilot.

**[S37](https://arxiv.org/html/2512.08296v3) Kim et al., "Towards a Science of Scaling Agent Systems," v3, April 8, 2026.** [Record/version history](https://arxiv.org/abs/2512.08296) · [Abstract and introduction consulted](https://arxiv.org/html/2512.08296v3). Latest consulted revision has 260 configurations across six benchmarks, not the smaller counts repeated in early summaries. Standardized architecture comparisons show task-dependent benefits and severe regressions. Reported relative benchmark extremes are not engineering-team speedups or universal scaling laws. Authors include Google Research/DeepMind and MIT researchers.

**[S38](https://doi.org/10.4230/LIPIcs.ESEM.2026.89) Gullstrand Heander et al., "Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes," ESEM 2026.** [Original publication record and abstract](https://doi.org/10.4230/LIPIcs.ESEM.2026.89) · [JetBrains research explanation, October 2026](https://blog.jetbrains.com/research/2026/10/review-ai-generated/). Both consulted. Participatory design with 17 practitioners and a 43-person follow-up survey; supports a proposed multilevel risk-weighted review design and perceived usefulness, not observed defect reductions or productivity gains. University/vendor collaboration, not independent validation of a shipping product.

**[S39](https://arxiv.org/html/2605.29442v2) Chen et al., "How Coding Agents Fail Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in 20,574 Real-World Sessions," v2, August 31, 2026.** [Record](https://arxiv.org/abs/2605.29442) · [Abstract and methods consulted](https://arxiv.org/html/2605.29442v2). Observational public-log study using pushback-grounded episodes and LLM-assisted annotation with human validation. Supports the importance of effort/trust costs and explicit correction. Percentages describe extracted episodes and visible resolutions, not overall agent failure rates. Public opt-in traces, detection choices, annotation errors, and missing off-log outcomes limit representativeness.

**[S40](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) OpenAI, "Why we no longer evaluate SWE-bench Verified."** [Original analysis consulted](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/). Publication date not established from the retrieved text. Audits 138 deliberately difficult tasks out of 500, with reported material issues in 59.4% of that subset; also presents contamination evidence. Supports evaluator/specification validity concerns, not a representative defect estimate for all benchmark tasks. Vendor analysis by a benchmark co-creator, not an independent audit of every provider's training process.

**[S41](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/) Daniel Stenberg, "The end of the curl bug-bounty," January 26, 2026.** [Primary operating account consulted](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/). Reports termination effective January 31, a 2025 confirmation rate below 5%, and substantial triage burden. Attributes the problem to multiple factors and explicitly contrasts curl with less-affected peers and its own better-filtered PR workflow. Negative case and incentive warning, not a controlled estimate that AI caused all false reports or that all open source is similarly affected.

**[S42](https://arxiv.org/html/2507.08149v2) Chen et al., "Code with Me or for Me? How Increasing AI Automation Transforms Developer Workflows," v2, September 13, 2025.** [Record](https://arxiv.org/abs/2507.08149) · [Original study design consulted](https://arxiv.org/html/2507.08149v2). Twenty university-recruited regular Copilot users, many with professional experience; randomized tool order within participants, paired task types, short April-May 2025 sessions comparing Copilot and OpenHands. Reports better correctness and lower active user effort with the agent; comprehension/experience challenges remain. Small selected sample, short horizon, different tool/model bundles, and All Hands AI author affiliations matter. Useful counterevidence to a blanket claim that agents cannot improve on copilot workflows.

### Foundational secure-development and operations references

**[S43](https://csrc.nist.gov/pubs/sp/800/218/final) Souppaya, Scarfone, and Dodson / NIST, "Secure Software Development Framework (SSDF) Version 1.1: Recommendations for Mitigating the Risk of Software Vulnerabilities," SP 800-218, February 2022.** [Official publication and abstract consulted](https://csrc.nist.gov/pubs/sp/800/218/final) · [Full framework for further reading](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf). Provides a high-level secure-SDLC and software-supplier vocabulary for sections 8, 10, and 19. The official abstract/record was consulted; the PDF was not text-reviewed for clause-by-clause mapping. This is foundational guidance, not evidence of an AI productivity effect or certification that the proposed controls satisfy a particular obligation.

**[S44](https://sre.google/sre-book/table-of-contents/) Google, "Site Reliability Engineering," online book.** [Book and contents](https://sre.google/sre-book/table-of-contents/) · [Release engineering](https://sre.google/sre-book/release-engineering/) · [Monitoring distributed systems](https://sre.google/sre-book/monitoring-distributed-systems/) · [Managing incidents](https://sre.google/sre-book/managing-incidents/) · [Postmortem culture](https://sre.google/sre-book/postmortem-culture/). The linked chapter text was consulted for reproducible and access-controlled releases, canary/rollback practices, service monitoring, incident roles, and system-oriented learning. Foundational operational experience at Google, not a staffing prescription for a five-person team or an experimental evaluation of AI-specific controls.

### What would strengthen or change these conclusions?

Independent replications of factory-style development; longer-term maintenance and incident data; controlled comparisons of agent-assisted versus conventional review; cost-per-accepted-outcome figures including failed attempts; evidence from small non-vendor teams, including unsuccessful deployments; and rigorous longitudinal work on engineer skill development. Also needed: comparative staffing studies, audited evaluator validity, a clearer account of capacity-to-customer-value conversion, and cost-adjusted tests of which controls can safely replace rather than accumulate on top of existing process.

Until that evidence is stronger, the appropriate stance is **rapid, bounded experimentation; explicit human accountability; proportionate authority controls; and conditional investment based on total outcomes**. Uncertainty justifies measurement and reversible decisions, not either an autonomous-factory mandate or a blanket refusal to use AI.
