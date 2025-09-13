from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from django.conf import settings

def summarize_description(text: str) -> str:
    """Use Groq LLM to summarize scholarship description into bullet points."""

    response_schemas = [
        ResponseSchema(
            name="bullets",
            description="A list of 4-8 concise bullet points summarizing the scholarship."
        ),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    template = f"""
    Summarize the following scholarship description into 4-8 concise bullet points.
    - Keep each point under 15 words.
    - Focus on key details: funding type, eligibility, benefits, deadlines.
    - Output MUST follow this format strictly:

    {format_instructions.replace("{", "{{").replace("}", "}}")}

    Scholarship Description:
    {{description}}
    """

    prompt = PromptTemplate.from_template(template)
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model="qwen/qwen3-32b"
    )

    chain = prompt | llm | output_parser
    parsed = chain.invoke({"description": text})

    bullets = parsed.get("bullets", [])
    return "\n".join(f"- {point}" for point in bullets)

