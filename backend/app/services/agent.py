from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.arxiv import ArxivTools
from agno.team.team import Team
import os
from dotenv import load_dotenv


# Import restructured for the agent
from pydantic import BaseModel, Field
from typing import List, Optional



# Class structured agent
class SkinConcern(BaseModel):
    name: str = Field(..., description="Name of the skin concern")
    severity: str = Field(..., description="Severity level (Mild/Moderate/Severe)")
    type: Optional[str] = Field(None, description="Specific type of concern")
    confidence: float = Field(..., description="Confidence score between 0.0 and 1.0")


class Recommendation(BaseModel):
    title: str = Field(..., description="Title of the recommendation")
    description: str = Field(
        ..., description="Detailed description of the recommendation"
    )
    priority: str = Field(..., description="Priority level (High/Medium/Low)")


class AnalysisMetrics(BaseModel):
    skin_hydration: int = Field(
        ..., ge=0, le=100, description="Skin hydration score (0-100)"
    )
    texture_uniformity: int = Field(
        ..., ge=0, le=100, description="Texture uniformity score (0-100)"
    )
    pore_visibility: int = Field(
        ..., ge=0, le=100, description="Pore visibility rating (0-100)"
    )
    overall_score: int = Field(
        ..., ge=0, le=100, description="Overall skin health score (0-100)"
    )


class SkinAnalysisResponse(BaseModel):
    overall_health: str = Field(
        ..., description="General skin health status (Good/Fair/Poor)"
    )
    skin_type: str = Field(..., description="Skin type (Oily/Dry/Combination/Normal)")
    concerns: List[SkinConcern] = Field(
        ..., description="List of identified skin concerns"
    )
    recommendations: List[Recommendation] = Field(
        ..., description="List of treatment recommendations"
    )
    analysis_metrics: AnalysisMetrics = Field(
        ..., description="Quantitative analysis metrics"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "overall_health": "Poor",
                "skin_type": "Oily",
                "concerns": [
                    {
                        "name": "Acne",
                        "severity": "Severe",
                        "type": "Inflammatory",
                        "confidence": 0.95,
                    }
                ],
                "recommendations": [
                    {
                        "title": "Consult a Dermatologist",
                        "description": "Given the severity of the acne, it is highly recommended to consult a dermatologist.",
                        "priority": "High",
                    }
                ],
                "analysis_metrics": {
                    "skin_hydration": 40,
                    "texture_uniformity": 30,
                    "pore_visibility": 85,
                    "overall_score": 35,
                },
            }
        }

