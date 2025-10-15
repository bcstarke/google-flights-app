# app.py
from flask import Flask, request, jsonify
from controller import FlightController

app = Flask(__name__)


@app.route('/')
def home():
    return """
    <h1>Flight Search API</h1>
    <p>GET to /search with:</p>
    <pre>
    {
        "origin": "NYC",
        "destination": "TYO", 
        "outbound_date": "2026-07-15",
        "return_date": "2026-07-25"
    }
    </pre>
    """


@app.route('/search', methods=['POST'])
def search():
    try:
        # Get user input
        data = request.json
        origin = data.get('origin')
        destination = data.get('destination')
        outbound_date = data.get('outbound_date')
        return_date = data.get('return_date')

        # Basic validation
        if not all([origin, destination, outbound_date, return_date]):
            return jsonify({"error": "Missing required fields: origin, destination, date"}), 400

        # Create search request
        search_request = {
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": outbound_date,
            "return_date": return_date
        }

        # Use controller to search
        controller = FlightController()
        results = controller.search(search_request)

        return jsonify({
            "success": True,
            "search": search_request,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)