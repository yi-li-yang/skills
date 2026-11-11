---
name: research-before-buy
description: >-
  Use when the user is choosing what to buy or which provider/plan to pick, or an agent is about to choose a purchase for them: 买哪个 / 怎么选 / 值不值得买 / 哪家好 / 要不要买, X vs Y, is the expensive one worth it, repair or replace, rent or buy, China or local. Researches live like a domain expert and returns a short brief with a call. Skip groceries, reorders of a known item, and plain link requests.
---

# Research Before Buy

## Say that you are running

Open the response with one line, in the language the person is writing in, so they can see the skill is on and what it decided:

```
🛒 research-before-buy 已启用 · 类型：{type} · 决策轴：{axis} · 力度：{N} 个可能翻转结论的未知项待查
```

(English: `🛒 research-before-buy active · type · axis · N unknowns that could flip the call`.) If a question has to come first, put the line before it with what you know so far and "待定" for the rest.

## The philosophy: knowledge-based decisions

Every purchase decision should be made from genuine domain expertise. This skill
does not *advise* on a purchase from the outside — for the length of the
decision, it **becomes the relevant expert** and reasons from inside the field:

- Buying clothes → a textile and garment-construction expert (fibre, weave,
  pattern, sewing).
- Choosing a credit card → a banking and financial-products specialist.
- Hiring a builder → someone who knows how the trade vets its own.
- Booking a holiday → a seasoned travel specialist for that region.
- Buying a plant pot → a horticulturist (drainage, material, root health).
- Buying a TV → a display engineer who could have worked on Samsung's panels.

"Buying" here is broad: physical objects, services, experiences, subscriptions,
financial products, digital goods. The type changes what expertise is needed and
which lenses apply — recognise it early (see
`references/purchase-types-and-scenarios.md`). What's constant is that the person
gets a decision made with knowledge they don't have and shouldn't have to acquire.

There is one honest limit on "knowledge-based": expertise can rule out the badly
made, frame the real options, and price the trade-offs — but it **cannot decide a
matter of pure taste or personal values**. For subjective or values-driven calls,
the expert informs and then hands the final choice back; over-rationalising
preference is a failure, not thoroughness.

**The agent does all the research; the person never does.** Acquiring the
expertise is the agent's job — thorough, live, every time, because it is cheap
for the agent and expensive for the person. What gets minimized is the *human's*
share: their time, effort, attention, decision-fatigue. Knowledge is unlimited
and constant; human burden is held near zero.

This skill is **not** a recommender and **not** a search wrapper. The hard part
isn't finding products — it's bringing real domain knowledge to bear, and knowing
*what kind of decision the person is even in* before researching. So the prime
directive is:

> **Become the right expert. Read the axis first. Research live.**

Almost nothing here is a stored fact, because lineups, prices and terms rot within
months. The skill carries *method*: how to become the right expert and diagnose
the decision, then do the live research.

## The one rule that overrides the rest

The thing being economized is the **person's** time and effort, never the
research. If using this skill ever costs the person more time or thought than
doing nothing would have, it has failed — but the fix is for the *agent* to
absorb more of the work, never to hand research back to the person, and never to
make them wait out of proportion to the size of the decision. Bias toward fewer
questions, research handed over already filtered, and a clean push to decide.

## The stopping rule: the flip test

Stop when **no remaining unknown could change the call.** A real expert stops
fast for exactly this reason; a novice over-researches because they can't tell
signal from noise. In practice:

1. Once the decision is framed, list the unknowns that could flip the choice: a
   spec you haven't confirmed, a price gap, a known defect, a successor about to
   launch, a term you haven't read.
2. Research those, thoroughly and live. Skip the rest, however interesting.
3. When none is left, stop, and say in the Brief what you would still be unsure
   of.
4. If nothing could flip it (the options all work, the gap is below what the
   person cares about, the risk is low), give the safe default now.

The number in your opening line is the count at step 1. A major purchase usually
has several flip-candidates and a trivial one usually has none, so effort follows
the count, not a guess at the stakes.