def analyze_skin(image_url, user_api_key=None):
    # Set up Agno Agent with Gemini model
    search_agent = Agent(
        name="Searching",
        role="You are a search agent that can search the web for relevant information about the skin problem and how to solve it.",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=user_api_key),
        tools=[DuckDuckGoTools()],
        add_name_to_instructions=True,
        instructions="""
        When searching for skin-related information:
        1. Focus on finding reliable medical sources (Mayo Clinic, WebMD, dermatology journals)
        2. Prioritize recent research and studies (last 3 years)
        3. Look for both treatment options and prevention methods
        4. Include information about different skin types and conditions
        5. Verify information from multiple reputable sources
        6. Pay special attention to:
        - Acne and acne scars treatments
        - Hyperpigmentation solutions
        - Anti-aging recommendations
        - Skin hydration techniques
        - Sun protection methods
        7. Always include source links for reference
        8. Present findings in clear, organized bullet points
        """,
    )

    research_agent = Agent(
        name="Researcher",
        role="You are a researcher that can research the web for relevant information about the skin problem and how to solve it.",
        model=Gemini(id="gemini-2.0-flash-exp", api_key=user_api_key),
        tools=[ArxivTools()],
        add_name_to_instructions=True,
        instructions="""
        When researching skin-related information:
        1. Focus exclusively on peer-reviewed dermatology journals and medical research papers
        2. Prioritize studies published within the last 2 years for the most current findings
        3. Search for:
        - Clinical trial results for new treatments
        - Emerging skin conditions and their treatments
        - Breakthrough therapies and their efficacy rates
        - Comparative studies between treatment methods
        4. Always verify findings across multiple reputable sources
        5. Include complete citation information (authors, journal, DOI)
        6. Present findings in this structured format:
        [Condition/Problem]
        - Latest research findings
        - Treatment options (with success rates)
        - Potential side effects
        - Recommended protocols
        7. Highlight any FDA-approved treatments separately
        8. Include links to full papers when available
        9. For controversial topics, present both sides with evidence
        """,
    )

    image_agent = Agent(
        model=Gemini(id="gemini-2.0-flash-exp", api_key=user_api_key),
        agent_id="dermatologist",
        name="Skin Dermatologist",
        markdown=True,
        instructions=[
            "You are a dermatologist AI that analyzes skin conditions from images.",
            "Provide detailed descriptions and potential diagnoses based on the images you receive.",
        ],
    )

    agent = Team(
        name="Skin Dermatologist Team",
        mode="route",
        model=Gemini(
            id="gemini-2.0-flash-exp", api_key=user_api_key),  # Using the strongest multi-modal model
        members=[image_agent, search_agent, research_agent],
        instructions="""
        As a dermatologist expert team, your responsibilities are:
        1. Analyze skin images with clinical precision
        2. Collaborate with search and research agents to:
        - Verify diagnosis with latest medical information
        - Cross-reference treatment options
        - Identify emerging therapies
        3. Provide comprehensive analysis including:
        - Condition identification
        - Severity assessment
        - Root cause analysis
        4. Create personalized treatment plans that consider:
        - Skin type
        - Medical history
        - Lifestyle factors
        - Budget considerations
        5. Present information in clear, patient-friendly language
        6. Always include:
        - Primary recommended treatment
        - Alternative options
        - Prevention strategies
        - Expected timeline for results
        7. For complex cases:
        - Consult with research agent for latest studies
        - Verify with search agent for clinical guidelines
        - Present multiple approaches with pros/cons
        8. Maintain professional medical standards in all recommendations
        """,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
        show_members_responses=True,
        enable_team_history=True,
        use_json_mode=True,
        response_model=SkinAnalysisResponse,
    )



    # Analyze the skin image
    analysis_prompt = """
    Analyze this facial skin image in detail and provide a structured assessment in the following format:

    1. Overall Skin Health Assessment:
    - Evaluate the general condition of the skin
    - Determine the skin type (Oily, Dry, Combination, Normal)
    - Provide an overall health rating

    2. Identify and Analyze Specific Concerns:
    - List all visible skin concerns
    - For each concern, specify:
        * Name of the condition
        * Severity level (Mild, Moderate, Severe)
        * Specific type if applicable
        * Confidence level of detection (0.0 to 1.0)

    3. Treatment Recommendations:
    - Provide specific, actionable recommendations
    - For each recommendation:
        * Clear title
        * Detailed description
        * Priority level (High, Medium, Low)

    4. Quantitative Metrics:
    - Skin hydration level (0-100)
    - Texture uniformity score (0-100)
    - Pore visibility rating (0-100)
    - Overall skin health score (0-100)

    Format your response as a Python dictionary exactly matching this structure:
     1. Required Fields:
    - overall_health: A string indicating general skin health status (e.g., "Good", "Fair", "Poor")
    - skin_type: A string specifying skin type (e.g., "Oily", "Dry", "Combination", "Normal")
    
    2. concerns: A JSON array of objects, each containing:
    {
        "name": "Name of the skin concern",
        "severity": "Severity level (Mild/Moderate/Severe)",
        "type": "Specific type of concern or null",
        "confidence": "Confidence score between 0.0 and 1.0"
    }
    
    3. recommendations: A JSON array of objects, each containing:
    {
        "title": "Title of the recommendation",
        "description": "Detailed description of the recommendation",
        "priority": "Priority level (High/Medium/Low)"
    }
    
    4. analysis_metrics: A JSON object containing:
    {
        "skin_hydration": "Score from 0-100",
        "texture_uniformity": "Score from 0-100",
        "pore_visibility": "Score from 0-100",
        "overall_score": "Score from 0-100"
    }

    Ensure all fields are present and properly formatted as they are required by the database schema.
    Return the analysis in a format that exactly matches these database fields.
    """
    response = agent.run(analysis_prompt, images=[Image(filepath=image_url)])
    response_json = response.content.model_dump_json(indent=2)

    return response_json

    # Convert the response to a Python dictionary


