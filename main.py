import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from textwrap import dedent

load_dotenv()

# 1. Setup Environment and LLM
gemini_flash = LLM(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Define Specialized Agents
researcher = Agent(
    role='Senior Financial Researcher',
    goal='Uncover deep insights into {company} and its 2025 market outlook.',
    backstory=dedent("""You are a world-class financial analyst. You specialize in 
    identifying emerging market trends for {company}."""),
    llm=gemini_flash,
    verbose=True
)

writer = Agent(
    role='Technical Financial Writer',
    goal='Synthesize research findings into a clear, investor-ready report.',
    backstory=dedent("""You are a seasoned business journalist. You transform raw 
    financial data into compelling, structured narratives for executive stakeholders."""),
    llm=gemini_flash,
    verbose=True
)

# 3. Define the Workflow Tasks
research_task = Task(
    description=dedent("""Research current financial trends for {company}. 
    Identify three key growth drivers and three potential risks."""),
    expected_output="A structured report for {company} including growth drivers and risks.",
    agent=researcher
)

writing_task = Task(
    description=dedent("""Using the research findings, write a high-level 3-paragraph 
    investment summary. Focus on the core recommendation (Buy/Hold/Sell)."""),
    expected_output="A polished 3-paragraph financial report in Markdown format.",
    agent=writer
)

# 4. Form and Kickoff the Crew
fin_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential, # Researcher must finish before Writer starts
    verbose=True
)

if __name__ == "__main__":
    print("\n--- Starting Autonomous Financial Research ---")
    result = fin_crew.kickoff(inputs={'company': 'NVIDIA'})
    print("\n--- FINAL FINANCIAL REPORT ---\n")
    print(result)