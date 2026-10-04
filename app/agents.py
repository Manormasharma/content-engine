import os
from crewai import Agent
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

load_dotenv()

# Initialize search tool for live web retrieval
search_tool = TavilySearchTool()

class ContentAgents:
    def research_agent(self) -> Agent:
        return Agent(
            role="Senior Market Research Analyst",
            goal="Gather accurate, up-to-date, and comprehensive facts on the given topic from live web sources.",
            backstory="An elite fact-gatherer with an eye for high-credibility data, statistics, and trends.",
            tools=[search_tool],
            llm="gemini/gemini-3.5-flash-lite",
            verbose=True,
            memory=True
        )

    def critic_agent(self) -> Agent:
        return Agent(
            role="Editorial Quality Controller",
            goal="Critically review research data for logical gaps, shallow arguments, or missing context.",
            backstory="A strict senior editor who rejects unverified information and ensures complete accuracy.",
            llm="gemini/gemini-3.5-flash-lite",
            verbose=True
        )

    def writer_agent(self) -> Agent:
        return Agent(   
            role="Technical Content Writer",
            goal="Transform verified research into a compelling, structured, and ready-to-publish format.",
            backstory="An expert writer skilled at structuring complex research data into clean markdown or scripts.",
            llm="gemini/gemini-3.5-flash-lite",
            verbose=True
            
        )
    