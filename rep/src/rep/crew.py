from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
from dotenv import load_dotenv
from crewai_tools import CodeInterpreterTool
load_dotenv()

code_interpreter = CodeInterpreterTool()

@CrewBase
class Rep:
    """Replicate crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def project_thinker(self) -> Agent:
        return Agent(
            config=self.agents_config['project_thinker'],
            verbose=True,
            memoryview=True
        )

    @agent
    def project_architecture(self) -> Agent:
        return Agent(
            config=self.agents_config['project_architecture'],
            verbose=True,
            memoryview=True
        )

    @agent
    def code_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_developer'],
            verbose=True,
            memoryview=True
        )
    @agent
    def animator(self) -> Agent:
        return Agent(
            config=self.agents_config['animator'],
            verbose=True,
            memoryview=True
        )
    @agent
    def background_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['background_editor'],
            verbose=True,
            memoryview=True
        )
    @agent
    def code_improver(self) -> Agent:
        return Agent(
            config=self.agents_config['code_improver'],
            verbose=True
        )

    @agent
    def command_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['command_writer'],
            verbose=True,
            tools=[code_interpreter]
        )

    @task
    def project_thinker_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_thinker_task'],
            memoryview=True
        )

    @task
    def project_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_architecture_task'],
            output_file='report.md',
            memoryview=True
        )

    @task
    def code_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_developer_task'],
            output_file='report2.json',
            memoryview=True
        )
    @task
    def animator_task(self) -> Task:
        return Task(
            config=self.tasks_config['animator_task'],
            output_file='report3.md',
            memoryview=True
        )
    @task
    def background_editor_task(self) -> Task:
        return Task(
            config=self.tasks_config['animator_task'],
            output_file='report4.md',
            memoryview=True
        )
    @task
    def code_improver_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_improver_task'],
            output_file='report3.json',
            memoryview=True
        )

    @task
    def command_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['command_writer_task'],
            output_file='report5.md',
            memoryview=True
        )

    

    @crew
    def crew(self) -> Crew:
        """Creates the Replicate crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
































# @CrewBase
# class Rep():
#     """Rep crew"""

#     # Learn more about YAML configuration files here:
#     # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
#     # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
#     agents_config = 'config/agents.yaml'
#     tasks_config = 'config/tasks.yaml'

#     # If you would like to add tools to your agents, you can learn more about it here:
#     # https://docs.crewai.com/concepts/agents#agent-tools
#     @agent
#     def researcher(self) -> Agent:
#         return Agent(
#             config=self.agents_config['researcher'],
#             verbose=True
#         )

#     @agent
#     def reporting_analyst(self) -> Agent:
#         return Agent(
#             config=self.agents_config['reporting_analyst'],
#             verbose=True
#         )

#     # To learn more about structured task outputs,
#     # task dependencies, and task callbacks, check out the documentation:
#     # https://docs.crewai.com/concepts/tasks#overview-of-a-task
#     @task
#     def research_task(self) -> Task:
#         return Task(
#             config=self.tasks_config['research_task'],
#         )

#     @task
#     def reporting_task(self) -> Task:
#         return Task(
#             config=self.tasks_config['reporting_task'],
#             output_file='report.md'
#         )

#     @crew
#     def crew(self) -> Crew:
#         """Creates the Rep crew"""
#         # To learn how to add knowledge sources to your crew, check out the documentation:
#         # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

#         return Crew(
#             agents=self.agents, # Automatically created by the @agent decorator
#             tasks=self.tasks, # Automatically created by the @task decorator
#             process=Process.sequential,
#             verbose=True,
#             # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
#         )
