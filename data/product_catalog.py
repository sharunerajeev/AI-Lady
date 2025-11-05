"""
Comprehensive product catalog with variants, eligibility criteria, and pricing.
This serves as the knowledge base for the recommendation engine.
"""

PRODUCT_CATALOG = {
    "health_insurance": {
        "category": "Health Insurance",
        "description": "Medical coverage for healthcare expenses",
        "products": [
            {
                "id": "health_basic",
                "name": "Basic Health Plan",
                "type": "Individual",
                "monthly_premium_range": "$150 - $250",
                "coverage_amount": "$50,000",
                "features": [
                    "Hospitalization coverage",
                    "Emergency care",
                    "Generic prescription drugs",
                    "Annual health checkup",
                    "Network hospitals only"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 65,
                    "employment_status": ["employed", "self-employed", "unemployed"],
                    "pre_existing_conditions": "Limited coverage after 2 years"
                },
                "best_for": [
                    "Young professionals",
                    "Single individuals",
                    "Budget-conscious customers",
                    "Healthy individuals with no major health concerns"
                ],
                "deductible": "$2,000",
                "out_of_pocket_max": "$6,000"
            },
            {
                "id": "health_premium",
                "name": "Premium Health Plan",
                "type": "Individual",
                "monthly_premium_range": "$350 - $500",
                "coverage_amount": "$200,000",
                "features": [
                    "Comprehensive hospitalization",
                    "Emergency and urgent care",
                    "Brand-name prescription drugs",
                    "Specialist consultations",
                    "Mental health services",
                    "Preventive care",
                    "International coverage",
                    "Out-of-network coverage available"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 70,
                    "employment_status": ["employed", "self-employed"],
                    "pre_existing_conditions": "Covered from day 1"
                },
                "best_for": [
                    "Individuals with pre-existing conditions",
                    "Those seeking comprehensive coverage",
                    "Frequent travelers",
                    "Higher income earners"
                ],
                "deductible": "$500",
                "out_of_pocket_max": "$3,000"
            },
            {
                "id": "health_family",
                "name": "Family Health Plan",
                "type": "Family",
                "monthly_premium_range": "$600 - $900",
                "coverage_amount": "$500,000 (shared)",
                "features": [
                    "Coverage for up to 6 family members",
                    "Maternity and newborn care",
                    "Pediatric care",
                    "Dental and vision (basic)",
                    "Hospitalization for all members",
                    "Prescription drug coverage",
                    "Annual health checkups for all",
                    "Vaccination coverage for children"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 75,
                    "family_size": {"min": 2, "max": 6},
                    "employment_status": ["employed", "self-employed"],
                    "pre_existing_conditions": "Covered after 1 year"
                },
                "best_for": [
                    "Families with children",
                    "Couples planning to have children",
                    "Multi-generational households",
                    "Those seeking comprehensive family coverage"
                ],
                "deductible": "$3,000 (family)",
                "out_of_pocket_max": "$12,000 (family)"
            }
        ]
    },
    "life_insurance": {
        "category": "Life Insurance",
        "description": "Financial protection for your loved ones",
        "products": [
            {
                "id": "life_basic",
                "name": "Basic Term Life",
                "type": "Term Life",
                "monthly_premium_range": "$20 - $50",
                "coverage_amount": "$100,000",
                "term_length": "10 years",
                "features": [
                    "Death benefit payout",
                    "Fixed premium for term",
                    "No cash value",
                    "Simple application process"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 55,
                    "health_status": "Good health required",
                    "income_requirement": "Minimum $25,000/year"
                },
                "best_for": [
                    "Young families",
                    "First-time buyers",
                    "Budget-conscious individuals",
                    "Those with temporary coverage needs"
                ],
                "renewable": True,
                "convertible": False
            },
            {
                "id": "life_premium",
                "name": "Premium Whole Life",
                "type": "Whole Life",
                "monthly_premium_range": "$200 - $400",
                "coverage_amount": "$500,000",
                "term_length": "Lifetime",
                "features": [
                    "Lifetime coverage",
                    "Cash value accumulation",
                    "Policy loan options",
                    "Dividend payments (potential)",
                    "Estate planning benefits",
                    "Tax-deferred growth"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 65,
                    "health_status": "Medical exam required",
                    "income_requirement": "Minimum $75,000/year"
                },
                "best_for": [
                    "High-income earners",
                    "Estate planning needs",
                    "Long-term financial planning",
                    "Those seeking investment component"
                ],
                "renewable": "N/A (lifetime coverage)",
                "convertible": "N/A"
            },
            {
                "id": "life_family",
                "name": "Family Protection Plan",
                "type": "Term Life with Living Benefits",
                "monthly_premium_range": "$100 - $200",
                "coverage_amount": "$300,000",
                "term_length": "20-30 years",
                "features": [
                    "Death benefit for dependents",
                    "Critical illness rider",
                    "Disability income rider",
                    "Child coverage included",
                    "Return of premium option",
                    "Flexible term lengths"
                ],
                "eligibility": {
                    "min_age": 25,
                    "max_age": 60,
                    "dependents": "Minimum 1 dependent",
                    "health_status": "Standard health required",
                    "income_requirement": "Minimum $50,000/year"
                },
                "best_for": [
                    "Parents with young children",
                    "Sole breadwinners",
                    "Those with mortgages",
                    "Families with special needs dependents"
                ],
                "renewable": True,
                "convertible": True
            }
        ]
    },
    "auto_insurance": {
        "category": "Auto Insurance",
        "description": "Vehicle protection and liability coverage",
        "products": [
            {
                "id": "auto_basic",
                "name": "Basic Auto Coverage",
                "type": "Liability Only",
                "monthly_premium_range": "$80 - $150",
                "coverage_limits": {
                    "bodily_injury": "$25,000 per person / $50,000 per accident",
                    "property_damage": "$25,000",
                    "comprehensive": "Not included",
                    "collision": "Not included"
                },
                "features": [
                    "Minimum state-required coverage",
                    "Liability protection",
                    "Uninsured motorist coverage",
                    "24/7 claims support"
                ],
                "eligibility": {
                    "min_age": 18,
                    "max_age": 100,
                    "driving_history": "Some violations acceptable",
                    "vehicle_age": "Any age",
                    "credit_score": "No minimum"
                },
                "best_for": [
                    "Older vehicles (>10 years)",
                    "Budget-conscious drivers",
                    "Low-value vehicles",
                    "Drivers with less-than-perfect records"
                ],
                "deductible": "N/A"
            },
            {
                "id": "auto_premium",
                "name": "Premium Auto Protection",
                "type": "Full Coverage",
                "monthly_premium_range": "$200 - $350",
                "coverage_limits": {
                    "bodily_injury": "$100,000 per person / $300,000 per accident",
                    "property_damage": "$100,000",
                    "comprehensive": "Actual cash value",
                    "collision": "Actual cash value"
                },
                "features": [
                    "Comprehensive and collision coverage",
                    "Rental car reimbursement",
                    "Roadside assistance",
                    "Gap insurance",
                    "New car replacement",
                    "Accident forgiveness",
                    "Vanishing deductible"
                ],
                "eligibility": {
                    "min_age": 21,
                    "max_age": 100,
                    "driving_history": "Clean record preferred",
                    "vehicle_age": "Recommended for vehicles <5 years",
                    "credit_score": "Good (650+)"
                },
                "best_for": [
                    "New or expensive vehicles",
                    "Leased or financed cars",
                    "Drivers with clean records",
                    "Those seeking maximum protection"
                ],
                "deductible": "$500 (comprehensive/collision)"
            },
            {
                "id": "auto_family",
                "name": "Family Auto Bundle",
                "type": "Multi-Vehicle Coverage",
                "monthly_premium_range": "$300 - $500",
                "coverage_limits": {
                    "bodily_injury": "$250,000 per person / $500,000 per accident",
                    "property_damage": "$100,000",
                    "comprehensive": "Actual cash value (all vehicles)",
                    "collision": "Actual cash value (all vehicles)"
                },
                "features": [
                    "Coverage for up to 4 vehicles",
                    "Teen driver coverage",
                    "Good student discounts",
                    "Multi-vehicle discount (up to 25%)",
                    "Umbrella liability option",
                    "Rideshare coverage available",
                    "All premium features included"
                ],
                "eligibility": {
                    "min_age": 25,
                    "max_age": 100,
                    "vehicles": "2-4 vehicles",
                    "driving_history": "Acceptable record",
                    "credit_score": "Fair (600+)"
                },
                "best_for": [
                    "Multi-car households",
                    "Families with teen drivers",
                    "Those seeking bundling discounts",
                    "Households with diverse vehicle types"
                ],
                "deductible": "$500-$1,000 (flexible)"
            }
        ]
    },
    "home_insurance": {
        "category": "Home Insurance",
        "description": "Property and liability protection for homeowners",
        "products": [
            {
                "id": "home_basic",
                "name": "Basic Home Protection",
                "type": "HO-1 Basic Form",
                "monthly_premium_range": "$100 - $180",
                "coverage_amount": "Up to $250,000",
                "features": [
                    "Named perils coverage",
                    "Dwelling protection",
                    "Personal liability ($100,000)",
                    "Medical payments to others ($1,000)",
                    "Limited personal property coverage"
                ],
                "covered_perils": [
                    "Fire and smoke",
                    "Lightning",
                    "Windstorm and hail",
                    "Theft",
                    "Vandalism"
                ],
                "eligibility": {
                    "property_type": ["single-family", "condo"],
                    "property_age": "Any age",
                    "location": "Non-coastal areas preferred",
                    "home_value": "$50,000 - $250,000"
                },
                "best_for": [
                    "Older homes",
                    "Low-value properties",
                    "Budget-conscious homeowners",
                    "Minimal coverage needs"
                ],
                "deductible": "$2,500"
            },
            {
                "id": "home_premium",
                "name": "Premium Homeowner Coverage",
                "type": "HO-3 Special Form",
                "monthly_premium_range": "$250 - $450",
                "coverage_amount": "Up to $1,000,000",
                "features": [
                    "All-risk dwelling coverage",
                    "Replacement cost coverage",
                    "Personal liability ($500,000)",
                    "Medical payments ($5,000)",
                    "Extended replacement cost (125%)",
                    "Identity theft protection",
                    "Water backup coverage",
                    "Equipment breakdown coverage"
                ],
                "covered_perils": "All perils except specifically excluded",
                "eligibility": {
                    "property_type": ["single-family", "townhouse"],
                    "property_age": "Preferably <30 years",
                    "location": "All areas",
                    "home_value": "$250,000 - $1,000,000"
                },
                "best_for": [
                    "New or well-maintained homes",
                    "High-value properties",
                    "Those seeking comprehensive protection",
                    "Homeowners in high-risk areas"
                ],
                "deductible": "$1,000"
            },
            {
                "id": "home_luxury",
                "name": "Luxury Estate Protection",
                "type": "HO-5 Comprehensive",
                "monthly_premium_range": "$500 - $1,000+",
                "coverage_amount": "$1,000,000+",
                "features": [
                    "All-risk coverage for dwelling and contents",
                    "Guaranteed replacement cost",
                    "High-value personal property coverage",
                    "Personal liability ($1,000,000+)",
                    "Jewelry and art coverage",
                    "Home systems protection",
                    "Landscaping coverage",
                    "Green rebuild coverage",
                    "Cyber protection"
                ],
                "covered_perils": "Comprehensive - all-risk for dwelling and contents",
                "eligibility": {
                    "property_type": ["single-family", "estate"],
                    "property_age": "Any (with appraisal)",
                    "location": "All areas (coastal requires endorsement)",
                    "home_value": "$1,000,000+"
                },
                "best_for": [
                    "Luxury homes",
                    "High-net-worth individuals",
                    "Properties with expensive contents",
                    "Historic or custom homes"
                ],
                "deductible": "$2,500 - $5,000 (flexible)"
            }
        ]
    }
}

