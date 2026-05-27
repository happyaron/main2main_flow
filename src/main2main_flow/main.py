#!/usr/bin/env python
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, router, or_

from main2main_flow.crews.content_crew.content_crew import ContentCrew
from main2main_flow.utils import UpgradeCompleted, StepCompleted, UpgradeFailed, StepRetryNeeded

class ContentState(BaseModel):
    topic: str = ""
    outline: str = ""
    draft: str = ""
    final_post: str = ""


class ContentFlow(Flow[ContentState]):

    @start()
    def initialize(self):
        self.max_step = 0
        self.current_step=0
        self.retry_count=0

    @listen(initialize)
    def analyze_commit_and_plan_step(self):
        # 笑爽
        print("analyze_commit_and_plan_step")
        self.max_step = 10
        return "Analysize"

    @listen(or_(analyze_commit_and_plan_step, StepCompleted, StepRetryNeeded))
    def ai_analysis(self):
        # 逢春
        # Call Agent
        print("commit_adapt")
        return "ADAPT_OK"

    @router(ai_analysis)
    def run_e2e_test(self) -> Literal["StepCompleted", "UpgradeCompleted", "UpgradeFailed", "StepRetryNeeded"]:
        # run e2e test 卫军
        print("run_e2e_test")
        test_reslut = True
        if test_reslut:
            self.current_step+=1
            if self.current_step>=self.max_step:
                return UpgradeCompleted
            else:
                return StepCompleted
        else:
            self.retry_count+=1
            if self.retry_count>=3:
                self.retry_count=0
                return UpgradeFailed
            else:
                return StepRetryNeeded

    @listen(or_(UpgradeCompleted, UpgradeFailed))
    def generate_final_post(self):
        # 佳伟
        # create final post from draft
        return "FinalPost"

    @listen(generate_final_post)
    def push_to_github(self):
        # 佳伟
        #if xxx:
        # push final post to github
        return "PushToGithub"

def kickoff():
    content_flow = ContentFlow()
    content_flow.kickoff()


def plot():
    content_flow = ContentFlow()
    content_flow.plot()


def run_with_trigger():
    """
    Run the flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    # The @start() methods will automatically receive crewai_trigger_payload parameter
    content_flow = ContentFlow()

    try:
        result = content_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


if __name__ == "__main__":
    kickoff()
