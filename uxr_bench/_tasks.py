"""Embedded benchmark task definitions — 25 tasks across 5 categories."""
from .models import BenchmarkTask, Difficulty, GroundTruth, TaskCategory

BENCHMARK_TASKS: list[BenchmarkTask] = [
    # ================================================================
    # THEMATIC CODING  (TC-001 – TC-005)
    # ================================================================
    BenchmarkTask(
        task_id="TC-001",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.EASY,
        description="Identify themes in a short onboarding friction transcript excerpt",
        input_text=(
            "P: I just — okay, when I first opened the app I had no idea what I was supposed to do. "
            "Like the button was there but I didn't know it was a button? And then I just started clicking "
            "things and eventually I figured it out but it took a while. I actually ended up watching a YouTube "
            "tutorial which I shouldn't have had to do."
        ),
        prompt_template=(
            "You are a UX researcher performing thematic coding. "
            "Read the following interview excerpt and identify the main themes present. "
            "Return ONLY a comma-separated list of theme labels (lowercase, underscored, no explanations).\n\n"
            "Excerpt:\n{input_text}\n\nThemes:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "onboarding_friction",
                "affordance_failure",
                "self_directed_learning",
                "workaround_behavior",
            ],
            rationale=(
                "Participant describes unclear first-run UX (onboarding_friction), inability to perceive "
                "interactive elements (affordance_failure), resorting to external resources "
                "(self_directed_learning), and ad-hoc exploration to compensate (workaround_behavior)."
            ),
        ),
        tags=["onboarding", "discoverability", "mobile"],
    ),
    BenchmarkTask(
        task_id="TC-002",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.MEDIUM,
        description="Identify themes in a transcript excerpt about data sharing attitudes",
        input_text=(
            "P: Honestly I'm pretty careful about what I share. I read the privacy policy — well, I skim it — "
            "and if something feels off I just don't use it. But at the same time, like, I use Google for everything "
            "so clearly I'm not that precious about it. I guess I just want to feel like I have some control, "
            "even if I know I don't really. It's more about trust, right? If a company feels shady I'm out."
        ),
        prompt_template=(
            "You are a UX researcher performing thematic coding. "
            "Read the following interview excerpt and identify the main themes present. "
            "Return ONLY a comma-separated list of theme labels (lowercase, underscored, no explanations).\n\n"
            "Excerpt:\n{input_text}\n\nThemes:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "privacy_concern",
                "perceived_control",
                "trust",
                "behavioral_inconsistency",
            ],
            rationale=(
                "Excerpt shows privacy awareness (privacy_concern), desire for agency over data "
                "(perceived_control), company-level trust judgments (trust), and acknowledged gap "
                "between stated values and behavior (behavioral_inconsistency)."
            ),
        ),
        tags=["privacy", "trust", "attitudes"],
    ),
    BenchmarkTask(
        task_id="TC-003",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.MEDIUM,
        description="Identify themes across a multi-speaker collaboration tools excerpt",
        input_text=(
            "P1: The notifications are just… constant. I've muted like three channels already. "
            "P2: Same. I don't even look at Slack half the time during deep work. "
            "P1: And then you miss something important and someone messages you asking why you didn't respond. "
            "P2: Yeah there's this pressure to always be on. "
            "I: Does that affect how you collaborate with the rest of your team? "
            "P1: Definitely. I'll batch my responses now, do it all at once at like 2pm. "
            "P2: I've started using status messages as a shield basically."
        ),
        prompt_template=(
            "You are a UX researcher performing thematic coding. "
            "Read the following interview excerpt and identify the main themes present. "
            "Return ONLY a comma-separated list of theme labels (lowercase, underscored, no explanations).\n\n"
            "Excerpt:\n{input_text}\n\nThemes:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "notification_fatigue",
                "always_on_pressure",
                "deep_work_protection",
                "workaround_behavior",
            ],
            rationale=(
                "Excerpt surfaces overwhelming notifications (notification_fatigue), social expectation of "
                "constant availability (always_on_pressure), active strategies to create focus time "
                "(deep_work_protection), and coping mechanisms like batching and status shields "
                "(workaround_behavior)."
            ),
        ),
        tags=["collaboration", "notifications", "remote-work"],
    ),
    BenchmarkTask(
        task_id="TC-004",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.HARD,
        description="Identify themes in a complex excerpt about financial app usage psychology",
        input_text=(
            "P: I check it every morning. Like before coffee. I know that's probably bad but — I don't know, "
            "it makes me feel in control? But then if the number is down I'm stressed for the whole day and "
            "that's not great. My partner says I'm obsessed. And I probably am a bit. But my parents never talked "
            "about money and I ended up in a lot of debt in my twenties so now I'm almost the opposite. "
            "Like, I need to know. I need to see the number. My friend uses the same app and she says she hides "
            "the balance sometimes, which I could never do — that would make it worse for me."
        ),
        prompt_template=(
            "You are a UX researcher performing thematic coding. "
            "Read the following interview excerpt and identify the main themes present. "
            "Return ONLY a comma-separated list of theme labels (lowercase, underscored, no explanations).\n\n"
            "Excerpt:\n{input_text}\n\nThemes:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "financial_anxiety",
                "compensatory_behavior",
                "loss_aversion",
                "individual_coping_strategy",
                "formative_experience",
            ],
            rationale=(
                "Shows anxiety-driven checking (financial_anxiety), over-correcting for past debt "
                "(compensatory_behavior), stress from negative numbers (loss_aversion), contrasting "
                "balance-hiding vs balance-checking strategies (individual_coping_strategy), and the role "
                "of money avoidance in childhood (formative_experience)."
            ),
        ),
        tags=["fintech", "psychology", "anxiety"],
    ),
    BenchmarkTask(
        task_id="TC-005",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.HARD,
        description="Identify themes in an abstract discussion about AI tool trust and adoption",
        input_text=(
            "P: The first few times it got something wrong I was really put off. Like I'd checked its output "
            "and it was confidently wrong, which is almost worse than being uncertain. So now I always verify. "
            "But that kind of defeats the purpose, right? Except — I've started to figure out what it's good at "
            "and what it's not. Like for drafting it's great, for facts it's unreliable. So I've adjusted. "
            "I: Does that feel like extra work? "
            "P: At first yes. Now it's just — it's part of how I use it. It's like any tool. You learn its limits."
        ),
        prompt_template=(
            "You are a UX researcher performing thematic coding. "
            "Read the following interview excerpt and identify the main themes present. "
            "Return ONLY a comma-separated list of theme labels (lowercase, underscored, no explanations).\n\n"
            "Excerpt:\n{input_text}\n\nThemes:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "trust_calibration",
                "verification_overhead",
                "capability_mapping",
                "mental_model_development",
                "tool_habituation",
            ],
            rationale=(
                "Participant develops calibrated trust after errors (trust_calibration), adds verification "
                "steps (verification_overhead), learns task-specific strengths and weaknesses "
                "(capability_mapping), builds an internal model of the tool (mental_model_development), "
                "and normalises this into routine usage (tool_habituation)."
            ),
        ),
        tags=["ai-tools", "trust", "adoption"],
    ),
    # ================================================================
    # BIAS DETECTION  (BD-001 – BD-005)
    # ================================================================
    BenchmarkTask(
        task_id="BD-001",
        category=TaskCategory.BIAS_DETECTION,
        difficulty=Difficulty.EASY,
        description="Detect bias in a single leading interview question",
        input_text=(
            "Interviewer question: 'Most users find the new navigation confusing — would you say that's been "
            "your experience too?'"
        ),
        prompt_template=(
            "You are a UX research methodologist reviewing interview questions for bias. "
            "Identify all bias types present in the following question or exchange. "
            "Return ONLY a comma-separated list of bias type labels (lowercase, underscored). "
            "Common types: leading_question, double_barreled, social_desirability, loaded_assumption, "
            "confirmation_bias, anchoring_bias, framing_effect, acquiescence_bias.\n\n"
            "Input:\n{input_text}\n\nBias types detected:"
        ),
        ground_truth=GroundTruth(
            labels=["leading_question", "anchoring_bias"],
            rationale=(
                "The question pre-supplies the expected answer ('confusing') and anchors the participant "
                "to a majority-view framing, both biasing the response direction."
            ),
        ),
        tags=["interview", "leading", "navigation"],
    ),
    BenchmarkTask(
        task_id="BD-002",
        category=TaskCategory.BIAS_DETECTION,
        difficulty=Difficulty.EASY,
        description="Detect a double-barreled question in an interview guide",
        input_text=(
            "Interviewer question: 'How easy is it to use and how often do you use the feature?'"
        ),
        prompt_template=(
            "You are a UX research methodologist reviewing interview questions for bias. "
            "Identify all bias types present in the following question or exchange. "
            "Return ONLY a comma-separated list of bias type labels (lowercase, underscored). "
            "Common types: leading_question, double_barreled, social_desirability, loaded_assumption, "
            "confirmation_bias, anchoring_bias, framing_effect, acquiescence_bias.\n\n"
            "Input:\n{input_text}\n\nBias types detected:"
        ),
        ground_truth=GroundTruth(
            labels=["double_barreled"],
            rationale=(
                "The question asks about two distinct constructs (ease of use AND frequency of use) in a "
                "single question, making it impossible to give a coherent single answer."
            ),
        ),
        tags=["interview", "double-barreled"],
    ),
    BenchmarkTask(
        task_id="BD-003",
        category=TaskCategory.BIAS_DETECTION,
        difficulty=Difficulty.MEDIUM,
        description="Detect multiple biases in a socially-framed question sequence",
        input_text=(
            "Interviewer: 'As a professional, how important is it to you to stay on top of the latest "
            "features in the tools you use? And do you feel like you're making the most of everything "
            "this platform offers?'"
        ),
        prompt_template=(
            "You are a UX research methodologist reviewing interview questions for bias. "
            "Identify all bias types present in the following question or exchange. "
            "Return ONLY a comma-separated list of bias type labels (lowercase, underscored). "
            "Common types: leading_question, double_barreled, social_desirability, loaded_assumption, "
            "confirmation_bias, anchoring_bias, framing_effect, acquiescence_bias.\n\n"
            "Input:\n{input_text}\n\nBias types detected:"
        ),
        ground_truth=GroundTruth(
            labels=["social_desirability", "double_barreled", "loaded_assumption"],
            rationale=(
                "'As a professional' primes socially desirable answers about diligence. Two questions asked "
                "simultaneously (double_barreled). 'Making the most of everything' assumes there is more to "
                "extract — a loaded assumption about under-utilisation."
            ),
        ),
        tags=["interview", "social-desirability", "professional-framing"],
    ),
    BenchmarkTask(
        task_id="BD-004",
        category=TaskCategory.BIAS_DETECTION,
        difficulty=Difficulty.MEDIUM,
        description="Detect confirmation bias in an interviewer's follow-up sequence",
        input_text=(
            "P: I don't really have strong feelings about it either way. "
            "I: But you did say earlier it was 'fine' — would you say the experience was generally positive? "
            "P: I guess it was okay, yeah. "
            "I: And the specific flow — that felt smooth to you? "
            "P: ...Sure."
        ),
        prompt_template=(
            "You are a UX research methodologist reviewing interview questions for bias. "
            "Identify all bias types present in the following question or exchange. "
            "Return ONLY a comma-separated list of bias type labels (lowercase, underscored). "
            "Common types: leading_question, double_barreled, social_desirability, loaded_assumption, "
            "confirmation_bias, anchoring_bias, framing_effect, acquiescence_bias.\n\n"
            "Input:\n{input_text}\n\nBias types detected:"
        ),
        ground_truth=GroundTruth(
            labels=["confirmation_bias", "leading_question", "acquiescence_bias"],
            rationale=(
                "The interviewer selectively reinforces a neutral-to-positive interpretation "
                "(confirmation_bias), reframes ambiguous responses as positive (leading_question), and "
                "the participant's '...Sure' shows acquiescence under mild pressure (acquiescence_bias)."
            ),
        ),
        tags=["interview", "confirmation-bias", "follow-up"],
    ),
    BenchmarkTask(
        task_id="BD-005",
        category=TaskCategory.BIAS_DETECTION,
        difficulty=Difficulty.HARD,
        description="Detect subtle framing effects and loaded language across a multi-question sequence",
        input_text=(
            "I: When you think about switching to a competitor, what would need to go really wrong for you "
            "to do that? "
            "P: I don't know, something pretty bad I suppose. "
            "I: Right, so it's quite a high bar — things would need to break down significantly. "
            "And given that, how committed would you say you are to staying with the current product?"
        ),
        prompt_template=(
            "You are a UX research methodologist reviewing interview questions for bias. "
            "Identify all bias types present in the following question or exchange. "
            "Return ONLY a comma-separated list of bias type labels (lowercase, underscored). "
            "Common types: leading_question, double_barreled, social_desirability, loaded_assumption, "
            "confirmation_bias, anchoring_bias, framing_effect, acquiescence_bias.\n\n"
            "Input:\n{input_text}\n\nBias types detected:"
        ),
        ground_truth=GroundTruth(
            labels=["framing_effect", "leading_question", "anchoring_bias", "confirmation_bias"],
            rationale=(
                "'What would need to go really wrong' frames switching as extreme (framing_effect). "
                "The follow-up summarises a vague response as strong commitment (leading_question). "
                "'High bar' and 'break down significantly' anchor to a loss frame (anchoring_bias). "
                "The interviewer confirms their hypothesis about loyalty (confirmation_bias)."
            ),
        ),
        tags=["interview", "framing", "retention"],
    ),
    # ================================================================
    # INSIGHT EXTRACTION  (IE-001 – IE-005)
    # ================================================================
    BenchmarkTask(
        task_id="IE-001",
        category=TaskCategory.INSIGHT_EXTRACTION,
        difficulty=Difficulty.EASY,
        description="Extract a clear actionable insight from converging theme data",
        input_text=(
            "Coded themes from 8 participants: onboarding_friction (n=7), affordance_failure (n=6), "
            "self_directed_learning (n=5). All participants who encountered affordance_failure also reported "
            "onboarding_friction. 5 of 8 sought external help within the first session."
        ),
        prompt_template=(
            "You are a senior UX researcher synthesising coded qualitative data into insights. "
            "Read the following coded data summary and extract the single most important actionable insight. "
            "Express it as: 'Users [behaviour] because [root cause], which means [design implication].' "
            "Keep to 2-3 sentences. No bullet points.\n\n"
            "Coded data:\n{input_text}\n\nInsight:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "onboarding",
                "affordance",
                "external_help",
                "first_session",
                "design_implication",
                "in_product_guidance",
            ],
            rationale=(
                "Insight should connect: first-session failure driven by invisible UI affordances, "
                "leading participants to seek external help, implying a need for in-product guidance "
                "or affordance redesign."
            ),
        ),
        tags=["onboarding", "synthesis", "convergent"],
    ),
    BenchmarkTask(
        task_id="IE-002",
        category=TaskCategory.INSIGHT_EXTRACTION,
        difficulty=Difficulty.MEDIUM,
        description="Extract a nuanced insight from mixed-signal coded data",
        input_text=(
            "Coded themes: privacy_concern (n=9), behavioral_inconsistency (n=8), perceived_control (n=6), "
            "trust (n=7). Participants who reported high privacy_concern were equally likely to report "
            "behavioral_inconsistency (r=0.81). Perceived_control was strongly associated with trust (r=0.74) "
            "but weakly associated with actual data-sharing behavior."
        ),
        prompt_template=(
            "You are a senior UX researcher synthesising coded qualitative data into insights. "
            "Read the following coded data summary and extract the single most important actionable insight. "
            "Express it as: 'Users [behaviour] because [root cause], which means [design implication].' "
            "Keep to 2-3 sentences. No bullet points.\n\n"
            "Coded data:\n{input_text}\n\nInsight:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "privacy_paradox",
                "perceived_control",
                "trust",
                "behavioral_gap",
                "design_opportunity",
                "control_mechanism",
            ],
            rationale=(
                "The insight should name the privacy paradox: stated concern does not predict behavior; "
                "perceived control drives trust independently of actual data-sharing, suggesting design "
                "should prioritise visible control mechanisms over privacy communication."
            ),
        ),
        tags=["privacy", "trust", "paradox", "mixed-signals"],
    ),
    BenchmarkTask(
        task_id="IE-003",
        category=TaskCategory.INSIGHT_EXTRACTION,
        difficulty=Difficulty.MEDIUM,
        description="Extract a design opportunity insight from behavioral pattern data",
        input_text=(
            "Coded themes: notification_fatigue (n=12), deep_work_protection (n=10), workaround_behavior (n=11). "
            "All workaround_behavior instances involved participants creating their own interruption-management "
            "systems (batching, status messages, channel muting). None reported using built-in DND or focus modes. "
            "When asked, 9 of 12 were unaware these features existed."
        ),
        prompt_template=(
            "You are a senior UX researcher synthesising coded qualitative data into insights. "
            "Read the following coded data summary and extract the single most important actionable insight. "
            "Express it as: 'Users [behaviour] because [root cause], which means [design implication].' "
            "Keep to 2-3 sentences. No bullet points.\n\n"
            "Coded data:\n{input_text}\n\nInsight:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "workaround",
                "discoverability",
                "built_in_feature",
                "awareness_gap",
                "notification",
                "focus_mode",
            ],
            rationale=(
                "Insight: users build manual workarounds because they are unaware of built-in focus features, "
                "implying a discoverability failure rather than a feature gap — the design opportunity is "
                "surfacing existing capabilities, not building new ones."
            ),
        ),
        tags=["notifications", "discoverability", "workarounds", "feature-awareness"],
    ),
    BenchmarkTask(
        task_id="IE-004",
        category=TaskCategory.INSIGHT_EXTRACTION,
        difficulty=Difficulty.HARD,
        description="Extract a hedged insight from competing evidence across expertise levels",
        input_text=(
            "Coded themes: trust_calibration (n=8), verification_overhead (n=7), tool_habituation (n=5), "
            "capability_mapping (n=6). Expert users (n=4) showed high capability_mapping and low "
            "verification_overhead. Novice users (n=4) showed high verification_overhead and low "
            "trust_calibration. Tool_habituation appeared only in the expert group after 3+ months of use. "
            "Capability_mapping preceded habituation in all expert cases."
        ),
        prompt_template=(
            "You are a senior UX researcher synthesising coded qualitative data into insights. "
            "Read the following coded data summary and extract the single most important actionable insight. "
            "Express it as: 'Users [behaviour] because [root cause], which means [design implication].' "
            "Keep to 2-3 sentences. No bullet points.\n\n"
            "Coded data:\n{input_text}\n\nInsight:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "expert_novice",
                "capability_mapping",
                "trust_calibration",
                "habituation",
                "onboarding",
                "user_journey",
                "progression",
            ],
            rationale=(
                "Insight should note the expert-novice split: capability mapping appears to unlock trust "
                "calibration which enables habituation — implying onboarding interventions should "
                "accelerate capability mapping to reduce verification overhead in novice users."
            ),
        ),
        tags=["ai-tools", "expertise", "trust", "longitudinal"],
    ),
    BenchmarkTask(
        task_id="IE-005",
        category=TaskCategory.INSIGHT_EXTRACTION,
        difficulty=Difficulty.HARD,
        description="Extract a longitudinal change insight from wave comparison data",
        input_text=(
            "Wave 1 (n=15, Jan): financial_anxiety (n=13), loss_aversion (n=11), compensatory_behavior (n=9). "
            "Wave 2 (n=13, Apr): financial_anxiety (n=8), loss_aversion (n=7), compensatory_behavior (n=4), "
            "new theme: acceptance (n=6). 6 participants moved from high anxiety to acceptance. "
            "All 6 reported using the balance-hiding feature introduced in the Feb update."
        ),
        prompt_template=(
            "You are a senior UX researcher synthesising coded qualitative data into insights. "
            "Read the following coded data summary and extract the single most important actionable insight. "
            "Express it as: 'Users [behaviour] because [root cause], which means [design implication].' "
            "Keep to 2-3 sentences. No bullet points.\n\n"
            "Coded data:\n{input_text}\n\nInsight:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "anxiety_reduction",
                "feature_impact",
                "balance_hiding",
                "longitudinal",
                "design_impact",
                "information_removal",
            ],
            rationale=(
                "Insight: the balance-hiding feature appears causally linked to reduced anxiety — notable "
                "because it resolves pain by removing information rather than adding it, challenging the "
                "default 'more transparency = better' design assumption."
            ),
        ),
        tags=["fintech", "longitudinal", "feature-impact", "design-insight"],
    ),
    # ================================================================
    # GUIDE EVALUATION  (GE-001 – GE-005)
    # ================================================================
    BenchmarkTask(
        task_id="GE-001",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.EASY,
        description="Score a well-constructed discussion guide (expected high score ~82)",
        input_text=(
            "Discussion Guide — Mobile Banking App\n"
            "Duration: 60 min | Participants: Mobile banking users, 18–45\n\n"
            "1. Tell me about the last time you managed money on your phone. Walk me through what you did. [5 min]\n"
            "   Probe: What made you choose to do it then?\n"
            "   Probe: Was there anything that felt off or unexpected?\n\n"
            "2. How do you typically decide which app to open when you need to check something financial? [10 min]\n"
            "   Probe: Has that changed recently?\n\n"
            "3. Describe a time when a financial app made you feel uncertain or anxious. [10 min]\n"
            "   Probe: What was happening in the app at that point?\n"
            "   Probe: What did you do next?\n\n"
            "4. What would make you trust a financial app more than you do now? [10 min]\n\n"
            "5. If you could change one thing about how your main banking app works, what would it be "
            "and why? [10 min]\n\n"
            "6. Is there anything about your relationship with money and apps we haven't talked about "
            "that you think is important? [5 min]"
        ),
        prompt_template=(
            "You are an expert UX research methodologist evaluating a discussion guide. "
            "Score the guide from 0–100 across these dimensions: "
            "neutrality (no leading questions), probe depth (follow-ups present), "
            "sequencing (warm-up to specific), coverage (topic breadth), time realism. "
            "Return ONLY a single integer score from 0 to 100.\n\n"
            "Guide:\n{input_text}\n\nScore:"
        ),
        ground_truth=GroundTruth(
            labels=["neutrality", "probe_depth", "sequencing", "coverage", "time_realism"],
            score=82.0,
            rationale=(
                "Strong neutral open questions, good probes, logical warm-to-specific sequencing, covers "
                "attitudes/behaviour/trust/improvement. Slight deduction: Q4 could use probes."
            ),
        ),
        tags=["guide-quality", "fintech", "high-quality"],
    ),
    BenchmarkTask(
        task_id="GE-002",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.EASY,
        description="Score a poor discussion guide with leading questions and no probes (expected ~28)",
        input_text=(
            "Discussion Guide — New Feature Evaluation\n"
            "Duration: 45 min\n\n"
            "1. Did you find the new dashboard helpful? [5 min]\n"
            "2. Most people find the new layout much easier to navigate — do you agree? [10 min]\n"
            "3. What do you like most about the new design? [10 min]\n"
            "4. Would you recommend this product to a friend? Why? [10 min]\n"
            "5. Is there anything you didn't like? [5 min]"
        ),
        prompt_template=(
            "You are an expert UX research methodologist evaluating a discussion guide. "
            "Score the guide from 0–100 across these dimensions: "
            "neutrality (no leading questions), probe depth (follow-ups present), "
            "sequencing (warm-up to specific), coverage (topic breadth), time realism. "
            "Return ONLY a single integer score from 0 to 100.\n\n"
            "Guide:\n{input_text}\n\nScore:"
        ),
        ground_truth=GroundTruth(
            labels=["leading_questions", "no_probes", "positive_framing", "shallow_coverage"],
            score=28.0,
            rationale=(
                "Multiple leading and confirmatory questions (Q2 is textbook anchoring bias). No probes. "
                "Questions frame the experience as positive, suppressing negative feedback."
            ),
        ),
        tags=["guide-quality", "poor-quality", "leading"],
    ),
    BenchmarkTask(
        task_id="GE-003",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.MEDIUM,
        description="Score a mixed-quality guide with good structure but weak probes (expected ~61)",
        input_text=(
            "Discussion Guide — Remote Work Tools Study\n"
            "Duration: 50 min | Participants: Knowledge workers using 3+ tools daily\n\n"
            "1. Walk me through a typical workday. What does it look like from the moment you start? [8 min]\n"
            "2. Which tools do you rely on most and why? [8 min]\n"
            "3. Describe a situation where your tools let you down recently. [8 min]\n"
            "4. How do you feel when you have to switch between different tools frequently? [8 min]\n"
            "5. What would your ideal work setup look like? [8 min]\n"
            "6. Is there anything important we missed? [5 min]"
        ),
        prompt_template=(
            "You are an expert UX research methodologist evaluating a discussion guide. "
            "Score the guide from 0–100 across these dimensions: "
            "neutrality (no leading questions), probe depth (follow-ups present), "
            "sequencing (warm-up to specific), coverage (topic breadth), time realism. "
            "Return ONLY a single integer score from 0 to 100.\n\n"
            "Guide:\n{input_text}\n\nScore:"
        ),
        ground_truth=GroundTruth(
            labels=["neutral_questions", "weak_probes", "good_sequencing", "moderate_coverage"],
            score=61.0,
            rationale=(
                "Questions are largely neutral and open. Sequencing is sensible. However, no probes listed "
                "under any question — major gap. Coverage is decent but misses collaboration and workaround "
                "behaviors specifically."
            ),
        ),
        tags=["guide-quality", "remote-work", "mixed-quality"],
    ),
    BenchmarkTask(
        task_id="GE-004",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.MEDIUM,
        description="Score a well-probed guide that is severely time-unrealistic (expected ~66)",
        input_text=(
            "Discussion Guide — AI Assistant Adoption Study\n"
            "Duration: 30 min | Participants: AI tool early adopters\n\n"
            "1. Tell me about the first time you used an AI assistant. [3 min]\n"
            "2. Walk me through the last time you used an AI tool at work — step by step. [5 min]\n"
            "   Probe: What made you decide to use it then?\n"
            "   Probe: What did you do with the output?\n"
            "3. Describe a time when the AI tool produced something surprising — good or bad. [5 min]\n"
            "   Probe: How did that affect how you use it now?\n"
            "4. How has your trust in AI tools changed since you first started? [5 min]\n"
            "   Probe: What specifically caused that shift?\n"
            "5. Imagine explaining to a colleague how to use AI tools well — what would you tell them? [5 min]\n"
            "6. What worries you, if anything, about using AI at work? [5 min]\n"
            "   Probe: Have you changed any work habits because of that?\n"
            "7. What would make you use AI tools even more than you do now? [5 min]\n"
            "8. If AI tools disappeared tomorrow, what would you miss? What wouldn't you miss? [3 min]"
        ),
        prompt_template=(
            "You are an expert UX research methodologist evaluating a discussion guide. "
            "Score the guide from 0–100 across these dimensions: "
            "neutrality (no leading questions), probe depth (follow-ups present), "
            "sequencing (warm-up to specific), coverage (topic breadth), time realism. "
            "Return ONLY a single integer score from 0 to 100.\n\n"
            "Guide:\n{input_text}\n\nScore:"
        ),
        ground_truth=GroundTruth(
            labels=["time_overrun", "good_probes", "good_coverage", "neutral_questions"],
            score=66.0,
            rationale=(
                "Questions neutral and well-probed. Coverage is good. However, guide is severely "
                "time-unrealistic: 8 questions with probes in 30 minutes requires 60–75 minutes. "
                "Significant deduction for time realism."
            ),
        ),
        tags=["guide-quality", "ai-tools", "time-realism"],
    ),
    BenchmarkTask(
        task_id="GE-005",
        category=TaskCategory.GUIDE_EVALUATION,
        difficulty=Difficulty.HARD,
        description="Score a technically correct guide with survivor bias built into sampling (expected ~71)",
        input_text=(
            "Discussion Guide — Subscription Retention Study\n"
            "Duration: 45 min | Participants: Users who have stayed subscribed 12+ months\n\n"
            "1. Tell me about your journey with this product — how did you first come across it? [5 min]\n"
            "   Probe: What were you hoping it would do for you at the time?\n"
            "2. Walk me through how you use it on a typical week. [8 min]\n"
            "   Probe: Has that changed from when you first started?\n"
            "3. Describe the last time the product really delivered for you. [8 min]\n"
            "   Probe: What made that moment work?\n"
            "4. What would need to change for you to consider cancelling? [8 min]\n"
            "   Probe: Has anything ever made you come close to cancelling?\n"
            "5. How does this product compare to alternatives you've tried? [8 min]\n"
            "   Probe: What keeps you here rather than elsewhere?\n"
            "6. What would make this even better for you? [5 min]"
        ),
        prompt_template=(
            "You are an expert UX research methodologist evaluating a discussion guide. "
            "Score the guide from 0–100 across these dimensions: "
            "neutrality (no leading questions), probe depth (follow-ups present), "
            "sequencing (warm-up to specific), coverage (topic breadth), time realism. "
            "Return ONLY a single integer score from 0 to 100.\n\n"
            "Guide:\n{input_text}\n\nScore:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "hypothesis_shielding",
                "survivor_bias",
                "participant_framing",
                "good_probes",
                "moderate_neutrality",
            ],
            score=71.0,
            rationale=(
                "Good probe depth and neutral question language. However, sampling only retained users "
                "builds in survivor bias and hypothesis shielding. Q3 primes positive recall. Technically "
                "competent but the research design undermines the stated retention objective."
            ),
        ),
        tags=["guide-quality", "retention", "survivor-bias", "hard"],
    ),
    # ================================================================
    # SAY-DO GAP  (SD-001 – SD-005)
    # ================================================================
    BenchmarkTask(
        task_id="SD-001",
        category=TaskCategory.SAY_DO_GAP,
        difficulty=Difficulty.EASY,
        description="Detect a classic privacy paradox say-do gap",
        input_text=(
            "Stated (interview): 'I'm very careful about my data. I don't share anything I don't have to. "
            "Privacy is really important to me — I've turned off location on most apps.' "
            "Observed (usage logs): The participant has location enabled for 11 of 14 installed apps, "
            "including shopping and weather apps. They have accepted all cookie banners without modification "
            "in their last 23 browsing sessions."
        ),
        prompt_template=(
            "You are a UX researcher analysing Say-Do Gaps — discrepancies between what participants say "
            "they do and what they actually do. "
            "Identify all gaps present in the following data. "
            "Return ONLY a comma-separated list of gap type labels (lowercase, underscored). "
            "Common types: privacy_paradox, frequency_misreport, feature_usage_gap, "
            "attitude_behavior_inconsistency, social_desirability_inflation, self_serving_rationalization, "
            "competitor_denial.\n\n"
            "Input:\n{input_text}\n\nSay-Do gaps detected:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "privacy_paradox",
                "attitude_behavior_inconsistency",
                "social_desirability_inflation",
            ],
            rationale=(
                "Classic privacy paradox: stated strong privacy values contradict actual permissive "
                "data-sharing behavior. Discrepancy driven by social desirability and genuine "
                "attitude-behavior inconsistency."
            ),
        ),
        tags=["privacy", "paradox", "attitudes"],
    ),
    BenchmarkTask(
        task_id="SD-002",
        category=TaskCategory.SAY_DO_GAP,
        difficulty=Difficulty.EASY,
        description="Detect a frequency misreport say-do gap",
        input_text=(
            "Stated (interview): 'I use the dashboard every single day — it's the first thing I check "
            "in the morning, without fail.' "
            "Observed (telemetry): The participant opened the dashboard on 9 of the last 30 days. "
            "Average gap between sessions: 3.2 days. No sessions logged before 10am."
        ),
        prompt_template=(
            "You are a UX researcher analysing Say-Do Gaps — discrepancies between what participants say "
            "they do and what they actually do. "
            "Identify all gaps present in the following data. "
            "Return ONLY a comma-separated list of gap type labels (lowercase, underscored). "
            "Common types: privacy_paradox, frequency_misreport, feature_usage_gap, "
            "attitude_behavior_inconsistency, social_desirability_inflation, self_serving_rationalization, "
            "competitor_denial.\n\n"
            "Input:\n{input_text}\n\nSay-Do gaps detected:"
        ),
        ground_truth=GroundTruth(
            labels=["frequency_misreport", "social_desirability_inflation"],
            rationale=(
                "Participant claims daily morning use; telemetry shows ~3-day average gaps and no morning "
                "sessions. Clear frequency misreport, likely inflated by social desirability."
            ),
        ),
        tags=["frequency", "telemetry", "engagement"],
    ),
    BenchmarkTask(
        task_id="SD-003",
        category=TaskCategory.SAY_DO_GAP,
        difficulty=Difficulty.MEDIUM,
        description="Detect attitude-behavior inconsistency in feature preference data",
        input_text=(
            "Stated (interview): 'I like things simple. I don't want a million features — just give me "
            "the core stuff that works. I actively avoid complex tools.' "
            "Observed (usage logs): The participant has enabled 14 of 17 available advanced settings. "
            "They use keyboard shortcuts exclusively, have customised their workspace layout twice, "
            "and have integrated 4 third-party plugins. They are in the top 5% of feature usage breadth."
        ),
        prompt_template=(
            "You are a UX researcher analysing Say-Do Gaps — discrepancies between what participants say "
            "they do and what they actually do. "
            "Identify all gaps present in the following data. "
            "Return ONLY a comma-separated list of gap type labels (lowercase, underscored). "
            "Common types: privacy_paradox, frequency_misreport, feature_usage_gap, "
            "attitude_behavior_inconsistency, social_desirability_inflation, self_serving_rationalization, "
            "competitor_denial.\n\n"
            "Input:\n{input_text}\n\nSay-Do gaps detected:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "attitude_behavior_inconsistency",
                "feature_usage_gap",
                "self_serving_rationalization",
            ],
            rationale=(
                "Stated preference for simplicity is directly contradicted by extensive power-user behavior. "
                "The 'I avoid complex tools' statement functions as self-serving rationalization "
                "of a discerning-user identity."
            ),
        ),
        tags=["feature-usage", "power-user", "identity"],
    ),
    BenchmarkTask(
        task_id="SD-004",
        category=TaskCategory.SAY_DO_GAP,
        difficulty=Difficulty.MEDIUM,
        description="Detect competitor denial gap in a within-interview contradiction",
        input_text=(
            "Exchange 1 (15 min in): "
            "I: 'Do you use any competitor products?' "
            "P: 'No, not really. I'm pretty loyal to this one.' "
            "Exchange 2 (32 min in, discussing workflow): "
            "P: '...and then I'll usually run it through Notion first to structure it, and sometimes "
            "I'll check how the other tool — you know, the Linear alternative — handles it before I decide.'"
        ),
        prompt_template=(
            "You are a UX researcher analysing Say-Do Gaps — discrepancies between what participants say "
            "they do and what they actually do. "
            "Identify all gaps present in the following data. "
            "Return ONLY a comma-separated list of gap type labels (lowercase, underscored). "
            "Common types: privacy_paradox, frequency_misreport, feature_usage_gap, "
            "attitude_behavior_inconsistency, social_desirability_inflation, self_serving_rationalization, "
            "competitor_denial.\n\n"
            "Input:\n{input_text}\n\nSay-Do gaps detected:"
        ),
        ground_truth=GroundTruth(
            labels=["competitor_denial", "attitude_behavior_inconsistency"],
            rationale=(
                "Explicit denial of competitor use (Exchange 1) contradicted by casual mention of two "
                "competitor tools in workflow context (Exchange 2). Competitor denial driven by brand "
                "loyalty identity."
            ),
        ),
        tags=["competitor", "loyalty", "within-interview"],
    ),
    BenchmarkTask(
        task_id="SD-005",
        category=TaskCategory.SAY_DO_GAP,
        difficulty=Difficulty.HARD,
        description="Detect subtle self-serving rationalization in retrospective purchase description",
        input_text=(
            "Stated (interview): 'I never make impulsive purchases. I always research before I buy — "
            "I'll spend a week comparing options, reading reviews, making sure it's the right decision. "
            "I bought the premium plan because after careful analysis I determined it was clearly the best value.' "
            "Observed (purchase log): The participant upgraded from free to premium 4 minutes after clicking "
            "an in-app upsell banner during a session in which they had been blocked by a paywall three times. "
            "No external review sites were visited in the 30 days prior to purchase."
        ),
        prompt_template=(
            "You are a UX researcher analysing Say-Do Gaps — discrepancies between what participants say "
            "they do and what they actually do. "
            "Identify all gaps present in the following data. "
            "Return ONLY a comma-separated list of gap type labels (lowercase, underscored). "
            "Common types: privacy_paradox, frequency_misreport, feature_usage_gap, "
            "attitude_behavior_inconsistency, social_desirability_inflation, self_serving_rationalization, "
            "competitor_denial.\n\n"
            "Input:\n{input_text}\n\nSay-Do gaps detected:"
        ),
        ground_truth=GroundTruth(
            labels=[
                "self_serving_rationalization",
                "attitude_behavior_inconsistency",
                "social_desirability_inflation",
            ],
            rationale=(
                "Participant retrospectively constructs a deliberate, rational decision narrative around a "
                "friction-driven, 4-minute impulse purchase. Self-serving rationalization to maintain a "
                "self-image as a discerning, rational consumer."
            ),
        ),
        tags=["purchase", "rationalization", "impulse", "retrospective"],
    ),
]
