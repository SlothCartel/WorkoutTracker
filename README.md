# WorkoutTracker

WorkoutTracker is a Python-based application designed to help users track their workouts and monitor their fitness progress. The application allows users to log different types of exercises, set goals, and visualize their progress over time.

## Features

- Log workouts with details such as exercise type, duration, and intensity
- Set and track fitness goals
- Visualize progress with charts and graphs
- User-friendly interface

## Getting Started

Follow these steps to set up and run the WorkoutTracker application on your local machine.

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/SlothCartel/WorkoutTracker.git
    cd WorkoutTracker
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Start the application:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and navigate to `http://localhost:8000` to access the WorkoutTracker interface.

## Contributing

We welcome contributions to improve WorkoutTracker. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
