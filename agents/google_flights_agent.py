import os
from .base_agent import FlightAgent
from serpapi import GoogleSearch


class GoogleFlightsAgent(FlightAgent):
    """Agent for Google Flights via SerpAPI"""

    def __init__(self):
        # Get API key from environment variable or replace with your key
        self.api_key = os.getenv('SERPAPI_KEY', '06dc4ca12dc4a975d2a9e19b1183cc3045b8b51db5b650186b0ef617c28a6360')

        # Debug: print API key status
        if self.api_key and self.api_key != 'your_serpapi_key_here':
            print(f"✓ SerpAPI key loaded: {self.api_key[:10]}...")
        else:
            print("✗ No SerpAPI key found - will use mock data")

    def search(self, search_request):
        """Search Google Flights"""

        # Check if we have a real API key
        if not self.api_key or self.api_key == "your_serpapi_key_here":
            print("❌ No valid SerpAPI key - using mock data")
            return self._get_mock_data(search_request)

        try:
            print(f"🔍 Searching Google Flights: {search_request['departure_id']} → {search_request['arrival_id']}")

            params = {
                'engine': 'google_flights',
                'departure_id': search_request['departure_id'],
                'arrival_id': search_request['arrival_id'],
                'outbound_date': search_request['outbound_date'],
                'return_date': search_request.get('return_date'),  # Optional
                'currency': 'USD',
                'hl': 'en',
                'gl': 'us',
                'api_key': self.api_key
            }

            print(f"📡 Making SerpAPI request...")
            search = GoogleSearch(params)
            data = search.get_dict()  # Changed from get_json()

            print(f"📊 SerpAPI response received")
            print(f"📋 Response keys: {list(data.keys())}")

            # Check for API errors
            if 'error' in data:
                print(f"❌ SerpAPI error: {data['error']}")
                return self._get_mock_data(search_request)

            results = self._parse_google_results(data)
            print(f"✅ Parsed {len(results)} real flights")
            return results

        except Exception as e:
            print(f"❌ Google Flights agent error: {e}")
            import traceback
            traceback.print_exc()
            return self._get_mock_data(search_request)

    def _parse_google_results(self, data):
        """Parse Google Flights API response"""
        results = []

        # Try different possible response structures
        flights_data = []

        if 'best_flights' in data:
            flights_data = data['best_flights']
            print(f"Found {len(flights_data)} best flights")
        elif 'other_flights' in data:
            flights_data = data['other_flights']
            print(f"Found {len(flights_data)} other flights")
        elif 'flights' in data:
            flights_data = data['flights']
            print(f"Found {len(flights_data)} flights")
        else:
            print(f"No flights found. Available keys: {list(data.keys())}")
            return []

        for flight in flights_data[:10]:  # Take first 10 results
            try:
                # Parse flight data - structure may vary
                price = 0
                if 'price' in flight:
                    price = flight['price']
                elif 'total_price' in flight:
                    price = flight['total_price']

                # Get departure/arrival info
                departure_time = "Unknown"
                arrival_time = "Unknown"

                if 'flights' in flight and flight['flights']:
                    first_segment = flight['flights'][0]
                    departure_time = first_segment.get('departure_airport', {}).get('time', 'Unknown')

                    last_segment = flight['flights'][-1]
                    arrival_time = last_segment.get('arrival_airport', {}).get('time', 'Unknown')

                # Count layovers
                stops = 0
                if 'layovers' in flight:
                    stops = len(flight['layovers'])
                elif 'flights' in flight:
                    stops = len(flight['flights']) - 1

                result = {
                    "airline": flight.get('airline', 'Multiple Airlines'),
                    "price": price,
                    "flight_type": "cash",  # Added for analysis agent
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                    "duration": flight.get('total_duration', 'Unknown'),
                    "stops": stops,
                    "booking_link": flight.get('booking_options', [{}])[0].get('link', '') if flight.get(
                        'booking_options') else '',
                    "raw_data": flight
                }
                results.append(result)

            except Exception as e:
                print(f"Error parsing flight: {e}")
                continue

        return results

    def _get_mock_data(self, search_request):
        """Return mock data for testing"""
        return [
            {
                "airline": "American Airlines",
                "price": 450,
                "flight_type": "cash",
                "departure_time": "08:00 AM",
                "arrival_time": "11:30 AM",
                "duration": "5h 30m",
                "stops": 0,
                "route": f"{search_request['departure_id']} → {search_request['arrival_id']}",
                "outbound_date": search_request['outbound_date'],  # Changed from 'date'
                "raw_data": {"mock": True}
            },
            {
                "airline": "Delta",
                "price": 520,
                "flight_type": "cash",
                "departure_time": "02:15 PM",
                "arrival_time": "06:45 PM",
                "duration": "6h 30m",
                "stops": 1,
                "route": f"{search_request['departure_id']} → {search_request['arrival_id']}",
                "outbound_date": search_request['outbound_date'],  # Changed from 'date'
                "raw_data": {"mock": True}
            }
        ]