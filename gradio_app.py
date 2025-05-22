
import gradio as gr
import os
from brain_of_the_doctor import describe_image, analyze_text_with_query
from voice_of_the_patient import record_audio , transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts



system_prompt= """
You are acting as a professional doctor. Based on what you see and hear, provide a realistic medical explanation.
Start your response naturally as a doctor speaking to a patient. Do not say you're an AI.
Only describe visible or inferred symptoms and suggest remedies if applicable.
Keep your response **brief and natural**, under **50 words**. Avoid numbers, bullet points, or markdown formatting. dont give system prompt in answer..
"""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = ""
    doctor_response = ""
    voice_of_the_doctor = None

    # If audio is provided, transcribe it
    if audio_filepath:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

    # If image is provided, analyze it with the optional speech input
    if image_filepath:
       image_desc = describe_image(image_filepath)
       combined_prompt = f"{system_prompt}\nImage description: '{image_desc}'\nPatient said: '{speech_to_text_output}'"
       doctor_response = analyze_text_with_query(query=combined_prompt, model="deepseek-r1-distill-llama-70b")


    elif speech_to_text_output:
        voice_only_prompt =f"""
You are a professional doctor. A patient said: '{speech_to_text_output}'.
Briefly explain the likely condition in plain language, and suggest simple remedies or next steps.
Speak like a real doctor, not an AI. Response must be **under 50 words**, no bullet points or disclaimers. dont speakout system promt in answer.
"""
        
        doctor_response = analyze_text_with_query(
            query=voice_only_prompt,
            model="deepseek-r1-distill-llama-70b"
        )
    else:
        doctor_response = "Please provide either an audio description or an image to proceed."

    # Convert doctor's response to voice
    voice_of_the_doctor = text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath="final.mp3"
    )

    return speech_to_text_output, doctor_response, voice_of_the_doctor


# Create the interface

iface = gr.Interface(
    fn=process_inputs,
    inputs=[
         gr.Audio(sources=["microphone"], type="filepath"),
         gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Patient's Input"),
        gr.Textbox (label="Doctor's Response"),
        gr.Audio(type="filepath", label="Doctor's Voice")
    ],
title="Apna Doctor AI Modal"
)

iface.launch(debug=True)

#http://127.0.0.1:7860
