from setuptools import setup, find_packages

setup(
    name="rpg_game",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="A text-based RPG game",
    entry_points={
        'console_scripts': [
            'rpg-game=rpg_game.main:main',
        ],
    },
    python_requires='>=3.6',
)
