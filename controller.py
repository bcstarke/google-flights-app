from agents.google_flights_agent import GoogleFlightsAgent


class FlightController:
    def __init__(self):
        # Start with just one agent
        self.agents = [
            GoogleFlightsAgent()
        ]

    def search(self, search_request):
        """
        Orchestrates search across all agents
        """
        all_results = []

        for agent in self.agents:
            try:
                print(f"Searching with {agent.__class__.__name__}...")
                agent_results = agent.search(search_request)

                # Add agent info to each result
                for result in agent_results:
                    result['agent'] = agent.__class__.__name__

                all_results.extend(agent_results)
                print(f"Got {len(agent_results)} results from {agent.__class__.__name__}")

            except Exception as e:
                print(f"Error with {agent.__class__.__name__}: {e}")
                # Continue with other agents
                continue

        return all_results
