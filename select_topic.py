#!/usr/bin/env python
"""
Research Topic Selector - Choose debate topic from library
Displays available research topics with descriptions and suggested papers
"""

import json
import os

def load_topics():
    """Load research topics from JSON file."""
    topics_file = os.path.join(os.path.dirname(__file__), "research_topics.json")
    if not os.path.exists(topics_file):
        print(f"Error: {topics_file} not found")
        return None
    
    with open(topics_file, "r", encoding="utf-8") as f:
        return json.load(f)

def display_topics(topics_data):
    """Display available research topics."""
    if not topics_data or "topics" not in topics_data:
        print("No topics available")
        return None
    
    topics = topics_data["topics"]
    
    print("\n" + "=" * 80)
    print("RESEARCH TOPICS FOR ACADEMIC DEBATE")
    print("=" * 80)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}] {topic['title']}")
        print(f"    Field: {topic['field']}")
        print(f"    Description: {topic['description']}")
        print(f"    Key Concepts: {', '.join(topic['key_concepts'][:3])}...")
        print(f"    Key Papers: {', '.join(topic['foundational_papers'][:2])}...")
    
    return topics

def get_topic_selection(topics):
    """Get user's topic selection."""
    while True:
        try:
            choice = input(f"\nSelect topic (1-{len(topics)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(topics):
                return topics[idx]
            else:
                print(f"Please enter a number between 1 and {len(topics)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def display_topic_details(topic):
    """Display detailed information about selected topic."""
    print("\n" + "=" * 80)
    print("SELECTED TOPIC DETAILS")
    print("=" * 80)
    
    print(f"\nTitle: {topic['title']}")
    print(f"Field: {topic['field']}")
    print(f"Description: {topic['description']}")
    
    print("\n📚 KEY CONCEPTS:")
    for concept in topic['key_concepts']:
        print(f"  • {concept}")
    
    print("\n📖 FOUNDATIONAL PAPERS:")
    for paper in topic['foundational_papers']:
        print(f"  • {paper}")
    
    print("\n🔍 RESEARCH GAPS TO EXPLORE:")
    for gap in topic['research_gaps']:
        print(f"  • {gap}")
    
    return {
        "topic": topic['title'],
        "field": topic['field']
    }

def main():
    """Main function."""
    print("\n🎓 Academic Debate Arena - Topic Selector")
    print("Select a research topic for rigorous academic debate\n")
    
    # Load topics
    topics_data = load_topics()
    if not topics_data:
        return None
    
    # Display and select
    topics = display_topics(topics_data)
    if not topics:
        return None
    
    selected = get_topic_selection(topics)
    debate_config = display_topic_details(selected)
    
    print("\n" + "=" * 80)
    print("✅ Ready to start debate!")
    print("=" * 80)
    print(f"\nTopic: {debate_config['topic']}")
    print(f"Field: {debate_config['field']}")
    print("\nYou can now run:")
    print(f'  python main.py')
    print(f"  (System will use this topic configuration)")
    
    return debate_config

if __name__ == "__main__":
    config = main()
    if config:
        # Could save to a temp config file or use as input to main.py
        print("\n" + "=" * 80)