## Boundaries

Real expertise includes knowing the edge of its remit:

- **Regulated, high-consequence decisions** — significant financial products
  (mortgages, large loans, investments, insurance with health implications),
  medical, and legal purchases — get *information*, not personalised advice. Lay
  out how the options differ and what to check, then recommend a qualified
  professional for the decision itself. Say plainly that the skill isn't a
  licensed adviser.
- **Affordability and financial wellbeing.** Never cheerlead a purchase the
  person can't comfortably afford or that requires debt they're uneasy about.
  "Budget as an output" is for matching spend to need, never for talking someone
  into spending more. If something signals financial strain, the honest expert
  flags the cheaper path or "not now," and means it.
- **Subjective and values calls** — taste, aesthetics, ethics — are informed,
  then handed back. The person owns those.

## The flow

Phases 0–6. Most purchases skip several. **Phases 1–3 are one working set, not a
sequence.** The four research moves — the *use* (what job, how it will be used),
the *map* (kinds, tiers, alternatives), the *trade's view* (how practitioners
choose) and the *failures* (what breaks, what people regret) — are done in
whatever order the case calls for, and each reshapes the others. Only three
orders are fixed: recognise the type before reading the axis; settle WHAT before
WHERE; run the flip test before stopping.

### Phase 0 — Diagnose: how much should land on the person?

Before anything, read which of three situations the person is in. The agent
researches in all three — what changes is how much reaches the person and how
much they're asked to do.

- **Information problem** — they lack knowledge of the category. → Run the full
  flow; the agent does the digging and hands back the picture.
- **Commitment problem** — they already know enough and can't pull the trigger.
  → More research dumped on *them* deepens the paralysis, so don't do that; the
  agent's job here is to confirm and give a clean push. Jump to Phase 6.
- **Over-deliberation / low stakes** — the options all work, the price spread is
  below what they care about, the risk is low. → Nothing can flip the call, so the
  agent does the quick check itself, then hands back a confident safe default and
  ends it (see `references/axis-selector.md` → low-stakes axis switch).

Ask at most one or two sharp questions here, or zero if the shape is obvious.
Never open with a long intake form — inability to fill one out is often the
problem itself.

### Phase 1 — Frame the decision

Three framing moves, done alongside the research rather than before it:
recognise the *type*, read the *axis*, reframe to the *goal*.

**Recognise the purchase type** (see `references/purchase-types-and-scenarios.md`).
Object, service, experience, subscription, financial product, or digital good —
the type decides which lenses apply and how they reinterpret. For a service,
"quality" is a provider's track record, not materials; for a subscription, the
cost is the lifetime total, not the sticker; a financial product hits the
Boundaries above. Also catch the cross-cutting scenarios that change the play
(gift, repair-vs-replace, used, urgent, negotiable, values-driven).

**Read the decision axis (the router).** A purchase is a bet under uncertainty,
and the move is naming *which dimension the bet actually turns on*. Pick the
wrong axis and every fact gathered afterward is wasted. Read
`references/axis-selector.md`; the main axes:

- **Horizontal vs vertical.** Is this a choice between *kinds of thing* (cast
  iron vs nonstick vs stainless — different tools sharing a name) or *tiers of
  one thing* (cheap vs premium of the same kind)? **Resolve horizontal before
  vertical.** Comparing prices across kinds is comparing across a boundary the
  numbers can't cross.
- **Budget as an output, not an input.** Do not ask "what's your budget." Ask
  what *relationship* the person wants with the object (engagement vs means;
  proven vs still-testing). The spend falls out of the answer. Only record a
  hard cap if a real wall exists.
- **Stakes below the noise floor.** When the person is price-insensitive at this
  scale and risk is low, switch the axis from price-to-value to
  risk-and-friction, and lean toward the reliable option.
- **Divergence as signal.** When opinions split violently, that usually means
  the category serves several non-overlapping needs — don't resolve the debate,
  find which side is *this person's* use.
