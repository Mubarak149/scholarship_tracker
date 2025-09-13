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



def extract_scholarship_data(text: str) -> dict:
    """Extract structured scholarship data + custom fields."""

    response_schemas = [
        ResponseSchema(name="name", description="Scholarship name"),
        ResponseSchema(name="provider", description="Scholarship provider or organization"),
        ResponseSchema(name="funding_type", description="Funding type: full or partial"),
        ResponseSchema(name="deadline", description="Application deadline (YYYY-MM-DD, if mentioned)"),
        ResponseSchema(name="flight_ticket_fee", description="Does it cover flight ticket? yes/no"),
        ResponseSchema(name="visa_application_fee", description="Does it cover visa application fee? yes/no"),
        ResponseSchema(name="work_permit_available", description="Is a work permit available? yes/no"),
        ResponseSchema(
            name="summary",
            description="A JSON list of 4-8 concise bullet points about the scholarship"
        ),
        ResponseSchema(
            name="custom_fields",
            description="""A JSON list of {field_name, field_value} for other details not covered above.
                           Examples: Eligible Countries, Age Limit, Degree Level."""
        ),
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    template = f"""
    Extract structured scholarship details from the text below.
    Include extra details under "custom_fields" if they don't fit the main fields.

    {format_instructions.replace("{", "{{").replace("}", "}}")}

    Scholarship Description:
    {{description}}
    """

    prompt = PromptTemplate.from_template(template)
    llm = ChatGroq(groq_api_key=settings.GROQ_API_KEY, model="qwen/qwen3-32b")

    chain = prompt | llm | output_parser
    parsed = chain.invoke({"description": text})

    # Normalize boolean conversions
    parsed["flight_ticket_fee"] = str(parsed.get("flight_ticket_fee", "")).lower() in ["yes", "true"]
    parsed["visa_application_fee"] = str(parsed.get("visa_application_fee", "")).lower() in ["yes", "true"]
    parsed["work_permit_available"] = str(parsed.get("work_permit_available", "")).lower() in ["yes", "true"]

    return parsed
