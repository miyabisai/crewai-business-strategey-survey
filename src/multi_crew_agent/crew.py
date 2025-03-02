from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool,ScrapeWebsiteTool,FileReadTool,FileWriterTool,DirectoryReadTool
from .tools.merge_files_tool import MergeFilesTool


@CrewBase
class MultiCrewAgent():
	"""MultiCrewAgent crew"""

	#config file
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	#tool
	search_tool = SerperDevTool(
   		n_results=10,
		country="jp",
    	locale="jp",
    	location="Japan",
	)

	file_read_tool = FileReadTool(
		file_path='./result/result.md'
	)

	search_result_file_path:str = './search/'
	output_result_file_path:str = './result/'

	merge_files_tool = MergeFilesTool()

    #Search website with chatgpt
	@agent
	def researcher_chatgpt(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_chatgpt'],
			tools=[self.search_tool],
			llm="gpt-4o-mini",
			verbose=True
		)
	#Search website with claude
	@agent
	def researcher_claude(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_claude'],
			tools=[self.search_tool],
			llm="gpt-4o-mini",
			verbose=True
		)
	#Search website with gemini
	@agent
	def researcher_gemini(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_gemini'],
			tools=[self.search_tool],
			llm="gpt-4o-mini",
			verbose=True
		)

	#Merge files
	@agent
	def files_merger(self) -> Agent:
		return Agent(
			config=self.agents_config['files_merger'], 
			tools=[self.merge_files_tool], 
			llm="gpt-4o", 
			verbose=True
		)
	#Analyze business
	@agent
	def business_analysis(self) -> Agent:
		return Agent(
			config=self.agents_config['business_analysis'],
			tools=[self.file_read_tool,ScrapeWebsiteTool()],
			llm="gpt-4o",
			verbose=True
		)
	
	@task
	def research_chatgpt_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_chatgpt_task'],
			output_file=f'{self.search_result_file_path}research_report_chatgpt.md'
		)
	
	@task
	def research_claude_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_claude_task'],
			output_file=f'{self.search_result_file_path}research_report_claude.md'
	)

	@task
	def research_gemini_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_gemini_task'],
			output_file=f'{self.search_result_file_path}research_report_gemini.md'
	)

	@task
	def files_merger_task(self) -> Task:
		return Task(
			config=self.tasks_config['files_merger_task'],
			output_file=f'{self.output_result_file_path}llm_return.md'
	)

	@task
	def business_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['business_analysis_task'],
			output_file='./result/analyze_report.md'
	)

	@crew
	def crew(self) -> Crew:
		"""Creates the MultiCrewAgent crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)


