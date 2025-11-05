"""
Recommendation Service - AI-powered insurance product recommendation engine
Analyzes customer requirements and matches them with suitable products
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from data.product_catalog import PRODUCT_CATALOG, QUESTIONNAIRES

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    AI-powered recommendation engine that matches customer requirements
    to insurance products using rule-based scoring and ML-ready architecture
    """

    def __init__(self):
        self.catalog = PRODUCT_CATALOG
        self.questionnaires = QUESTIONNAIRES

    def get_questionnaire(self, insurance_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the questionnaire for a specific insurance type

        Args:
            insurance_type: Type of insurance (health_insurance, life_insurance, etc.)

        Returns:
            Questionnaire dict or None if not found
        """
        return self.questionnaires.get(insurance_type)

    def validate_answer(
        self, insurance_type: str, question_id: str, answer: Any
    ) -> tuple[bool, Optional[str]]:
        """
        Validate user's answer against question constraints

        Args:
            insurance_type: Type of insurance
            question_id: ID of the question
            answer: User's answer

        Returns:
            Tuple of (is_valid, error_message)
        """
        questionnaire = self.questionnaires.get(insurance_type)
        if not questionnaire:
            return False, "Invalid insurance type"

        question = next(
            (q for q in questionnaire["questions"] if q["id"] == question_id), None
        )
        if not question:
            return False, "Invalid question ID"

        if question["required"] and (answer is None or answer == ""):
            return False, f"{question['question']} is required"

        if question["type"] == "number" and "validation" in question:
            try:
                num_val = float(answer)
                val = question["validation"]
                if "min" in val and num_val < val["min"]:
                    return False, f"Value must be at least {val['min']}"
                if "max" in val and num_val > val["max"]:
                    return False, f"Value must be at most {val['max']}"
            except (ValueError, TypeError):
                return False, "Please provide a valid number"

        if question["type"] == "choice" and answer not in question.get("options", []):
            return False, f"Please choose from: {', '.join(question['options'])}"

        return True, None

    def recommend_products(
        self, insurance_type: str, user_requirements: Dict[str, Any], ai_provider=None
    ) -> List[Dict[str, Any]]:
        """
        Generate product recommendations based on user requirements

        Args:
            insurance_type: Type of insurance
            user_requirements: Dict of user answers to questionnaire
            ai_provider: Optional AI provider for advanced analysis

        Returns:
            List of recommended products with scores and reasons
        """
        if insurance_type not in self.catalog:
            return []

        products = self.catalog[insurance_type]["products"]
        recommendations = []

        for product in products:
            score, reasons = self._score_product(
                product, user_requirements, insurance_type
            )

            if score > 0:  # Only include products with positive scores
                recommendations.append(
                    {
                        "product": product,
                        "score": score,
                        "match_percentage": min(100, int(score)),
                        "reasons": reasons,
                        "category": insurance_type,
                    }
                )

        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x["score"], reverse=True)

        # Use AI for additional insights if available
        if ai_provider and recommendations:
            recommendations = self._enhance_with_ai(
                recommendations, user_requirements, ai_provider
            )

        return recommendations

    def _score_product(
        self, product: Dict[str, Any], requirements: Dict[str, Any], insurance_type: str
    ) -> tuple[float, List[str]]:
        """
        Score a product against user requirements

        Returns:
            Tuple of (score, list of matching reasons)
        """
        score = 0.0
        reasons = []

        # Type-specific scoring logic
        if insurance_type == "health_insurance":
            score, reasons = self._score_health_insurance(product, requirements)
        elif insurance_type == "life_insurance":
            score, reasons = self._score_life_insurance(product, requirements)
        elif insurance_type == "auto_insurance":
            score, reasons = self._score_auto_insurance(product, requirements)
        elif insurance_type == "home_insurance":
            score, reasons = self._score_home_insurance(product, requirements)

        return score, reasons

    def _score_health_insurance(
        self, product: Dict[str, Any], req: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Score health insurance products"""
        score = 0.0
        reasons = []

        # Age eligibility (critical - must match)
        age = req.get("age")
        if age:
            eligibility = product["eligibility"]
            if eligibility["min_age"] <= age <= eligibility["max_age"]:
                score += 20
                reasons.append("Meets age requirements")
            else:
                return 0, ["Age not within eligible range"]

        # Family size matching
        family_size = req.get("family_size", 1)
        if family_size == 1 and product["type"] == "Individual":
            score += 25
            reasons.append("Perfect for individual coverage")
        elif family_size > 1 and product["type"] == "Family":
            score += 30
            reasons.append(f"Designed for families of {family_size}")
            if "family_size" in product["eligibility"]:
                fam_elig = product["eligibility"]["family_size"]
                if fam_elig["min"] <= family_size <= fam_elig["max"]:
                    score += 10
                    reasons.append("Family size within plan limits")

        # Pre-existing conditions
        has_conditions = req.get("pre_existing_conditions") == "yes"
        if has_conditions:
            if (
                "Covered from day 1"
                in product["eligibility"]["pre_existing_conditions"]
            ):
                score += 25
                reasons.append("Immediate coverage for pre-existing conditions")
            elif (
                "Limited coverage" in product["eligibility"]["pre_existing_conditions"]
            ):
                score += 10
                reasons.append(
                    "Some coverage for pre-existing conditions after waiting period"
                )
        else:
            score += 10
            reasons.append("No pre-existing conditions concern")

        # Budget matching
        budget = req.get("budget")
        if budget:
            premium_range = product["monthly_premium_range"]
            min_premium = int(
                premium_range.split(" - ")[0].replace("$", "").replace(",", "")
            )
            max_premium = int(
                premium_range.split(" - ")[1].replace("$", "").replace(",", "")
            )

            if min_premium <= budget <= max_premium:
                score += 20
                reasons.append("Within your budget range")
            elif budget >= max_premium:
                score += 15
                reasons.append("Comfortably within budget")
            elif budget < min_premium:
                score -= 10
                reasons.append("May exceed your budget")

        # Employment status
        employment = req.get("employment_status")
        if employment in product["eligibility"]["employment_status"]:
            score += 10
            reasons.append("Employment status eligible")

        # Coverage preferences
        preference = req.get("coverage_preference")
        if preference == "low_cost" and "Basic" in product["name"]:
            score += 15
            reasons.append("Budget-friendly option as preferred")
        elif preference == "comprehensive_coverage" and "Premium" in product["name"]:
            score += 15
            reasons.append("Comprehensive coverage as desired")
        elif (
            preference == "international_coverage"
            and "International coverage" in product.get("features", [])
        ):
            score += 15
            reasons.append("Includes international coverage")
        elif preference == "family_benefits" and product["type"] == "Family":
            score += 15
            reasons.append("Family-focused benefits included")

        return score, reasons

    def _score_life_insurance(
        self, product: Dict[str, Any], req: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Score life insurance products"""
        score = 0.0
        reasons = []

        # Age eligibility
        age = req.get("age")
        if age:
            eligibility = product["eligibility"]
            if eligibility["min_age"] <= age <= eligibility["max_age"]:
                score += 20
                reasons.append("Age eligible for this plan")
            else:
                return 0, ["Age not within eligible range"]

        # Dependents
        dependents = req.get("dependents", 0)
        if dependents > 0:
            if "Family" in product["name"] or "dependents" in product["eligibility"]:
                score += 25
                reasons.append(f"Good coverage for {dependents} dependent(s)")
            if dependents >= 2 and "Child coverage" in str(product.get("features", [])):
                score += 10
                reasons.append("Includes child coverage riders")
        else:
            if product["type"] == "Term Life" and "Basic" in product["name"]:
                score += 20
                reasons.append("Simple coverage for individuals without dependents")

        # Income matching
        income = req.get("annual_income", 0)
        if income:
            income_req = product["eligibility"].get("income_requirement", "")
            if "Minimum" in income_req:
                min_income = int(
                    income_req.split("$")[1].replace(",", "").split("/")[0]
                )
                if income >= min_income:
                    score += 15
                    reasons.append("Meets income requirements")
                else:
                    score -= 20
                    reasons.append("Income below minimum requirement")

            # Coverage amount vs income rule of thumb (5-10x annual income)
            coverage_str = product["coverage_amount"].replace("$", "").replace(",", "")
            coverage = int(coverage_str) if coverage_str.isdigit() else 100000
            ideal_coverage = income * 7  # Middle of 5-10x range

            if coverage >= ideal_coverage * 0.7 and coverage <= ideal_coverage * 1.3:
                score += 20
                reasons.append("Coverage amount well-matched to income")

        # Health status
        health = req.get("health_status")
        health_req = product["eligibility"].get("health_status", "")
        if health == "excellent" or health == "good":
            score += 15
            reasons.append("Good health qualifies for best rates")
        elif health == "fair" and "Standard health" in health_req:
            score += 10
            reasons.append("Eligible with standard health requirements")
        elif health == "poor" and "Good health required" in health_req:
            score -= 15
            reasons.append("May require medical underwriting")

        # Existing coverage
        has_coverage = req.get("existing_coverage") == "yes"
        if has_coverage and product["type"] == "Whole Life":
            score += 10
            reasons.append(
                "Good supplement to existing coverage with investment component"
            )
        elif not has_coverage:
            score += 10
            reasons.append("Provides essential first-time coverage")

        # Coverage goals
        goal = req.get("coverage_goal")
        if goal == "income_replacement" and "Term Life" in product["type"]:
            score += 15
            reasons.append("Term life ideal for income replacement")
        elif goal == "estate_planning" and "Whole Life" in product["type"]:
            score += 15
            reasons.append("Whole life excellent for estate planning")
        elif goal == "debt_coverage" and "Basic" in product["name"]:
            score += 10
            reasons.append("Affordable coverage for debt protection")
        elif goal == "child_education" and "Family" in product["name"]:
            score += 15
            reasons.append("Family plan supports educational needs")

        return score, reasons

    def _score_auto_insurance(
        self, product: Dict[str, Any], req: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Score auto insurance products"""
        score = 0.0
        reasons = []

        # Age and experience
        age = req.get("age", 25)
        experience = req.get("driving_experience", 0)

        if age >= product["eligibility"]["min_age"]:
            score += 15
            reasons.append("Meets age requirement")
        else:
            return 0, ["Age below minimum requirement"]

        if age < 25 and "Family" in product["name"]:
            score += 10
            reasons.append("Family plan offers good coverage for young drivers")

        # Driving record
        violations = req.get("accidents_violations", "none")
        driving_history = product["eligibility"]["driving_history"]

        if violations == "none":
            score += 25
            reasons.append("Clean driving record qualifies for best rates")
            if "Clean record preferred" in driving_history:
                score += 10
        elif (
            violations in ["1_violation", "1_accident"]
            and "Acceptable record" in driving_history
        ):
            score += 15
            reasons.append("Driving history within acceptable range")
        elif "Some violations acceptable" in driving_history:
            score += 10
            reasons.append("Eligible despite driving history")

        # Vehicle count
        vehicle_count = req.get("vehicle_count", 1)
        if vehicle_count > 1 and "Multi-Vehicle" in product["type"]:
            score += 30
            reasons.append(f"Multi-vehicle discount for {vehicle_count} vehicles")
        elif vehicle_count == 1 and "Multi-Vehicle" not in product["type"]:
            score += 20
            reasons.append("Perfect for single vehicle coverage")

        # Vehicle age and value
        vehicle_age = req.get("vehicle_age", "new_0-3_years")
        vehicle_value = req.get("vehicle_value", 20000)

        if vehicle_age == "very_old_10+_years" or vehicle_value < 5000:
            if "Liability Only" in product["type"]:
                score += 25
                reasons.append(
                    "Liability-only coverage recommended for older/low-value vehicles"
                )
            else:
                score -= 10
                reasons.append(
                    "Full coverage may not be cost-effective for this vehicle"
                )
        elif vehicle_age == "new_0-3_years" or vehicle_value > 25000:
            if "Full Coverage" in product["type"]:
                score += 25
                reasons.append(
                    "Full coverage protects your valuable vehicle investment"
                )
            if "New car replacement" in product.get("features", []):
                score += 15
                reasons.append("New car replacement feature included")

        # Coverage preferences
        need = req.get("coverage_need")
        if need == "minimum_liability" and "Basic" in product["name"]:
            score += 20
            reasons.append("Meets minimum coverage requirement")
        elif need == "full_coverage" and "Full Coverage" in product["type"]:
            score += 20
            reasons.append("Comprehensive full coverage as requested")
        elif need == "premium_protection" and "Premium" in product["name"]:
            score += 20
            reasons.append("Premium protection with all features")

        return score, reasons

    def _score_home_insurance(
        self, product: Dict[str, Any], req: Dict[str, Any]
    ) -> tuple[float, List[str]]:
        """Score home insurance products"""
        score = 0.0
        reasons = []

        # Property type matching
        prop_type = req.get("property_type")
        if prop_type in product["eligibility"]["property_type"]:
            score += 20
            reasons.append(f"Covers {prop_type} properties")
        else:
            return 0, ["Property type not covered by this plan"]

        # Property value matching
        prop_value = req.get("property_value", 0)
        if prop_value:
            value_range = product["eligibility"]["home_value"]

            # Handle ranges like "$1,000,000+"
            if "+" in value_range:
                # Minimum value only, no upper limit
                min_val = int(
                    value_range.replace("$", "").replace(",", "").replace("+", "")
                )
                if prop_value >= min_val:
                    score += 25
                    reasons.append("Coverage adequate for your property value")
                else:
                    score -= 10
                    reasons.append("Property value below this plan's minimum")
            else:
                # Standard range with min and max
                min_val = int(
                    value_range.split(" - ")[0].replace("$", "").replace(",", "")
                )
                max_val_str = (
                    value_range.split(" - ")[1]
                    .replace("$", "")
                    .replace(",", "")
                    .replace("+", "")
                )

                if "+" in value_range.split(" - ")[1]:
                    # Has + at the end
                    if prop_value >= min_val:
                        score += 25
                        reasons.append("Coverage adequate for your property value")
                else:
                    max_val = int(max_val_str)
                    if min_val <= prop_value <= max_val:
                        score += 25
                        reasons.append("Perfect coverage range for your property value")
                    elif prop_value > max_val:
                        score -= 10
                        reasons.append(
                            "Property value exceeds this plan's coverage limit"
                        )
                    elif prop_value < min_val:
                        score -= 5
                        reasons.append("You may be over-insured with this plan")

        # Property age
        prop_age = req.get("property_age", 0)
        age_pref = product["eligibility"]["property_age"]

        if "Any" in age_pref:
            score += 10
            reasons.append("No age restrictions")
        elif "Preferably <30 years" in age_pref and prop_age < 30:
            score += 15
            reasons.append("Property age ideal for this coverage")
        elif prop_age > 50 and "Basic" in product["name"]:
            score += 10
            reasons.append("Suitable for older properties")

        # Location risk
        location_risk = req.get("location_risk", "no")
        if location_risk == "yes":
            if "Premium" in product["name"] or "Luxury" in product["name"]:
                score += 15
                reasons.append("Enhanced coverage for high-risk locations")
            else:
                score -= 10
                reasons.append("May require additional riders for high-risk area")
        else:
            score += 10
            reasons.append("Standard location risk")

        # Mortgage requirement
        has_mortgage = req.get("mortgage") == "yes"
        if has_mortgage:
            if "Replacement cost" in str(product.get("features", [])):
                score += 15
                reasons.append("Replacement cost coverage meets lender requirements")
            score += 10
            reasons.append("Adequate coverage for mortgaged property")

        # Contents value
        contents = req.get("contents_value", 0)
        if (
            contents > 100000
            and "high-value personal property"
            in str(product.get("features", [])).lower()
        ):
            score += 20
            reasons.append("High-value personal property coverage included")
        elif contents > 200000 and "Luxury" in product["name"]:
            score += 25
            reasons.append("Luxury plan best for valuable contents")

        # Coverage type preference
        if prop_value > 1000000 and "Luxury" in product["name"]:
            score += 20
            reasons.append("Luxury estate protection for high-value property")
        elif prop_value < 250000 and "Basic" in product["name"]:
            score += 15
            reasons.append("Cost-effective coverage for your property")

        return score, reasons

    def _enhance_with_ai(
        self,
        recommendations: List[Dict[str, Any]],
        requirements: Dict[str, Any],
        ai_provider,
    ) -> List[Dict[str, Any]]:
        """
        Use AI to add personalized insights to recommendations
        This is a placeholder for future AI enhancement
        """
        # TODO: Implement AI-based enhancement using the ai_provider
        # For now, just return the recommendations as-is
        return recommendations

    def generate_comparison(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a side-by-side comparison of recommended products

        Args:
            products: List of product dicts to compare

        Returns:
            Comparison table structure
        """
        if not products:
            return {}

        comparison = {"products": [], "features": []}

        # Extract all unique features
        all_features = set()
        for prod in products:
            product_data = prod.get("product", prod)
            if "features" in product_data:
                all_features.update(product_data["features"])

        comparison["features"] = sorted(list(all_features))

        # Build comparison matrix
        for prod in products:
            product_data = prod.get("product", prod)
            prod_comparison = {
                "name": product_data["name"],
                "type": product_data["type"],
                "premium": product_data["monthly_premium_range"],
                "coverage": product_data.get("coverage_amount", "N/A"),
                "score": prod.get("match_percentage", "N/A"),
                "features": {},
            }

            # Mark which features this product has
            product_features = product_data.get("features", [])
            for feature in comparison["features"]:
                prod_comparison["features"][feature] = feature in product_features

            comparison["products"].append(prod_comparison)

        return comparison


# Global instance
recommendation_engine = RecommendationEngine()


def get_recommendation_engine() -> RecommendationEngine:
    """Get the global recommendation engine instance"""
    return recommendation_engine