# Questionnaire templates for gathering customer requirements
QUESTIONNAIRES = {
    "health_insurance": {
        "questions": [
            {
                "id": "age",
                "question": "What is your age?",
                "type": "number",
                "required": True,
                "validation": {"min": 18, "max": 100}
            },
            {
                "id": "employment_status",
                "question": "What is your current employment status?",
                "type": "choice",
                "required": True,
                "options": ["employed", "self-employed", "unemployed", "retired"]
            },
            {
                "id": "family_size",
                "question": "How many family members would you like to cover (including yourself)?",
                "type": "number",
                "required": True,
                "validation": {"min": 1, "max": 10}
            },
            {
                "id": "pre_existing_conditions",
                "question": "Do you have any pre-existing medical conditions?",
                "type": "choice",
                "required": True,
                "options": ["yes", "no"]
            },
            {
                "id": "budget",
                "question": "What is your monthly budget for health insurance (in USD)?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 10000}
            },
            {
                "id": "coverage_preference",
                "question": "What's most important to you?",
                "type": "choice",
                "required": False,
                "options": ["low_cost", "comprehensive_coverage", "international_coverage", "family_benefits"]
            }
        ]
    },
    "life_insurance": {
        "questions": [
            {
                "id": "age",
                "question": "What is your age?",
                "type": "number",
                "required": True,
                "validation": {"min": 18, "max": 80}
            },
            {
                "id": "dependents",
                "question": "How many dependents do you have?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 10}
            },
            {
                "id": "annual_income",
                "question": "What is your annual income (in USD)?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 10000000}
            },
            {
                "id": "existing_coverage",
                "question": "Do you have any existing life insurance coverage?",
                "type": "choice",
                "required": True,
                "options": ["yes", "no"]
            },
            {
                "id": "health_status",
                "question": "How would you describe your current health?",
                "type": "choice",
                "required": True,
                "options": ["excellent", "good", "fair", "poor"]
            },
            {
                "id": "coverage_goal",
                "question": "What is your primary goal for life insurance?",
                "type": "choice",
                "required": False,
                "options": ["income_replacement", "debt_coverage", "estate_planning", "child_education"]
            }
        ]
    },
    "auto_insurance": {
        "questions": [
            {
                "id": "age",
                "question": "What is your age?",
                "type": "number",
                "required": True,
                "validation": {"min": 16, "max": 100}
            },
            {
                "id": "driving_experience",
                "question": "How many years of driving experience do you have?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 80}
            },
            {
                "id": "accidents_violations",
                "question": "Have you had any accidents or violations in the past 3 years?",
                "type": "choice",
                "required": True,
                "options": ["none", "1_violation", "2+_violations", "1_accident", "multiple_accidents"]
            },
            {
                "id": "vehicle_count",
                "question": "How many vehicles do you need to insure?",
                "type": "number",
                "required": True,
                "validation": {"min": 1, "max": 10}
            },
            {
                "id": "vehicle_age",
                "question": "What is the age of your primary vehicle?",
                "type": "choice",
                "required": True,
                "options": ["new_0-3_years", "recent_4-7_years", "older_8-10_years", "very_old_10+_years"]
            },
            {
                "id": "vehicle_value",
                "question": "What is the approximate value of your primary vehicle (in USD)?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 500000}
            },
            {
                "id": "coverage_need",
                "question": "What type of coverage are you looking for?",
                "type": "choice",
                "required": False,
                "options": ["minimum_liability", "full_coverage", "premium_protection"]
            }
        ]
    },
    "home_insurance": {
        "questions": [
            {
                "id": "property_type",
                "question": "What type of property do you own?",
                "type": "choice",
                "required": True,
                "options": ["single-family", "townhouse", "condo", "estate"]
            },
            {
                "id": "property_age",
                "question": "How old is your property (in years)?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 200}
            },
            {
                "id": "property_value",
                "question": "What is the estimated value of your property (in USD)?",
                "type": "number",
                "required": True,
                "validation": {"min": 0, "max": 50000000}
            },
            {
                "id": "location_risk",
                "question": "Is your property in a high-risk area (coastal, flood zone, earthquake zone)?",
                "type": "choice",
                "required": True,
                "options": ["yes", "no", "unsure"]
            },
            {
                "id": "mortgage",
                "question": "Do you have an active mortgage on the property?",
                "type": "choice",
                "required": True,
                "options": ["yes", "no"]
            },
            {
                "id": "contents_value",
                "question": "What is the approximate value of your personal belongings (in USD)?",
                "type": "number",
                "required": False,
                "validation": {"min": 0, "max": 5000000}
            }
        ]
    }
}
