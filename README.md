# Memes Generator 


![Version](https://img.shields.io/badge/Version-1.0-blue.svg?style=plastic&logo=appveyor&logoColor=white&color=blueviolet)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue.svg?style=plastic&logo=windows&logoColor=white&color=green)
[![GitHub contributors](https://img.shields.io/github/contributors-anon/Sk-Azraf-Sami/Memes-Generator?style=plastic&labelColor=&color=blue&logo=)](https://github.com/Sk-Azraf-Sami/Memes-Generator/graphs/contributors)
[![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Sk-Azraf-Sami/Memes-Generator?style=plastic&labelColor=&color=blue&logo=)](https://github.com/Sk-Azraf-Sami/Memes-Generator/commits/main)
[![GitHub language count](https://img.shields.io/github/languages/count/Sk-Azraf-Sami/Memes-Generator?style=plastic&labelColor=&color=blue&logo=)](https://github.com/Sk-Azraf-Sami/Memes-Generator/search?l=python&type=Code)
![GitHub repo size](https://img.shields.io/github/repo-size/Sk-Azraf-Sami/Memes-Generator?style=plastic)
![License](https://img.shields.io/badge/License-[MIT]-blue.svg?style=plastic&color=orange&logo=GitHub)


## Table of Contents 
- [Description](#description)
- [User Interface](#user-interface)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)


## [Description](#description)

The **Meme Generator** is an innovative web application built using Python and Flask that allows users to create personalized memes with a wide range of features, including text addition, padding, collage creation, black-and-white conversion, image enhancement, Gaussian blurring, and background removal. It demonstrates key techniques in image processing and computer vision, making it both a practical tool and an educational platform.

Key features include:
- **Text Addition**: Customize memes with captions and credits.
- **Padding**: Add borders to images for better formatting.
- **Collage Creation**: Combine multiple images into a single composite image.
- **Image Enhancement**: Use histogram equalization to improve contrast.
- **Black-and-White Conversion**: Convert images to grayscale.
- **Blurring**: Apply Gaussian blur to reduce noise and smooth images.
- **Background Removal**: Remove backgrounds using advanced techniques like GrabCut.


## [User Interface](#user-interface)

This is the live version of the website:  
[https://memes-generator-g87x.onrender.com/](https://memes-generator-g87x.onrender.com/)

The user interface includes:  
1. **Home Page**: A welcoming interface where users can upload images.  
2. **Tools Page**: After uploading an image, users can access various tools to modify the image.  
3. **Tool-Specific UI**: Each tool (e.g., Text Addition, Padding, Background Removal) has a dedicated, easy-to-use modal or interface to adjust settings interactively.  

For example:
- The **Text Addition Tool** allows users to dynamically adjust the position, size, and color of the text on the image.  
- The **Collage Tool** includes options to specify rows and upload multiple images.  

Check out the live demo to explore the full set of features!


## [Installation](#installation)
To install the MemeLab , follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Sk-Azraf-Sami/Memes-Generator.git
    ```

2. **Install the required dependencies:**
    Make sure you have `pip` installed and then run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure you have Python installed:**
    The game was developed using Python 3.x. You can download the latest version from [python.org](https://www.python.org/downloads/). After installation, verify that Python is installed correctly by running:
    ```bash
    python --version
    ```
    or, for some systems:
    ```bash
    python3 --version
    ```

## [How to Run](#how-to-run)

To start the game, run the following command: 
```bash
python app.py
```
#### Additional Notes
- If you encounter any issues during installation, please check the repository's [issues section](https://github.com/Sk-Azraf-Sami/Memes-Generator/issues) for solutions or to report a problem.
- Be sure to check for updates regularly to keep the web app running smoothly.


## [Documentation](#documentation)

For detailed information about the 'Memes Generator', please refer to the [docummentation](https://github.com/Sk-Azraf-Sami/Memes-Generator/tree/main/document).


## [Contributing](#contributing)

Thank you for your interest in contributing to the 'Memes Generator'! We welcome contributions from everyone. To get started, please follow the guidelines below:

##### Bug Reports and Feature Requests

If you encounter any bugs or have ideas for new features, please open an issue on the GitHub repository. When opening an issue, provide as much detail as possible, including steps to reproduce the issue and any relevant information about your environment. This will help us investigate and address the problem more effectively.

##### Pull Requests

We gladly accept pull requests for bug fixes, enhancements, and new features. To contribute code to the project, follow these steps:

1. Fork the repository and create your branch from the `main` branch.
2. Make your changes, ensuring that your code adheres to the project's coding style and conventions.
3. Write tests to cover your changes and ensure the existing tests pass.
4. Ensure your code compiles without any errors or warnings.
5. Commit your changes and push your branch to your forked repository.
6. Open a pull request against the `main` branch of the original repository.
7. Provide a clear and descriptive title for your pull request and explain the changes you have made.
8. Be responsive to any feedback or questions during the review process.

By contributing to this project, you agree that your contributions will be licensed under the project's [MIT License](https://opensource.org/licenses/MIT).

##### Code Style and Conventions

To maintain consistency throughout the project's codebase, please adhere to the following guidelines:

- Use proper indentation and formatting.
- Follow naming conventions for variables, classes, and methods.
- Write clear and concise comments to improve code readability.
- Ensure your code is modular, reusable, and follows best practices.

##### Communication

If you have any questions or need assistance, feel free to reach out to the project maintainers or open an issue on GitHub.

We appreciate your contributions and look forward to working with you to improve this game!


## [License](#license)

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
