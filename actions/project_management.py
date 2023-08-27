#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:12 - August 27, 2023 rewrite by -EG
@Author  : alexanderwu
@File    : project_management.py
"""
from typing import List, Tuple

from metagpt.actions.action import Action
from metagpt.const import WORKSPACE_ROOT
from metagpt.utils.common import CodeParser
from pathlib import Path

PROMPT_TEMPLATE = Path( __file__ ).parent.joinpath( 'golden_project_management_prompt.md' ).read_text()
FORMAT_EXAMPLE = Path( __file__ ).parent.joinpath( 'golden_swift_format.md' ).read_text()
OUTPUT_MAPPING = {
    "Swift Dependencies": ( str, ... ),
    "Other Language Dependencies": ( str, ... ),
    "API Specifications": ( str, ... ),
    "Logic Analysis": ( List[ Tuple[ str, str ]], ... ),
    "Task Prioritization": (List[str], ...),
    "Shared Knowledge Base": ( str, ... ),
    "Clarifications Needed": ( str, ... )}

class WriteTasks(Action):
    def __init__(self, name="CreateTasks", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, context, rsp):
        ws_name = CodeParser.parse_str(block="Swift package name", text=context[-1].content)
        file_path = WORKSPACE_ROOT / ws_name / 'docs/api_spec_and_tasks.md'
        file_path.write_text(rsp.content)

        # Write requirements.txt
        requirements_path = WORKSPACE_ROOT / ws_name / 'requirements.txt'
        requirements_path.write_text( rsp.instruct_content.dict().get( "Swift Dependencies" ).strip( '"\n' ))

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format(context=context, format_example=FORMAT_EXAMPLE)
        rsp = await self._aask_v1(prompt, "task", OUTPUT_MAPPING)
        self._save(context, rsp)
        return rsp

class AssignTasks(Action):
    async def run(self, *args, **kwargs):
        # Here you should implement the actual action
        pass