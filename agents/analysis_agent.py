class FlightAnalysisAgent:
    """
    Agent that analyzes and ranks all flight options
    This is where the intelligence happens!
    """

    def __init__(self):
        # Mile valuations (cents per mile)
        self.mile_values = {
            "American Airlines": 1.2,  # 1.2 cents per AA mile
            "United": 1.3,
            "Delta": 1.2,
        }

    def analyze(self, all_results, search_request):
        """
        Analyze all results and provide recommendations
        """
        print(f"\n🧠 Analysis Agent: Analyzing {len(all_results)} options...")

        if not all_results:
            return {
                "summary": "No flights found",
                "best_cash": None,
                "best_miles": None,
                "all_options": []
            }

        # Separate cash and award flights
        cash_flights = [r for r in all_results if r.get('flight_type') != 'award']
        award_flights = [r for r in all_results if r.get('flight_type') == 'award']

        # Find best options
        best_cash = self._find_best_cash(cash_flights)
        best_award = self._find_best_award(award_flights)

        # Calculate value comparisons
        recommendations = self._generate_recommendations(best_cash, best_award)

        return {
            "summary": f"Found {len(cash_flights)} cash flights and {len(award_flights)} award flights",
            "best_cash_option": best_cash,
            "best_award_option": best_award,
            "recommendations": recommendations,
            "all_options": self._rank_all_options(all_results),
            "search_params": search_request
        }

    def _find_best_cash(self, flights):
        """Find cheapest cash option"""
        if not flights:
            return None

        best = min(flights, key=lambda x: x.get('price', float('inf')))
        print(f"💵 Best cash: {best.get('airline')} - ${best.get('price')}")
        return best

    def _find_best_award(self, flights):
        """Find best award option (lowest miles)"""
        if not flights:
            return None

        best = min(flights, key=lambda x: x.get('miles_cost', float('inf')))
        print(f"🎁 Best award: {best.get('airline')} - {best.get('miles_cost'):,} miles")
        return best

    def _generate_recommendations(self, best_cash, best_award):
        """Generate intelligent recommendations"""
        recommendations = []

        if best_cash and best_award:
            # Calculate value
            cash_price = best_cash.get('price', 0)
            miles_cost = best_award.get('miles_cost', 0)
            mile_value = self.mile_values.get(best_award.get('airline'), 1.2)

            miles_value_in_cash = (miles_cost * mile_value / 100)
            taxes = best_award.get('cash_cost', 0)
            total_award_cost = miles_value_in_cash + taxes

            savings = cash_price - total_award_cost

            if savings > 100:
                recommendations.append({
                    "type": "award_better",
                    "message": f"✨ Use miles! Save ~${savings:.2f}",
                    "details": f"Award flight costs {miles_cost:,} miles (≈${miles_value_in_cash:.2f}) + ${taxes:.2f} taxes vs ${cash_price} cash"
                })
            elif savings < -50:
                recommendations.append({
                    "type": "cash_better",
                    "message": f"💰 Pay cash! Better value than using miles",
                    "details": f"Cash ${cash_price} is better value than {miles_cost:,} miles"
                })
            else:
                recommendations.append({
                    "type": "similar",
                    "message": "🤷 Similar value - your preference",
                    "details": "Cash and miles options are roughly equivalent in value"
                })

        return recommendations

    def _rank_all_options(self, results):
        """Rank all options by value"""
        # Sort by price (cash) or miles cost (awards)
        sorted_results = sorted(results, key=lambda x: x.get('price') or x.get('miles_cost', float('inf')))
        return sorted_results[:10]  # Top 10