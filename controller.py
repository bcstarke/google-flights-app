from agents.google_flights_agent import GoogleFlightsAgent
from agents.american_airlines_agent import AmericanAirlinesAwardAgent
from agents.analysis_agent import FlightAnalysisAgent
import concurrent.futures
import time


class FlightController:
    def __init__(self):
        # Multiple specialized agents
        self.search_agents = [
            GoogleFlightsAgent(),
            AmericanAirlinesAwardAgent(),
        ]

        # Analysis agent to compare results
        self.analysis_agent = FlightAnalysisAgent()

    def search(self, search_request):
        """
        Orchestrates search across all agents in parallel
        """
        print(f"\n{'=' * 60}")
        print(f"🎯 Flight Search: {search_request['departure_id']} → {search_request['arrival_id']}")
        print(f"📅 Dates: {search_request['outbound_date']} - {search_request['return_date']}")
        print(f"{'=' * 60}\n")

        start_time = time.time()
        all_results = []

        # Run agents in parallel for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.search_agents)) as executor:
            # Submit all agent searches
            future_to_agent = {
                executor.submit(self._run_agent, agent, search_request): agent
                for agent in self.search_agents
            }

            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    agent_results = future.result()

                    # Tag results with agent name
                    for result in agent_results:
                        result['source_agent'] = agent.__class__.__name__
                        result['search_time'] = time.time() - start_time

                    all_results.extend(agent_results)
                    print(f"✅ {agent.__class__.__name__}: {len(agent_results)} results")

                except Exception as e:
                    print(f"❌ {agent.__class__.__name__} failed: {e}")

        # Use analysis agent to rank and compare results
        analyzed_results = self.analysis_agent.analyze(all_results, search_request)

        total_time = time.time() - start_time
        print(f"\n⏱️  Total search time: {total_time:.2f}s")
        print(f"📊 Total results: {len(all_results)}")
        print(f"{'=' * 60}\n")

        return analyzed_results

    def _run_agent(self, agent, search_request):
        """Run a single agent and handle errors"""
        try:
            return agent.search(search_request)
        except Exception as e:
            print(f"Error in {agent.__class__.__name__}: {e}")
            return []