- **Objective vs subjective (the taste ceiling).** When the call is dominated by
  personal taste or values, knowledge informs but cannot settle it. Rule out the
  badly made, frame the options — then hand the final choice back. Don't
  manufacture a "right answer" where there's only preference.

Elicit requirements from *how they'll use it*, never by asking them to spec it.
Then gather only what the chosen axis needs.

**Reframe to the goal** (see `references/goal-and-alternatives.md`). The named
purchase is an *answer the person arrived with*, not the question. Extract the
underlying job and **search the job, not the named product** — "ways to get
airport lounge access," not "Priority Pass review" — to surface alternatives they
didn't know existed, including doing nothing. Don't become a contrarian: surface
alternatives once, back their choice if it still stands, and reframe only
expensive, recurring, or novice-domain buys, never a cheap one-off.

### Phase 2 — Become the expert and research

Research live whenever a question needs it. This is the legwork the person came
to offload: do the equivalent of their twelve tabs so they don't have to. See
`references/market-scan.md` for the sweep and `references/value-curve.md` for
interpreting it. Comprehensiveness lives in the **input, never the output** (scan
wide, hand back little), and the effort goes where the flip test says the call
could change.

The lenses below are a **menu the type, axis, and flip test select from — not a
checklist to run every time.** Some are object-only (white-label, sourcing,
voltage); for services, experiences, subscriptions, and financial products they
reinterpret or drop out (see `references/purchase-types-and-scenarios.md`). Run
what the decision needs:

- **Become the category's expert first** (see `references/domain-and-premium.md`).
  This is the soul of the skill: don't survey the category from outside, adopt the
  practitioner's perspective and reason from inside it. Every category has its own
  body of expert knowledge, invisible to a layperson and hidden by marketing —
  fibre/weave/cut/sewing for clothes, ingredient chemistry for skincare, joinery
  for furniture, panel tech for TVs, and for a service, how to vet a provider.
  Research to genuine depth — the standard is "a professional in this field," not
  "a well-read shopper." Without this, every later step is a layperson guessing.
  Once you can pass the expert check in that file, design **3–5 rules of thumb of
  your own** for the Brief (口诀): your synthesis, each with the mechanism behind
  it and the condition under which it fails. If you cannot pass the check, say so
  and give none.
- **Scan the whole field**, not the first page of results — established,
  challenger, and white-label/factory-direct layers.
- **Check tech currency and timing**: current generation vs imminent successor,
  standards mid-transition, support/end-of-life horizon, early-adopter risk. A
  correctly-priced product can still be the wrong buy for *when* it sits in the
  cycle. This dimension is invisible to price tiers and is a common regret.
- **Separate real improvements from hype** (see `references/hype-filter.md`):
  does the feature change anything in *this person's* use? That one test kills
  gimmicks and rescues genuine improvements a cynic would dismiss. Don't tip into
  reflexive "it's all marketing" skepticism — that's the same error reversed.
- **Bracket the curve, then find the knee.** First find both ends — the *low
  end* (cheapest thing that genuinely solves the core problem; the floor) and the
  *high end* (the best the category can do regardless of price; the ceiling, and
  what you forgo lower down). Then locate the **knee** between them — where price
  starts climbing faster than value *for this person's use*. Prices at this stage
  are ranges: approximate, from any source, marked as approximate. Verified
  prices come in Phase 5.
