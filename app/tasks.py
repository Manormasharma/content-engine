from crewai import Task, Crew, Process
from app.agents import ContentAgents

def run_content_pipeline(topic: str, output_format: str) -> str:
    agents = ContentAgents()
    
    # Grab our 3 actors
    researcher = agents.research_agent()
    critic = agents.critic_agent()
    writer = agents.writer_agent()

    # TASK 1: The Researcher's job
    t_research = Task(
        description=f"Conduct thorough online research regarding: {topic}.",
        expected_output="A comprehensive bullet-point research brief with sources and data points.",
        agent=researcher
    )

    # TASK 2: The Critic's job (Notice it looks at what the Researcher produced)
    t_critique = Task(
        description="Review the research brief for factual strength, gaps, or logic flaws. Provide a finalized, validated summary.",
        expected_output="A validated and approved research document ready for synthesis.",
        agent=critic
    )

    # TASK 3: The Writer's job (Turns the approved notes into your final format)
    t_write = Task(
        description=(
            f"Using the verified research, write a polished piece formatted specifically as a {output_format}. "
            "If the format is a LinkedIn Post: "
            "1. Keep it concise, professional, and engaging (under 1300 characters). "
            "2. Use a strong hook in the first sentence with relevant emojis. "
            "3. End with 3-4 targeted hashtags and a call-to-action. "
            "4. At the very end, provide an explicit 'IMAGE_PROMPT: [A detailed description for an accompanying high-converting graphic]'."
        ),
        expected_output="A professional LinkedIn post layout paired with a creative image prompt.",
        agent=writer
    )

    # THE CREW: This bundles them together into a sequential conveyor belt
    crew = Crew(
        agents=[researcher, critic, writer],
        tasks=[t_research, t_critique, t_write],
        process=Process.sequential, # Means Step 1 finishes before Step 2 starts, and Step 2 before Step 3
        verbose=True
    )

    # Kickoff triggers the whole chain reaction and returns the final text
    result = crew.kickoff(inputs={"topic": topic, "output_format": output_format})
    return str(result)