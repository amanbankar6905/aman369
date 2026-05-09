This folder contains three separate tools each for 
1. Google search
2. Location to latitude,longitude converter
3. Weather information from Command Line Interface.

1. For Google search :
> Install - pip install googlesearch
>make sure the working directory and the code directory is same.
>Go to Serpapi for downloading googlesearch api for free.
>Copy the generated api-key and paste in your IDE's Environment Variables (.env) file.
>Give the input for google search on your terminal as "python your_file_name.py "your search topic"
>The results will be available on the terminal

2. For Location CLI Tool
> pip install dotenv
>Go to OpenWeather API which provides free api for location search via the special "Geocoding" api call provided at "https://openweathermap.org/api/geocoding-api?collection=other"
>copy the key in the openweathermap.org dashboard and paste in the ".env" variables of your IDE.
> For running the tool in terminal type "python your-filename.py "your place"
>The results will be available in the terminal


3. For Weather CLI Tool
>Use the same API key used in LocationCLI_Tool.
>Download the city codes from "https://bulk.openweathermap.org/sample/?utm_source=copilot.com" 
> Enter the command for getting the weather by searching for the city code in the "city code" JSON file and enter the command as python your-weather-filename.py {city code}
>The results will be available as per the format in the openweathermap.org dashboard.
