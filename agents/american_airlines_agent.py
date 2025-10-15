from .base_agent import FlightAgent
import random


class AmericanAirlinesAwardAgent(FlightAgent):
    """
    Agent for American Airlines award search
    (Mock for now - replace with real API when you reverse engineer it)
    """

    def __init__(self):
        self.name = "American Airlines Award Search"
        print(f"🛫 Initialized {self.name}")

    def search(self, search_request):
        """Search for AA award availability"""
        print(f"🔍 {self.name}: Searching award flights...")

        # Simulate API call delay
        import time
        time.sleep(1)

        # Mock award data (replace with real AA API)
        return self._get_mock_award_data(search_request)

    def _get_mock_award_data(self, search_request):
        """Mock award availability data"""
        awards = [
            {
                "airline": "American Airlines",
                "flight_type": "award",
                "miles_cost": 60000,
                "cash_cost": 45.60,  # Taxes/fees
                "cabin": "Economy",
                "departure_time": "10:30 AM",
                "arrival_time": "2:45 PM",
                "duration": "14h 15m",
                "stops": 1,
                "availability": "Good",
                "route": f"{search_request['departure_id']} → {search_request['arrival_id']}",
                "raw_data": {"mock": True, "award": True}
            },
            {
                "airline": "American Airlines",
                "flight_type": "award",
                "miles_cost": 110000,
                "cash_cost": 85.40,
                "cabin": "Business",
                "departure_time": "11:00 AM",
                "arrival_time": "3:30 PM",
                "duration": "14h 30m",
                "stops": 1,
                "availability": "Limited",
                "route": f"{search_request['departure_id']} → {search_request['arrival_id']}",
                "raw_data": {"mock": True, "award": True}
            }
        ]

        return awards
