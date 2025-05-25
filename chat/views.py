import openai
from openai import OpenAI
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decouple import config

client = OpenAI(api_key=config("OPENAI_API_KEY"))

@api_view(['POST'])
def chat_view(request):
    user_message = request.data.get("message")

    if not user_message:
        return Response({"error": "Message is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a kind and supportive therapy assistant named Calmari. Help the user with their mental health needs."},
                {"role": "user", "content": user_message},
            ]
        )

        ai_message = response.choices[0].message.content
        return Response({"reply": ai_message}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
