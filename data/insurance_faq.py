"""
Mock insurance FAQ data for the POC.
This includes common questions about various insurance types.
"""

INSURANCE_FAQ_DATA = [
    # Life Insurance FAQs
    {
        "question": "What is term life insurance?",
        "answer": "Term life insurance provides coverage for a specific period (term), typically 10, 20, or 30 years. If the insured person passes away during the term, the beneficiaries receive a death benefit. It's generally the most affordable type of life insurance.",
        "category": "life_insurance",
        "keywords": ["term life", "life insurance", "death benefit", "coverage period"],
    },
    {
        "question": "What is whole life insurance?",
        "answer": "Whole life insurance provides lifetime coverage and includes a cash value component that grows over time. Premiums remain level throughout your life, and the policy builds cash value that you can borrow against. It's more expensive than term life but offers permanent protection.",
        "category": "life_insurance",
        "keywords": [
            "whole life",
            "permanent insurance",
            "cash value",
            "lifetime coverage",
        ],
    },
    {
        "question": "How much life insurance do I need?",
        "answer": "A common rule of thumb is to have coverage worth 10-12 times your annual income. However, consider factors like outstanding debts (mortgage, loans), future expenses (children's education), funeral costs, and your family's ongoing living expenses. A financial advisor can help calculate your specific needs.",
        "category": "life_insurance",
        "keywords": ["coverage amount", "how much insurance", "insurance calculation"],
    },
    # Health Insurance FAQs
    {
        "question": "What is a health insurance deductible?",
        "answer": "A deductible is the amount you pay out-of-pocket for healthcare services before your insurance begins to pay. For example, with a $1,000 deductible, you pay the first $1,000 of covered services yourself, then your insurance kicks in. Plans with higher deductibles typically have lower monthly premiums.",
        "category": "health_insurance",
        "keywords": ["deductible", "out-of-pocket", "health insurance", "premium"],
    },
    {
        "question": "What is the difference between HMO and PPO?",
        "answer": "HMO (Health Maintenance Organization) requires you to choose a primary care physician and get referrals for specialists, but typically has lower premiums. PPO (Preferred Provider Organization) offers more flexibility to see any doctor without referrals, but usually costs more. PPO also covers out-of-network care at a reduced rate.",
        "category": "health_insurance",
        "keywords": ["HMO", "PPO", "network", "primary care physician"],
    },
    {
        "question": "What is co-insurance?",
        "answer": "Co-insurance is the percentage of costs you pay after meeting your deductible. For example, with 20% co-insurance, you pay 20% of the bill and insurance pays 80%. This continues until you reach your out-of-pocket maximum for the year.",
        "category": "health_insurance",
        "keywords": [
            "co-insurance",
            "cost sharing",
            "percentage",
            "out-of-pocket maximum",
        ],
    },
    # Auto Insurance FAQs
    {
        "question": "What does comprehensive auto insurance cover?",
        "answer": "Comprehensive coverage protects your vehicle from non-collision damage such as theft, vandalism, fire, natural disasters, falling objects, and animal collisions. It does not cover collision damage or liability. It's optional unless required by your lender.",
        "category": "auto_insurance",
        "keywords": [
            "comprehensive",
            "auto insurance",
            "theft",
            "vandalism",
            "non-collision",
        ],
    },
    {
        "question": "What is collision coverage?",
        "answer": "Collision coverage pays for damage to your vehicle resulting from a collision with another vehicle or object, regardless of who is at fault. It covers repairs or replacement up to your car's actual cash value, minus your deductible.",
        "category": "auto_insurance",
        "keywords": ["collision", "auto insurance", "accident", "vehicle damage"],
    },
    {
        "question": "What is liability insurance?",
        "answer": "Liability insurance covers damage you cause to other people or their property. It includes bodily injury liability (medical expenses, lost wages) and property damage liability. Most states require minimum liability coverage. It does not cover damage to your own vehicle.",
        "category": "auto_insurance",
        "keywords": [
            "liability",
            "bodily injury",
            "property damage",
            "required coverage",
        ],
    },
    # Home Insurance FAQs
    {
        "question": "What does homeowners insurance typically cover?",
        "answer": "Standard homeowners insurance (HO-3 policy) covers: 1) Dwelling (structure of your home), 2) Other structures (garage, fence), 3) Personal property, 4) Loss of use (temporary housing), 5) Personal liability, 6) Medical payments to others. Coverage includes perils like fire, wind, hail, lightning, and theft.",
        "category": "home_insurance",
        "keywords": ["homeowners", "dwelling", "coverage", "HO-3", "property"],
    },
    {
        "question": "What is replacement cost vs actual cash value?",
        "answer": "Replacement cost coverage pays to replace damaged property with new items of similar kind and quality without deducting for depreciation. Actual cash value pays the depreciated value of items. For example, a 5-year-old roof might cost $10,000 to replace but have an actual cash value of only $6,000.",
        "category": "home_insurance",
        "keywords": [
            "replacement cost",
            "actual cash value",
            "depreciation",
            "valuation",
        ],
    },
    {
        "question": "Does homeowners insurance cover floods?",
        "answer": "No, standard homeowners insurance does not cover flood damage. You need a separate flood insurance policy, typically through the National Flood Insurance Program (NFIP) or private insurers. This is important even if you're not in a high-risk flood zone.",
        "category": "home_insurance",
        "keywords": ["flood", "water damage", "NFIP", "separate policy"],
    },
    # Claims FAQs
    {
        "question": "How do I file an insurance claim?",
        "answer": "To file a claim: 1) Contact your insurance company immediately (phone, app, or online portal), 2) Provide policy number and incident details, 3) Document damage with photos/videos, 4) Get police report if applicable, 5) Keep receipts for expenses, 6) Cooperate with the claims adjuster, 7) Track your claim status through your insurer's portal.",
        "category": "claims",
        "keywords": ["file claim", "claim process", "claims adjuster", "documentation"],
    },
    {
        "question": "How long does it take to process a claim?",
        "answer": "Simple claims may be processed in a few days, while complex claims can take weeks or months. Factors affecting timing include: claim complexity, documentation completeness, investigation requirements, and state regulations. Most insurers must acknowledge claims within a few days and provide regular updates.",
        "category": "claims",
        "keywords": [
            "claim processing time",
            "how long",
            "claim timeline",
            "settlement",
        ],
    },
    {
        "question": "What should I do after a car accident?",
        "answer": "After an accident: 1) Check for injuries and call 911 if needed, 2) Move to safety if possible, 3) Call police to file a report, 4) Exchange information with other drivers (name, insurance, contact), 5) Take photos of damage and scene, 6) Get witness contact info, 7) Notify your insurance company immediately, 8) Do not admit fault at the scene.",
        "category": "claims",
        "keywords": [
            "car accident",
            "accident procedure",
            "what to do",
            "steps after accident",
        ],
    },
    # Policy & Renewal FAQs
    {
        "question": "When should I renew my insurance policy?",
        "answer": "Most insurance policies have annual terms and should be renewed before expiration to avoid coverage gaps. You'll typically receive a renewal notice 30-60 days before expiration. Review your coverage needs annually and shop around for better rates. Set reminders 45 days before expiration to allow time for comparison shopping.",
        "category": "renewal",
        "keywords": ["renewal", "policy expiration", "annual renewal", "coverage gap"],
    },
    {
        "question": "Can I cancel my insurance policy anytime?",
        "answer": "Yes, you can typically cancel most policies anytime, but consider: 1) You may owe a cancellation fee, 2) You might get a prorated refund, 3) Some policies have minimum terms, 4) Gaps in coverage can increase future rates, 5) You may need proof of new coverage first (especially auto insurance). Always secure new coverage before canceling.",
        "category": "policy",
        "keywords": ["cancel policy", "cancellation", "refund", "policy termination"],
    },
    {
        "question": "What factors affect my insurance premium?",
        "answer": "Common factors include: Age, location, coverage amount, deductible level, claims history, credit score (where allowed), for auto: driving record and vehicle type, for home: home age and construction, for health: age and tobacco use, for life: age and health status. Bundling policies and maintaining good history can reduce premiums.",
        "category": "policy",
        "keywords": ["premium", "rates", "cost factors", "pricing", "discounts"],
    },
    # General Insurance FAQs
    {
        "question": "What is an insurance deductible?",
        "answer": "A deductible is the amount you must pay out-of-pocket before your insurance coverage begins to pay for a claim. Higher deductibles typically result in lower premiums, while lower deductibles mean higher premiums but less out-of-pocket expense when filing a claim.",
        "category": "general",
        "keywords": ["deductible", "out-of-pocket", "premium", "cost"],
    },
    {
        "question": "What does bundling insurance mean?",
        "answer": "Bundling means purchasing multiple insurance policies (such as home and auto) from the same insurance company. Insurers typically offer discounts of 15-25% for bundling policies. It also simplifies management by having one point of contact and coordinated renewal dates.",
        "category": "general",
        "keywords": ["bundling", "multi-policy", "discount", "package deal"],
    },
    {
        "question": "What is an insurance rider or endorsement?",
        "answer": "A rider (also called endorsement) is an addition to your insurance policy that provides extra coverage or modifies existing coverage. Examples include jewelry riders for homeowners insurance, umbrella liability coverage, or waiver of premium riders for life insurance. They typically cost extra but customize your policy to your needs.",
        "category": "general",
        "keywords": [
            "rider",
            "endorsement",
            "additional coverage",
            "policy modification",
        ],
    },
    # Contact & Support FAQs
    {
        "question": "How can I contact customer support?",
        "answer": "You can reach our customer support team through multiple channels: 1) Phone: 1-800-INSURANCE (24/7), 2) Email: support@aiinsurance.com, 3) Live chat on our website and mobile app, 4) Visit a local branch office, 5) Social media direct messages. For emergencies and claims, call our 24/7 hotline.",
        "category": "support",
        "keywords": [
            "contact",
            "customer support",
            "phone number",
            "help",
            "assistance",
        ],
    },
    {
        "question": "How do I update my policy information?",
        "answer": "Update your policy information by: 1) Logging into your online account portal, 2) Calling customer service, 3) Using our mobile app, 4) Emailing your agent. Important updates include: address changes, additional drivers/vehicles, home improvements, beneficiary changes. Some changes may affect your premium.",
        "category": "support",
        "keywords": [
            "update policy",
            "change information",
            "modify coverage",
            "account update",
        ],
    },
]


def get_all_faqs():
    """Return all FAQ data."""
    return INSURANCE_FAQ_DATA


def get_faqs_by_category(category: str):
    """Get FAQs filtered by category."""
    return [faq for faq in INSURANCE_FAQ_DATA if faq["category"] == category]


def get_categories():
    """Get list of all categories."""
    return list(set(faq["category"] for faq in INSURANCE_FAQ_DATA))