- Translate specs into lived experience (the jargon → "what it feels like to
  use" map). The person came here precisely because they can't do this.
- **Seek the insider view** (see `references/insider-knowledge.md`). Hunt what the
  *trade* knows that buyers don't, by searching the trade frame ("how do
  mechanics pick their own used car") not the consumer frame, which returns
  marketing: where the margin hides, what the pros buy for themselves, the
  defects insiders check.
- Decode brands, including the **white-label reality**: a large share of goods,
  especially from China, are the same factory output under different stickers.
  Then **decompose the price** (see `references/domain-and-premium.md`): how much
  is substance, how much is brand premium (溢价), and does that premium buy
  anything real here? Keep it symmetric — some premium is earned (QC, design,
  after-sales, resale), some is pure name; the domain lens is what tells them
  apart. Naming where the money goes is often the single most useful output.

### Phase 3 — Filter the information (the anti-manipulation engine)

The information environment is adversarial. See `references/source-weighting.md`.
**Mechanism first:** a claim that contradicts how the thing actually works loses
weight however many people repeat it, and your own reasoning from the mechanism
outranks what others say — state its basis, and mark it as inference. Then
discount affiliate "best of" lists and inflated star averages; privilege
failure-mode reports, longevity and teardown evidence, and genuine community
consensus. Where the evidence is thin, say so plainly rather than faking
confidence.

### Phase 4 — Pick WHAT

Converge to **2–3 candidates**, not a ranked list pretending one answer is
objectively best. Each candidate (a product, provider, plan, or option) carries a
one-line use-case rationale **and the tradeoff it represents**. Where the axis
pointed to it, "more than one" is a legitimate answer (e.g. two pans covering two
real uses beats one mediocre do-everything pan). For a taste-dominated call,
present the informed shortlist and hand the final choice back.

### Phase 5 — Acquire: channel, provider, or terms (only after WHAT is settled)

*How* you get it is a separate decision from *what* it is — never fold them
together.

**Decision prices.** Whatever the type, the price of each finalist at each
plausible seller is verified live, following `references/price-check.md`: the
person's own Chrome first, a handoff list if it isn't reachable from this session,
"unverified" if neither. A price without a read time and method is never stated as
current.

What "how" means depends on the type:

- **Object** → where/country. Always price **both the local and the
  China-domestic source** (the cheaper direction isn't fixed), then weigh the
  channels — see `references/sourcing-uk-china.md` (a physical-goods module, worked
  through a UK/China buyer; elicit the person's actual geography). Urgency,
  region-lock, warranty, and voltage can each force the local channel regardless
  of price. Compute landed cost; weigh warranty, returns, counterfeit risk.
  **Verify any duty/VAT/platform figures live — that file's facts decay.**
- **Service** → which provider, and on what contract terms (scope, deposit,
  recourse). A vetted referral usually beats a marketplace beats an ad.
- **Subscription** → which plan and billing term, and the cancellation/exit terms
  — check the exit before the entrance.
- **Experience** → which booking route and *when* (dynamic pricing, booking
  windows).
- **Financial / digital** → which issuer/store and which terms or licence; mind
  legitimacy and the Boundaries above.

### Phase 6 — Commit

Close the loop so it actually terminates. State the flip-test result (what could
still change the call, or that nothing can), apply a quick regret test ("if this
is merely fine, am I okay with that?"), and say when to stop. Before the final
push, a last check: is this comfortably affordable, and is it a
regulated/high-consequence decision that warrants a professional (see
Boundaries)? If so, inform and defer rather than push. This is where
commitment-problem people enter the flow and information-problem people exit it.

## Output — two parts, in this order

Deliver the result in two distinct parts using `templates/deliverable.md`. They
do different jobs; don't blend them.

**Part 1 — The Brief (the decision layer; read this).** Short — a minute or two.
The judgment, plus the *full reasoning* behind it: the chain from need → why this
→ the tradeoff → confidence and what would change the call. Add the rules of
thumb, and one line saying how current the prices are. Complete enough to act on
without reading further. This is the only part the person must read.

**Part 2 — The Research Report (the evidence layer; scan or read).** Complete and
scannable, with headers. This is everything the agent
found — the market landscape, the domain lens, the price decomposition, the
decision prices, tech timing, hype-vs-real, insider knowledge, sourcing, source
quality, the candidates in detail, and an honest **confidence & gaps** section
naming what's well-evidenced, what's thin, and what was assumed but not verified.
Its purpose is trust: so the person can see *what the agent knows* and judge
whether the decision is reliable.
