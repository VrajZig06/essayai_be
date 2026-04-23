# Parallel Workflow in Langgraph

from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_SECRET = os.getenv("GROQ_SECRET")

llm = ChatGroq(
    groq_api_key=GROQ_SECRET,
    model="openai/gpt-oss-120b"
)
from langgraph.graph import START, StateGraph, END
import uuid


# Pydantic output Parser
class EvaluationResponse(BaseModel):
    feedback: str = Field(description="This is feedback text after evaluted by the LLM")
    score: int = Field(description="Give Score based on evaluation in range of 1-10")


pydantic_parser = PydanticOutputParser(pydantic_object=EvaluationResponse)

# Alternative: Separate prompts for each individual attribute
CLARITY_PROMPT = PromptTemplate(
    input_variables=["content"],
    partial_variables={"format_instruction": pydantic_parser.get_format_instructions()},
    template="""
         You are an expert evaluator focused specifically on CLARITY OF THOUGHTS.

         Evaluate the following content on a scale of 1-10 for clarity of thoughts only:

         Clarity Criteria:
         - How well-organized and logical are the ideas?
         - Is the reasoning easy to follow?
         - Are concepts presented in a coherent manner?

         Output Format:
         Individual Score: X/10
         Attribute-Specific Feedback: [Feedback focused ONLY on clarity]
         Examples: [Specific examples of clarity issues or strengths]
         Improvement Suggestions: [Targeted advice for improving clarity]

         CONTENT TO EVALUATE:
         {content}

         \n {format_instruction}
      """,
)

DEPTH_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["content"],
    partial_variables={"format_instruction": pydantic_parser.get_format_instructions()},
    template="""
         You are an expert evaluator focused specifically on DEPTH OF ANALYSIS.

         Evaluate the following content on a scale of 1-10 for depth of analysis only:

         Depth Criteria:
         - How thoroughly are topics explored?
         - Is there critical thinking and insight?
         - Are multiple perspectives considered?
         - Is the analysis superficial or comprehensive?

         Output Format:
         Individual Score: X/10
         Attribute-Specific Feedback [Feedback focused ONLY on analysis depth]
         Examples:[Specific examples showing analysis depth]
         Improvement Suggestions [Targeted advice for deepening analysis]

         CONTENT TO EVALUATE:
         {content}

         \n {format_instruction}
   """,
)

LANGUAGE_QUALITY_PROMPT = PromptTemplate(
    input_variables=["content"],
    partial_variables={"format_instruction": pydantic_parser.get_format_instructions()},
    template="""
         You are an expert evaluator focused specifically on LANGUAGE QUALITY.

         Evaluate the following content on a scale of 1-10 for language quality only:

         Language Criteria:
         - Grammar correctness
         - Spelling accuracy
         - Sentence structure and flow
         - Vocabulary appropriateness
         - Punctuation usage

         Output Format:
         Individual Score: X/10
         Attribute-Specific Feedback: [Feedback focused ONLY on language]
         Examples: [Specific examples of language issues or strengths]
         Improvement Suggestions: [Targeted advice for improving language]

         CONTENT TO EVALUATE:
         {content}

         \n {format_instruction}
      """,
)

# Overall Conclusion and Score Summation Prompt
OVERALL_CONCLUSION_PROMPT = PromptTemplate(
    input_variables=["clarity_evaluation", "depth_evaluation", "language_evaluation"],
    partial_variables={"format_instruction": pydantic_parser.get_format_instructions()},
    template="""
      Generate an overall conclusion based on three individual evaluations.

      EVALUATIONS:
      Clarity: {clarity_evaluation}
      Depth: {depth_evaluation}
      Language: {language_evaluation}

      TASK:
      1. Extract individual scores (1-10 each)
      2. Calculate total score (max 30)
      3. Provide overall conclusion with key strengths and improvement areas

      OUTPUT:
      - Individual scores breakdown
      - Total score/30
      - Performance level: Exceptional (27-30), Excellent (21-26), Good (15-20), Needs Improvement (9-14), Poor (3-8)
      - Brief overall conclusion
      - 2-3 key strengths
      - 2-3 priority recommendations

      \n {format_instruction}
   """,
)

