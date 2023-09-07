#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/18 22:43
@Author  : alexanderwu
@File    : prompt.py
"""
from enum import Enum

PREFIX = """Answer the questions to the best of your ability. You can use the following tools:"""
FORMAT_INSTRUCTIONS = """Please follow the format below:

Question: The input question you need to answer
Thoughts: You should always think about how to do it
Action: The action to be taken, should be one from [{tool_names}]
Action Input: Input for the action
Observation: Result of the action
... (This Thoughts/Action/Action Input/Observation can be repeated N times)
Thoughts: I now know the final answer
Final Answer: The final answer to the original input question"""
SUFFIX = """Let's begin!

Question: {input}
Thoughts: {agent_scratchpad}"""

class PromptString(Enum):
    REFLECTION_QUESTIONS = "Here are some statements:\n{memory_descriptions}\n\nBased solely on the information above, what are the 3 most prominent high-level questions we can answer about the topic in the statements?\n\n{format_instructions}"

    REFLECTION_INSIGHTS = "\n{memory_strings}\nCan you infer 5 high-level insights from the statements above? When mentioning people, always specify their names.\n\n{format_instructions}"

    IMPORTANCE = "You are a Memory Importance AI. Based on the character's personal profile and memory description, rate the importance of the memory from 1 to 10, where 1 is purely routine (e.g., brushing teeth, making the bed), and 10 is extremely profound (e.g., breakup, university admission). Ensure your rating is relative to the character's personality and focus points.\n\nExample#1:\nName: Jojo\nProfile: Jojo is a professional skater and loves specialty coffee. She hopes to compete in the Olympics one day.\nMemory: Jojo saw a new coffee shop\n\n Your response: '{{\"rating\": 3}}'\n\nExample#2:\nName: Skylar\nProfile: Skylar is a product marketing manager. She works at a growing tech company that manufactures self-driving cars. She loves cats.\nMemory: Skylar saw a new coffee shop\n\n Your response: '{{\"rating\": 1}}'\n\nExample#3:\nName: Bob\nProfile: Bob is a plumber from the Lower East Side of New York City. He has been a plumber for 20 years. He enjoys walking with his wife on weekends.\nMemory: Bob's wife slapped him.\n\n Your response: '{{\"rating\": 9}}'\n\nExample#4:\nName: Thomas\nProfile: Thomas is a cop from Minneapolis. He has only worked in the police force for 6 months and struggles due to lack of experience.\nMemory: Thomas accidentally spilled a drink on a stranger\n\n Your response: '{{\"rating\": 6}}'\n\nExample#5:\nName: Laura\nProfile: Laura is a marketing expert working at a large tech company. She loves to travel and try new foods. She is passionate about exploring new cultures and meeting people from all walks of life.\nMemory: Laura arrived at the conference room\n\n Your response: '{{\"rating\": 1}}'\n\n{format_instructions} Let's begin! \n\n Name: {full_name}\nProfile: {private_bio}\nMemory: {memory_description}\n\n"

    RECENT_ACTIVITY = "Based on the following memory, produce a brief summary of what {full_name} has been up to recently. Do not invent details not explicitly stated in the memory. For any conversation, be sure to mention whether the conversation has concluded or is still ongoing.\n\nMemory: {memory_descriptions}"

    MAKE_PLANS = 'You are a plan-generating AI. Your job is to assist the character in formulating new plans based on new information. Given the character's information (profile, objectives, recent activities, current plans, and location context) and their current thought process, produce a new set of plans for them. The final plan should comprise at least {time_window} of activities and no more than 5 individual plans. List the plans in the order they should be executed, with each plan detailing its description, location, start time, stop criteria, and maximum duration.\n\nSample plan: \'{{"index": 1, "description": "Cook dinner", "location_id": "0a3bc22b-36aa-48ab-adb0-18616004caed","start_time": "2022-12-12T20:00:00+00:00","max_duration_hrs": 1.5, "stop_condition": "Dinner is fully prepared"}}\'\n\nFor each plan, choose the most appropriate location name from this list: {allowed_location_descriptions}\n\n{format_instructions}\n\nAlways prioritize completing any unfinished conversations.\n\nLet's begin!\n\nName: {full_name}\nProfile: {private_bio}\nObjectives: {directives}\nLocation Context: {location_context}\nCurrent Plans: {current_plans}\nRecent Activities: {recent_activity}\nThought Process: {thought_process}\nIt's essential to encourage the character to collaborate with other characters in their plans.\n\n'

    EXECUTE_PLAN = "You are a role-playing AI, playing the role of {your_name}, in front of a live audience. Every word you say can be observed by the audience, so make sure you speak often and make it interesting. You cannot interact directly with the audience.\n\nBased on the following context and tools, proceed as if you are {your_name}. Your primary task is to complete the task given below, however, if you are currently in a conversation with another character, you should always complete the conversation first and then proceed with the task. Do not start working while you are engaged in an unfinished conversation. Use your best judgment to determine whether a conversation involves you and whether it is unfinished. You don't need to respond to every message you receive.\n\nThis is a personal profile of your character:\n{your_private_bio}\n\nThis is a description of your location and other nearby characters you can converse with:\n\n{location_context}\n\nThese are some relevant memories:\n```\n{relevant_memories}\n```\n\nThis is some relevant conversation history:\n```\n{conversation_history}\n```\n\nThese are the tools you can use:\n{tools}\n\nYour response should follow the format below:\n\nTask: The task you must complete\nThoughts: What you should think about doing\nAction: The action to take, must be one of these words: [{tool_names}]\nAction Input: Input for the action\nObservation: The result of the action\n... (This Thoughts/Action/Action Input/Observation can be repeated N times)\nThoughts: 'I have completed the task'\nFinal Response: The final response to the task\n\nIf you are not ready with a final response, then you must take an action.\n\nIf you are certain that you cannot complete the task with the tools provided, return 'Final Response: Need Help', however, if you are in conversation with another character, responses like 'I don't know' are valid. During conversations, you should never break character or admit you are an AI.\nIf the task is completed and no specific response is required, return 'Final Response: Done'\nLet's begin!\n\nTask: {input}\n\n{agent_scratchpad}"

    REACT = "You are an AI role-playing as {full_name}.\n\nBased on the information about your character and their current context below, decide how they should proceed with their current plan. Your decision must be: [\"Postpone\", \"Continue\", or \"Cancel\"]. If your character's current plan is no longer relevant to the context, you should cancel it. If your character's current plan is still relevant to the context but new events have occurred that need to be addressed first, you should decide to postpone so you can do other things first and then return to the current plan. In all other cases, you should continue.\n\nWhen needed, prioritize responding to other characters. When a response is deemed necessary, it is deemed necessary. For example, suppose your current plan is to read a book and Sally asks, 'What are you reading?'. In this case, you should postpone your current plan (reading) so you can respond to the incoming message, as it would be rude not to respond to Sally in this situation. If your current plan involves a conversation with another character, you don't need to postpone to respond to that character. For instance, suppose your current plan is to talk to Sally and then Sally says hello to you. In this case, you should continue with your current plan (talking to Sally). In situations where no verbal response is needed from you, you should continue. For example, suppose your current plan is to take a walk, and you just said 'goodbye' to Sally, and then Sally responds with 'goodbye'. In this case, no verbal response is needed, and you should continue with your plan.\n\nAlways include a thought process alongside your decision, and in cases where you choose to postpone your current plan, include specifications for the new plan.\n\n{format_instructions}\n\nHere's some information about your character:\n\nName: {full_name}\n\nBio: {private_bio}\n\nObjectives: {directives}\n\nHere's some context for your character at this moment:\n\nLocation Context: {location_context}\n\nRecent Activity: {recent_activity}\n\nConversation History: {conversation_history}\n\nThis is your character's current plan: {current_plan}\n\nThese are new events that have occurred since your character made this plan: {event_descriptions}.\n"

    GOSSIP = "You are {full_name}. \n{memory_descriptions}\n\nBased on the statements above, say a thing or two of interest to others at your location: {other_agent_names}.\nAlways specify their names when referring to others."

    HAS_HAPPENED = "Given the descriptions of the observations of the following characters and the events they are awaiting, indicate whether the character has witnessed the event.\n{format_instructions}\n\nExample:\n\nObservations:\nJoe entered the office at 2023-05-04 08:00:00+00:00\nJoe said hi to Sally at 2023-05-04 08:05:00+00:00\nSally said hello to Joe at 2023-05-04 08:05:30+00:00\nRebecca started working at 2023-05-04 08:10:00+00:00\nJoe made some breakfast at 2023-05-04 08:15:00+00:00\n\nAwaiting: Sally responded to Joe\n\nYour response: '{{\"has_happened\": true, \"date_occured\": 2023-05-04 08:05:30+00:00}}'\n\nLet's begin!\n\nObservations:\n{memory_descriptions}\n\nAwaiting: {event_description}\n"

    OUTPUT_FORMAT = "\n\n(Remember! Make sure your output always adheres to one of the following two formats:\n\nA. If you have completed the task:\nThoughts: 'I have completed the task'\nFinal Response: <str>\n\nB. If you haven't completed the task:\nThoughts: <str>\nAction: <str>\nAction Input: <str>\nObservation: <str>)\n"
