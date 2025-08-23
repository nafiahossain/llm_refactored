import logging
import sys

from agent.agent import Agent

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    """Main entry point for the agent application"""
    if len(sys.argv) < 2:
        print('Usage: python main.py "your question here"')
        print("\nExample queries:")
        print('  python main.py "What is 12.5% of 243?"')
        print('  python main.py "What\'s the weather in Paris?"')
        print('  python main.py "Who is Ada Lovelace?"')
        print('  python main.py "Translate hello to Spanish"')
        print(
            '  python main.py "Add 10 to the average temperature in Paris and London"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    agent = Agent(use_fake_llm=True)

    try:
        result = agent.answer(query)
        print(result)
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
