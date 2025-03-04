from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool,ScrapeWebsiteTool,FileReadTool,FileWriterTool,DirectoryReadTool
from .tools.merge_files_tool import MergeFilesTool


@CrewBase
class MultiCrewAgent():

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
		file_path='./result/*'
	)

	search_result_file_path:str = './search/'
	output_result_file_path:str = './result/'

	merge_files_tool = MergeFilesTool()

    # ChatGPTを使ってウェブサイトを検索
	@agent
	def researcher_chatgpt(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_chatgpt'],
			tools=[self.search_tool],
			llm="gemini/gemini-2.0-flash",
			verbose=True
		)
	# Claudeを使ってウェブサイトを検索
	@agent
	def researcher_claude(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_claude'],
			tools=[self.search_tool],
			llm="gpt-4o-mini",
			verbose=True
		)
	# Geminiを使ってウェブサイトを検索
	@agent
	def researcher_gemini(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher_gemini'],
			tools=[self.search_tool],
			llm="gpt-4o-mini",
			verbose=True
		)

	# ファイルをマージする
	@agent
	def files_merger(self) -> Agent:
		return Agent(
			config=self.agents_config['files_merger'],
			tools=[self.merge_files_tool],
			llm="gpt-4o",
			verbose=True
		)
	# ビジネス分析を行う
	@agent
	def business_analysis(self) -> Agent:
		return Agent(
			config=self.agents_config['business_analysis'],
			tools=[self.file_read_tool,ScrapeWebsiteTool()],
			llm="o1-mini",
			verbose=True
		)
	# ITコンサルタントのエージェント
	@agent
	def it_consultant(self) -> Agent:
		return Agent(
			config=self.agents_config['it_consultant'],
			tools=[self.file_read_tool],
			llm="anthropic/claude-3-7-sonnet-20250219",
			verbose=True
		)

	# ChatGPTによる調査タスク
	@task
	def research_chatgpt_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_chatgpt_task'],
			output_file=f'{self.search_result_file_path}research_report_chatgpt.md'
		)

	# Claudeによる調査タスク
	@task
	def research_claude_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_claude_task'],
			output_file=f'{self.search_result_file_path}research_report_claude.md'
	)

	# Geminiによる調査タスク
	@task
	def research_gemini_task(self) -> Task:
		return Task(
			config=self.tasks_config['researcher_gemini_task'],
			output_file=f'{self.search_result_file_path}research_report_gemini.md'
	)

	# ファイルマージタスク
	@task
	def files_merger_task(self) -> Task:
		return Task(
			config=self.tasks_config['files_merger_task'],
			output_file=f'{self.output_result_file_path}llm_return.md'
	)

	# ビジネス分析タスク
	@task
	def business_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['business_analysis_task'],
	)

	# ITコンサルタントによる提案タスク
	@task
	def it_consultant_task(self) -> Task:
		return Task(
			config=self.tasks_config['it_consultant_task'],
			output_file=f'{self.output_result_file_path}analyze_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Crew メソットを設定する"""

		return Crew(
			agents=self.agents, # @agentデコレータによって自動的に作成される
			tasks=self.tasks, # @taskデコレータによって自動的に作成される
			process=Process.sequential,
			verbose=True,
            output_log_file="./logs/log" # ログファイルの出力先を指定する
		)