# Create Model
model = llm


# Create Graph state
class EssayState(TypedDict):
    essay: str

    # --------- Evaluation Points ---------
    # Clarity of thoughts
    clarity_of_thoughts_score: int
    clarity_of_thoughts_feedback: str

    # Depth Analysis
    depth_analysis_score: int
    depth_analysis_feedback: str

    # Language Formation
    language_quality_score: int
    language_quality_feedback: str

    # final Score
    final_score: int
    final_feedback: str


# Evaluate Clarity of thoughts
def evaluate_clarity_of_thoughts(state: EssayState):
    essay = state["essay"]

    prompt = CLARITY_PROMPT.invoke({"content": essay})
    llm_response = model.invoke(prompt)

    result = pydantic_parser.parse(llm_response.content)

    state["clarity_of_thoughts_feedback"] = result.feedback
    state["clarity_of_thoughts_score"] = result.score

    # return state
    return {
        "clarity_of_thoughts_feedback": result.feedback,
        "clarity_of_thoughts_score": result.score,
    }


# Evaluate Depth Analysis
def evaluate_depth_analysis(state: EssayState):
    essay = state["essay"]

    prompt = DEPTH_ANALYSIS_PROMPT.invoke({"content": essay})
    llm_response = model.invoke(prompt)

    result = pydantic_parser.parse(llm_response.content)

    state["depth_analysis_feedback"] = result.feedback
    state["depth_analysis_score"] = result.score

    # return state
    return {
        "depth_analysis_feedback": result.feedback,
        "depth_analysis_score": result.score,
    }


# Evaluate Language
def evaluate_language(state: EssayState):
    essay = state["essay"]

    prompt = LANGUAGE_QUALITY_PROMPT.invoke({"content": essay})
    llm_response = model.invoke(prompt)

    result = pydantic_parser.parse(llm_response.content)

    state["language_quality_feedback"] = result.feedback
    state["language_quality_score"] = result.score

    # return state
    return {
        "language_quality_feedback": result.feedback,
        "language_quality_score": result.score,
    }


# Evaluate Overall Feedback
def evaluate_final_feedback(state: EssayState):
    prompt = OVERALL_CONCLUSION_PROMPT.invoke(
        {
            "clarity_evaluation": state["clarity_of_thoughts_feedback"],
            "depth_evaluation": state["depth_analysis_feedback"],
            "language_evaluation": state["language_quality_feedback"],
        }
    )

    # Get LLM Response
    llm_response = model.invoke(prompt)

    result = pydantic_parser.parse(llm_response.content)

    state["final_feedback"] = result.feedback
    state["final_score"] = (
        state["clarity_of_thoughts_score"]
        + state["depth_analysis_score"]
        + state["language_quality_score"]
    )

    # return state
    return {
        "final_feedback": result.feedback,
        "final_score": (
            state["clarity_of_thoughts_score"]
            + state["depth_analysis_score"]
            + state["language_quality_score"]
        ),
    }


