import os
from .base_agent import FlightAgent
from serpapi import GoogleSearch


class GoogleFlightsAgent(FlightAgent):
    """Agent for Google Flights via SerpAPI"""

    def __init__(self):
        # Get API key from environment variable or replace with your key
        self.api_key = os.getenv('SERPAPI_KEY')

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
                'api_key': self.api_key,
                'travel_class': '3',
                'deep_search': 'true'
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
        all_flights = []

        # Collect flights from all available sections
        for key in ['best_flights', 'other_flights', 'flights']:
            if key in data and data[key]:
                all_flights.extend(data[key])
                print(f"Found {len(data[key])} flights in '{key}'")

        if not all_flights:
            print(f"No flights found. Available keys: {list(data.keys())}")
            return []

        print(f"📊 Total flights to parse: {len(all_flights)}")

        for flight in all_flights:  # Parse ALL flights - no limit
            try:
                price = flight.get('price', 0)

                # Parse departure/arrival info
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
                    "flight_type": "business",
                    "cabin_class": "Business",
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