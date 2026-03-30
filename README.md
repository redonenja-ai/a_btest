# 🎯 A/B Voting Studio

An interactive Streamlit application for A/B testing with human voting, spin wheel points, and AI persona simulations.

## Features

- **📤 Upload Options**: Upload images for Option A and Option B with custom titles
- **🗳️ User Voting**: Cast votes and see real-time results with progress bars
- **🎰 Spin Wheel**: Earn random points (0-50) with animated spinning
- **🤖 AI Persona Simulation**: Simulate up to 100 AI personas voting based on appeal scores
- **📊 Analytics**: Combined charts showing human vs AI voting patterns

## Installation

```bash
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

## How It Works

1. **Set Up**: Upload images and set AI appeal scores (0-100) for each option
2. **Vote**: Cast human votes for your preferred option
3. **Spin**: Click the spin button to earn random points
4. **AI Test**: Run AI persona simulations to see how different profiles would vote
5. **Analyze**: View combined results and determine the winner

## AI Persona Logic

AI personas vote based on the appeal scores you set:
- Higher appeal score = higher probability of being voted for
- Each persona has a random preference type and confidence level
- Results are displayed in a detailed table