# Function: Generate HTML Report
def generate_html_report(data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Essay Evaluation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f7fa;
                color: #333;
            }}
            h1 {{
                text-align: center;
                color: #2c3e50;
            }}
            .section {{
                background: #ffffff;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .score {{
                font-weight: bold;
                color: #e74c3c;
            }}
            .title {{
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            pre {{
                white-space: pre-wrap;
                font-family: inherit;
            }}
        </style>
    </head>
    <body>

        <h1>Essay Evaluation Report</h1>

        <div class="section">
            <div class="title">Essay</div>
            <p>{data["essay"]}</p>
        </div>

        <div class="section">
            <div class="title">Overall Score</div>
            <p class="score">{data["final_score"]} / 30</p>
        </div>

        <div class="section">
            <div class="title">Clarity of Thoughts ({data["clarity_of_thoughts_score"]}/10)</div>
            <pre>{data["clarity_of_thoughts_feedback"]}</pre>
        </div>

        <div class="section">
            <div class="title">Depth of Analysis ({data["depth_analysis_score"]}/10)</div>
            <pre>{data["depth_analysis_feedback"]}</pre>
        </div>

        <div class="section">
            <div class="title">Language Quality ({data["language_quality_score"]}/10)</div>
            <pre>{data["language_quality_feedback"]}</pre>
        </div>

        <div class="section">
            <div class="title">Final Feedback</div>
            <pre>{data["final_feedback"]}</pre>
        </div>

    </body>
    </html>
    """
    return html


def save_report(state: EssayState):
    report_id = uuid.uuid4()
    
    # Create directory if it doesn't exist
    import os
    os.makedirs("essay_reports", exist_ok=True)

    # Save file
    with open(
        f"essay_reports/essay_{report_id}_report.html", "w", encoding="utf-8"
    ) as file:
        file.write(generate_html_report(state))

    print(f"essay_{report_id}_report Generated...")

    return state


graph = StateGraph(EssayState)

# Create Nodes
graph.add_node("eval_cot", evaluate_clarity_of_thoughts)
graph.add_node("eval_da", evaluate_depth_analysis)
graph.add_node("eval_lq", evaluate_language)
graph.add_node("final_eval", evaluate_final_feedback)
graph.add_node("save_report", save_report)

# Starting Phase
graph.add_edge(START, "eval_cot")
graph.add_edge(START, "eval_da")
graph.add_edge(START, "eval_lq")

# Handle Parallel Execution
graph.add_edge("eval_cot", "final_eval")
graph.add_edge("eval_da", "final_eval")
graph.add_edge("eval_lq", "final_eval")

# Terminate the Graph
graph.add_edge("final_eval", "save_report")
graph.add_edge("save_report", END)

# Compile the Graph
workflow = graph.compile()

# # Essay
# result = workflow.invoke(
#     {
#         "essay": """Indian Politics: A Dynamic Democratic System

# Indian politics is one of the most complex and vibrant political systems in the world. As the largest democracy, India operates under a constitutional framework that ensures representation, rights, and governance for over a billion people. Since gaining independence in 1947, the nation has developed a unique political identity shaped by diversity, democratic values, and continuous evolution.

# At the heart of Indian politics lies the Constitution of India, which came into effect on January 26, 1950. It establishes India as a sovereign, socialist, secular, and democratic republic. The Constitution provides a clear separation of powers among the executive, legislature, and judiciary, ensuring a system of checks and balances. This framework has helped maintain stability while allowing flexibility to adapt to changing societal needs.

# India follows a parliamentary system of government, where the President is the constitutional head, and the Prime Minister is the executive head. The Parliament consists of two houses: the Lok Sabha (House of the People) and the Rajya Sabha (Council of States). Political parties play a crucial role in this system, ranging from national parties to regional ones, each representing different ideologies, cultures, and interests. This diversity often leads to coalition governments, reflecting the inclusive nature of Indian democracy.

# One of the defining features of Indian politics is its electoral system. Elections are conducted by the Election Commission of India, an independent body that ensures free and fair elections. The use of Electronic Voting Machines (EVMs) and the large-scale participation of voters make Indian elections a remarkable democratic exercise. Citizens above the age of 18 have the right to vote, making public participation a cornerstone of governance.

# However, Indian politics also faces several challenges. Issues such as corruption, caste-based politics, communalism, and political polarization continue to affect the system. The influence of money and muscle power in elections is another concern. Despite these challenges, there has been increasing awareness among citizens, leading to greater demand for transparency and accountability.

# In recent years, Indian politics has seen significant transformations due to technological advancements and social media. These platforms have enabled better communication between leaders and citizens but have also contributed to the spread of misinformation. Political campaigns have become more data-driven, and public opinion plays a more visible role than ever before.

# Despite its complexities, Indian politics remains a strong example of democratic resilience. Peaceful transitions of power, active judiciary interventions, and a vibrant civil society contribute to the strength of the system. The participation of youth and increasing political awareness signal a promising future for the country.

# In conclusion, Indian politics is a dynamic blend of tradition and modernity, challenges and opportunities. While it continues to evolve, the core principles of democracy, justice, and equality remain its guiding force. The success of Indian politics ultimately depends on the active participation of its citizens and their commitment to democratic values."""
#     }
# )

# print(result)
