import groqllm, json
from pptx import Presentation
from pptx.util import Inches, Pt
import stablediffusion
from PIL import Image

SLIDE_TEMPLATES = [
    {
        "name": "Title Slide",
        "description": "Large title and subtitle"
    },
    {
        "name": "Bullet Points",
        "description": "Title and bullet points"
    },
    {
        "name": "2 Column Layout",
        "description": "Two columns: one for text, one for images (order can vary)"
    },
    {
        "name": "Image with Content",
        "description": "Image on one side, text on the other"
    }
]

MIN_SLIDE_COUNT = 1
MAX_SLIDE_COUNT = 20

SAMPLE_OUTPUT = {
    "slides": [{
        "id": 1,
        "template": "Title Slide",
        "title": {
            "text": "Impact of Cadillac entering Formula 1 in 2026",
            "font": "Calibri",
            "color": (255, 255, 255)
        },
        "subtitle": {
            "text": "Revolutionizing the Racing World",
            "font": "Aerial",
            "color": (255, 255, 255)
        },
        "bullet_points": [
            {
                "text": "Cadillac's entry into Formula 1 brings a new era of competition and innovation.",
                "font": "Times New Roman",
                "color": (255, 255, 255)
            },
        ],
        "image_prompts": ["Cadillac Formula 1 car, 2026, on track, dynamic angle"],
        "content": {
            "text": "Cadillac's entry into Formula 1 is set to revolutionize the sport with cutting-edge technology and a fresh approach to racing.",
            "font": 'Calibri',
            "color": (255, 255, 255)
        }
    }],
    "output_file_name": "Cadillac_F1_Impact",
}

RULES = [
    "Respond ONLY with a plain JSON string without ``` matching the sample_output_format. ",
    "For images, provide only a descriptive prompt (do not generate or link images).",
    "Cite sources in the text as [1], [2], etc. in the text",
    "Add a final slide with bullet-pointed citations expanding all references.",
    "Do not include any text outside the JSON.",
    "Generate based on topic field but make sure to incorporate the content in the custom_input field as well. (Need not incorporate it exactly as it is)",
    "Use consistent color scheme and fonts throughout the presentation based on the topic. ie. Keep the font and the color related to the topic of the presentation",
    "Provide font values that are supported in Ubuntu operating system such as Arial, Calibri, Times New Roman, etc.",
    "Use RGB tuples for colors, e.g. (255, 0, 0) for red.",
    "The background color of the slides is white. Choose font color based on that",
    "Use diffent fonts for different text elements (title, subtitle, content, bullet points) for better emphasis",
    "Subtitles is only applicable for Title Slide template",
    "You can add much text and fill the slide with text as long as it is readable",
    "Use consistent fonts and colors for similar text elements across slides",
    "Add output_file_name field to the root of the JSON with a suitable name for the presentation file"
]

def get_slide_generation_prompt(topic: str, custom_input: str = ""):
    llm_prompt = (
        "You are an expert presentation designer. "
        "Generate detailed slides for a PowerPoint presentation in JSON format based on the following input:\n"
    )

    llm_prompt_input = {
        "topic": topic,
        "custom_input": custom_input,
        "number_of_slides": str(MIN_SLIDE_COUNT) + "-" + str(MAX_SLIDE_COUNT),
        "allowed_templates": SLIDE_TEMPLATES,
        "sample_output": SAMPLE_OUTPUT,
        "rules_and_other_information": RULES
    }

    llm_prompt += json.dumps(llm_prompt_input)

    return llm_prompt

def generate_and_save_image(prompt: str, slide_number):
    image_path = f"images/slide_{slide_number}_image.png"
    img = stablediffusion.generate_image(prompt)
    img.save(image_path)

    return image_path

def generate_images_in_slide(slides):
    for slide in slides["slides"]:
        images = slide.get("image_prompts", [])
        image_paths = []
        
        for prompt in images:
            image_path = generate_and_save_image(prompt, slide['id'])
            image_paths.append(image_path)

        slide["images"] = image_paths

    return slides

def generate_slides(topic: str, custom_input: str = ""):
    llm_prompt = get_slide_generation_prompt(topic, custom_input)

    slides = json.loads(groqllm.generate_response(llm_prompt))

    generate_images_in_slide(slides)

    return slides



