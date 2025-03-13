It is an application where you can keep a diary as you wish, choose the diary you want from the diaries you keep, and evaluate the diaries you 
choose from the eyes of artificial intelligence. In this way, artificial intelligence will be able to make a general assessment based on the events
you experience and give you various recommendations based on these events.

I got help from streamlit library for frontend and backend design in the project. I also got help from the pydantic library for the artificial 
intelligence evaluation. The artificial intelligence that will be evaluated in the Pydantic library is groq. The diaries are saved to Firebase 
and every time the application is opened, the previously written diaries are pulled from the Firebase realtime database.

To run the project uniquely, you need a groq api key and a firebase api key. The necessary information for Firebase needs to be saved in 
credentials.json and the groq api key needs to be saved in the .env file.

To run project, you need to write 'streamlit run HomePage.py' on terminal. 
