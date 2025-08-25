# Slidy Presentation Generator

Slidy is a FastAPI-based service for generating PowerPoint presentations using LLMs and Stable Diffusion for images.

## API Endpoints

### `POST /generate/`

Generate a PowerPoint presentation based on a prompt and optional custom input.

- **Request Body** (JSON):
    - `prompt` (string): The main topic or subject for the presentation.
    - `custom_input` (string, optional): Additional instructions or content to include.

- **Response**:
    - Returns the generated `.pptx` file as a downloadable response.

#### Example Request

```json
POST /generate/
Content-Type: application/json

{
    "prompt": "The impact of AI on modern education",
    "custom_input": "Focus on both positive and negative effects."
}
```

#### Example Response

- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Downloaded file: `presentation.pptx`

---

## Sample Presentations

Sample generated presentations can be found in the generated_presentations folder

---

## Project Structure

- `server.py`: FastAPI server exposing the API.
- `generator.py`: Handles slide and image generation.
- `presentation.py`: PowerPoint slide creation logic.
- `stablediffusion.py`: Image generation using Stable Diffusion.
- `groqllm.py`: LLM integration for slide content.
- `images/`: Stores generated slide images.
- `presentations/`: Stores generated PowerPoint files.

---

## Running the Server

```
python3 server.py
```

---