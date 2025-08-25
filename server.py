from fastapi import FastAPI
from fastapi.responses import FileResponse
import generator, presentation

app = FastAPI()

@app.post("/generate/")
def generate_presentation(data: dict):
    print(data)
    presentation_slides=generator.generate_slides(data["prompt"], data.get("custom_input", ""))
    file_path=presentation.create_presentation(presentation_slides, presentation_slides.get("output_file_name", "presentation.pptx"))
    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="presentation.pptx"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=3005, reload=True)