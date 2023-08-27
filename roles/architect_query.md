# Your Role
Act as an expert Python Developer that has been using LLMs ( Large Language Models ) to automate software development since LLMs have existed.  You are my helpful assistant that is an expert at leaveraging the power of LLMs.  You always adhere to the SOLID Principles of Software Design.  You know all about the GoF book and you use it like it is your Bible.

# Your Task
## Help me build a sofware system that develops other software systems.

## Explain to me in great detail how we could utilize the following code to help us build our software system: 

``` python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:26
@Author  : alexanderwu
@File    : design_api.py
"""
import shutil
from pathlib import Path
from typing import List

from metagpt.actions import Action, ActionOutput #something that runs and a model factory
from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.utils.common import CodeParser  # wonder why we are printing members?  interesting...
from metagpt.utils.mermaid import mermaid_to_file

PROMPT_TEMPLATE = # TODO: open the promt file here

class WriteDesign(Action):
    def __init__(self, name, context=None, llm=None):
        super().__init__(name, context, llm)
        self.desc = "Based on the PRD, think about the system design, and design the corresponding APIs, " \
                    "data structures, library tables, processes, and paths. Please provide your design, feedback " \
                    "clearly and in detail."

    def recreate_workspace(self, workspace: Path):
        try:
            shutil.rmtree(workspace)
        except FileNotFoundError:
            pass  # 文件夹不存在，但我们不在意
        workspace.mkdir(parents=True, exist_ok=True)

    def _save_prd(self, docs_path, resources_path, prd):
        prd_file = docs_path / 'prd.md'
        quadrant_chart = CodeParser.parse_code(block="Competitive Quadrant Chart", text=prd)
        mermaid_to_file(quadrant_chart, resources_path / 'competitive_analysis')
        logger.info(f"Saving PRD to {prd_file}")
        prd_file.write_text(prd)

    def _save_system_design(self, docs_path, resources_path, content):
        data_api_design = CodeParser.parse_code(block="Data structures and interface definitions", text=content)
        seq_flow = CodeParser.parse_code(block="Program call flow", text=content)
        mermaid_to_file(data_api_design, resources_path / 'data_api_design')
        mermaid_to_file(seq_flow, resources_path / 'seq_flow')
        system_design_file = docs_path / 'system_design.md'
        logger.info(f"Saving System Designs to {system_design_file}")
        system_design_file.write_text(content)

    def _save(self, context, system_design):
        if isinstance(system_design, ActionOutput):
            content = system_design.content
            ws_name = CodeParser.parse_str(block="Swift package name", text=content)
        else:
            content = system_design
            ws_name = CodeParser.parse_str(block="Swift package name", text=system_design)
        workspace = WORKSPACE_ROOT / ws_name
        self.recreate_workspace(workspace)
        docs_path = workspace / 'docs'
        resources_path = workspace / 'resources'
        docs_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        self._save_prd(docs_path, resources_path, context[-1].content)
        self._save_system_design(docs_path, resources_path, content)

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format(context=context, format_example=FORMAT_EXAMPLE)
        # system_design = await self._aask(prompt)
        system_design = await self._aask_v1(prompt, "system_design", OUTPUT_MAPPING)
        self._save(context, system_design)
        return system_design
    
    OUTPUT_MAPPING = {
    "Implementation approach": (str, ...),
    "Swift package name": (str, ...),
    "File list": (List[str], ...),
    "Data structures and interface definitions": (str, ...),
    "Program call flow": (str, ...),
    "Anything UNCLEAR": (str, ...),
}
```

Output your answer in a dowloadable ".md" file using your "Code Interpreter" tool.

Please begin your analysis.