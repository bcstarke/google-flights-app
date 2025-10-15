class FlightAgent:
    """Base class for all flight search agents"""

    def search(self, search_request):
        """
        Search for flights
        Args:
            search_request: dict with origin, destination, date
        Returns:
            list of flight results
        """
        raise NotImplementedError("Each agent must implement search()")

    def format_result(self, raw_data):
        """Convert raw API response to standard format"""
        return {
            "airline": "Unknown",
            "price": 0,
            "departure_time": "Unknown",
            "arrival_time": "Unknown",
            "duration": "Unknown",
            "stops": 0,
            "raw_data": raw_data
        }