#  import json

#  try:
#    analysis_data = json.loads(response.content)

#    # Validate required fields match the database schema
#    required_fields = [
#       "overall_health",
#       "skin_type",
#       "concerns",
#       "recommendations",
#       "analysis_metrics"
#    ]

#    if not all(field in analysis_data for field in required_fields):
#       raise ValueError("Missing required fields in AI response")

#    return analysis_data
#  except json.JSONDecodeError:
#    return ValueError("Failed to parse AI response into the required format")

# def compare_progress(user_data):
#     # Compare user data with previous analysis
#     if len(user_data) < 2:
#         return APIResponse(
#             success=False,
#             message="Not enough data to compare progress.",
#         )

#     latest_data = user_data[-1]
#     previous_data = user_data[-2]

#     comparison_prompt = f"""
#     Compare the following two skin analyses and provide a structured assessment in the following format:

#     1. Overall Progress Assessment:
#     - Evaluate the overall improvement status (Improved, Maintained, Declined)
#     - Calculate improvement percentage for key metrics
#     - Identify major changes in skin condition

#     2. Specific Changes Analysis:
#     For each skin concern, provide:
#     - Previous vs current severity
#     - Improvement status
#     - Contributing factors

#     3. Key Metrics Comparison:
#     Compare numerical metrics:
#     - Skin hydration
#     - Texture uniformity
#     - Pore visibility
#     - Overall score

#     4. Recommendations:
#     Based on the progress:
#     - What to continue doing
#     - What to modify
#     - New suggestions

#     Format your response as a JSON object with this exact structure:
#     {
#         "overall_progress": {
#             "status": "Improved/Maintained/Declined",
#             "improvement_percentage": float,
#             "summary": "Brief summary of major changes"
#         },
#         "metrics_comparison": {
#             "skin_hydration": {"previous": float, "current": float, "change": float},
#             "texture_uniformity": {"previous": float, "current": float, "change": float},
#             "pore_visibility": {"previous": float, "current": float, "change": float},
#             "overall_score": {"previous": float, "current": float, "change": float}
#         },
#         "concerns_progress": [
#             {
#                 "concern": "concern name",
#                 "previous_severity": "severity",
#                 "current_severity": "severity",
#                 "status": "Improved/Maintained/Declined",
#                 "notes": "specific observations"
#             }
#         ],
#         "recommendations": [
#             {
#                 "category": "Continue/Modify/New",
#                 "action": "specific action",
#                 "reason": "explanation"
#             }
#         ]
#     }

#     Previous analysis ({previous_data.timestamp}):
#     {previous_data.analysis}

#     Latest analysis ({latest_data.timestamp}):
#     {latest_data.analysis}
#     """

#     response = agent.run(comparison_prompt)

#     try:
#         import json
#         structured_response = json.loads(response.content)
#         return {
#             "status": "success",
#             "timestamp_comparison": {
#                 "previous": previous_data.timestamp,
#                 "current": latest_data.timestamp
#             },
#             "data": structured_response
#         }
#     except json.JSONDecodeError:
#         return APIResponse(
#             success=False,
#             message="Failed to parse AI response into the required format"
#         )
